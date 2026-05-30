from __future__ import annotations

from datetime import datetime, timezone

from backend.extensions import db


class AnalysisRecord(db.Model):
    __tablename__ = "analysis_records"

    id = db.Column(db.Integer, primary_key=True)
    analysis_type = db.Column(db.String(32), nullable=False, default="single")
    image_name = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(512), nullable=False)
    report_text = db.Column(db.Text, nullable=False)
    environment_score = db.Column(db.Integer, nullable=False)
    land_distribution = db.Column(db.JSON, nullable=False)
    environmental_summary = db.Column(db.JSON, nullable=False)
    disaster_summary = db.Column(db.JSON, nullable=False)
    comparison_summary = db.Column(db.JSON, nullable=True)
    pdf_path = db.Column(db.String(512), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "analysis_type": self.analysis_type,
            "image_name": self.image_name,
            "image_path": self.image_path,
            "report_text": self.report_text,
            "environment_score": self.environment_score,
            "land_distribution": self.land_distribution,
            "environmental_summary": self.environmental_summary,
            "disaster_summary": self.disaster_summary,
            "comparison_summary": self.comparison_summary,
            "pdf_path": self.pdf_path,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
