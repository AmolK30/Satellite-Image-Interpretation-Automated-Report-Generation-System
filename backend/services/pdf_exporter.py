from __future__ import annotations

from pathlib import Path
from typing import Any
import logging

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


LOGGER = logging.getLogger(__name__)


class PDFExporter:
    def build_report(
        self,
        output_path: str | Path,
        title: str,
        image_path: str | None,
        report_text: str,
        land_distribution: dict[str, int],
        environmental_score: int,
        environmental_summary: dict[str, Any],
        disaster_summary: dict[str, Any],
    ) -> str:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="SectionTitle", parent=styles["Heading2"], textColor=colors.HexColor("#0f172a")))

        story = [Paragraph(title, styles["Title"]), Spacer(1, 0.2 * inch)]

        if image_path and Path(image_path).exists():
            try:
                story.append(Image(image_path, width=5.6 * inch, height=3.2 * inch))
                story.append(Spacer(1, 0.2 * inch))
            except Exception as exc:  # pragma: no cover
                LOGGER.warning("Unable to add image to PDF: %s", exc)

        story.extend([
            Paragraph("Report Overview", styles["SectionTitle"]),
            Paragraph(report_text.replace("\n", "<br/>"), styles["BodyText"]),
            Spacer(1, 0.15 * inch),
            Paragraph("Land Distribution", styles["SectionTitle"]),
        ])

        table_data = [["Class", "Percentage"]] + [[label.title(), f"{value}%"] for label, value in land_distribution.items()]
        table = Table(table_data, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.HexColor("#e2e8f0")]),
        ]))
        story.extend([
            table,
            Spacer(1, 0.15 * inch),
            Paragraph("Environmental Metrics", styles["SectionTitle"]),
            Paragraph(f"Score: {environmental_score}/100", styles["BodyText"]),
            Paragraph(f"Interpretation: {environmental_summary.get('interpretation', '')}", styles["BodyText"]),
            Spacer(1, 0.15 * inch),
            Paragraph("Disaster Analysis", styles["SectionTitle"]),
            Paragraph(f"Risk Level: {disaster_summary.get('risk_level', 'Unknown')}", styles["BodyText"]),
            Paragraph(f"Threats: {', '.join(disaster_summary.get('threats', []))}", styles["BodyText"]),
            Paragraph(f"Recommendations: {', '.join(disaster_summary.get('recommendations', []))}", styles["BodyText"]),
        ])

        doc.build(story)
        return str(output)
