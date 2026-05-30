from __future__ import annotations

from pathlib import Path
import logging

from flask import Flask, jsonify
from flask_cors import CORS

from backend.config import Config
from backend.extensions import db
from backend.routes.analysis import analysis_bp
from backend.routes.history import history_bp


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
LOGGER = logging.getLogger(__name__)


def create_app(config: Config | None = None) -> Flask:
    app = Flask(__name__)
    settings = config or Config()
    app.config.from_mapping(
        SECRET_KEY=settings.secret_key,
        SQLALCHEMY_DATABASE_URI=settings.database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAX_CONTENT_LENGTH=settings.max_content_length,
        UPLOAD_FOLDER=settings.upload_folder,
        REPORT_FOLDER=settings.report_folder,
        ENABLE_HF_MODELS=settings.enable_hf_models,
        HF_TEXT_MODEL=settings.hf_text_model,
    )

    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)

    app.register_blueprint(analysis_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/api")

    @app.get("/")
    def health_check():
        return jsonify({"status": "ok", "service": "satellite-analysis-system", "documentation": "/api/history"})

    @app.errorhandler(413)
    def payload_too_large(_error):
        return jsonify({"error": "File too large."}), 413

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Route not found."}), 404

    @app.errorhandler(500)
    def server_error(_error):
        return jsonify({"error": "Unexpected server error."}), 500

    with app.app_context():
        Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
        Path(app.config["REPORT_FOLDER"]).mkdir(parents=True, exist_ok=True)
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
