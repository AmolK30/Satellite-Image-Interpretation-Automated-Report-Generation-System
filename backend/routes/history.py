from __future__ import annotations

from flask import Blueprint, jsonify, request

from backend.extensions import db
from backend.models import AnalysisRecord


history_bp = Blueprint("history", __name__)


@history_bp.get("/history")
def history_list():
    limit = request.args.get("limit", default=20, type=int)
    records = AnalysisRecord.query.order_by(AnalysisRecord.created_at.desc()).limit(max(1, min(limit, 100))).all()
    return jsonify([record.to_dict() for record in records]), 200


@history_bp.delete("/history/<int:record_id>")
def delete_history(record_id: int):
    record = db.session.get(AnalysisRecord, record_id)
    if record is None:
        return jsonify({"error": "Record not found."}), 404
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Record deleted successfully."}), 200
