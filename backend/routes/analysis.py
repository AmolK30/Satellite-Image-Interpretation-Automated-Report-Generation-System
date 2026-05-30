from __future__ import annotations

from pathlib import Path
import logging

from flask import Blueprint, current_app, jsonify, request, send_file

from backend.extensions import db
from backend.models import AnalysisRecord
from backend.services.feature_extractor import validate_image_file
from backend.services.pipeline import AnalysisPipeline
from backend.utils.files import ensure_directory, secure_storage_name


LOGGER = logging.getLogger(__name__)
analysis_bp = Blueprint("analysis", __name__)
pipeline = AnalysisPipeline()


def _store_upload(uploaded_file) -> tuple[str, str]:
    uploads_dir = ensure_directory(current_app.config["UPLOAD_FOLDER"])
    stored_name = secure_storage_name(uploaded_file.filename)
    stored_path = uploads_dir / stored_name
    uploaded_file.save(stored_path)
    return stored_name, str(stored_path)


@analysis_bp.post("/analyze")
def analyze_image():
    if "image" not in request.files:
        return jsonify({"error": "Missing image file in request."}), 400

    uploaded_file = request.files["image"]
    if not uploaded_file.filename:
        return jsonify({"error": "A valid filename is required."}), 400

    try:
        validate_image_file(uploaded_file.filename, file_size=request.content_length, max_size=current_app.config["MAX_CONTENT_LENGTH"])
        image_name, image_path = _store_upload(uploaded_file)
        result = pipeline.analyze(image_path=image_path, image_name=image_name)

        pdf_path = None
        if request.form.get("generate_pdf", "true").lower() in {"1", "true", "yes"}:
            reports_dir = ensure_directory(current_app.config["REPORT_FOLDER"])
            pdf_path = str(reports_dir / f"{Path(image_name).stem}.pdf")
            pipeline.pdf_exporter.build_report(
                output_path=pdf_path,
                title="Satellite Image Analysis Report",
                image_path=image_path,
                report_text=result["report"],
                land_distribution=result["land_distribution"],
                environmental_score=result["environment_score"],
                environmental_summary=result["environmental_summary"],
                disaster_summary=result["disaster_summary"],
            )

        record = AnalysisRecord(
            analysis_type="single",
            image_name=image_name,
            image_path=image_path,
            report_text=result["report"],
            environment_score=result["environment_score"],
            land_distribution=result["land_distribution"],
            environmental_summary=result["environmental_summary"],
            disaster_summary=result["disaster_summary"],
            comparison_summary=None,
            pdf_path=pdf_path,
        )
        db.session.add(record)
        db.session.commit()

        response = record.to_dict()
        response.update(result)
        response["pdf_path"] = pdf_path
        return jsonify(response), 200
    except Exception as exc:
        db.session.rollback()
        LOGGER.exception("Analysis failed")
        return jsonify({"error": str(exc)}), 400


@analysis_bp.post("/compare-images")
def compare_images():
    old_file = request.files.get("old_image")
    new_file = request.files.get("new_image")
    if not old_file or not new_file or not old_file.filename or not new_file.filename:
        return jsonify({"error": "Both old_image and new_image are required."}), 400

    try:
        validate_image_file(old_file.filename, file_size=request.content_length, max_size=current_app.config["MAX_CONTENT_LENGTH"])
        validate_image_file(new_file.filename, file_size=request.content_length, max_size=current_app.config["MAX_CONTENT_LENGTH"])

        old_name, old_path = _store_upload(old_file)
        new_name, new_path = _store_upload(new_file)

        old_result = pipeline.analyze(old_path, old_name)
        new_result = pipeline.analyze(new_path, new_name)
        comparison = pipeline.compare(old_result, new_result)

        record = AnalysisRecord(
            analysis_type="comparison",
            image_name=f"{old_name}::{new_name}",
            image_path=f"{old_path}::{new_path}",
            report_text=comparison["report"],
            environment_score=new_result["environment_score"],
            land_distribution=new_result["land_distribution"],
            environmental_summary=new_result["environmental_summary"],
            disaster_summary=new_result["disaster_summary"],
            comparison_summary=comparison,
            pdf_path=None,
        )
        db.session.add(record)
        db.session.commit()

        return jsonify({
            "old_image": old_result,
            "new_image": new_result,
            "urban_growth": comparison["urban_growth"],
            "forest_loss": comparison["forest_loss"],
            "report": comparison["report"],
            "record": record.to_dict(),
        }), 200
    except Exception as exc:
        db.session.rollback()
        LOGGER.exception("Comparison failed")
        return jsonify({"error": str(exc)}), 400


@analysis_bp.get("/reports/<int:record_id>/pdf")
def download_pdf(record_id: int):
    record = db.session.get(AnalysisRecord, record_id)
    if not record or not record.pdf_path:
        return jsonify({"error": "PDF report not found."}), 404
    pdf_path = Path(record.pdf_path)
    if not pdf_path.exists():
        return jsonify({"error": "PDF file is missing from disk."}), 404
    return send_file(pdf_path, as_attachment=True, download_name=pdf_path.name)
