from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from typing import Dict, Any


def generate_audit_report(data: Dict[str, Any], output_path: str) -> str:
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Audit Trail Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    for key, value in data.items():
        elements.append(Paragraph(f"<b>{key}</b>: {value}", styles["Normal"]))
        elements.append(Spacer(1, 8))

    doc.build(elements)
    return output_path
