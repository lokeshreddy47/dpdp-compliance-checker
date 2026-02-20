from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import os


def generate_pdf_report(result: dict, website_url: str):

    if not os.path.exists("reports"):
        os.makedirs("reports")

    file_path = "reports/dpdp_compliance_report.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()

    # ===== Title =====
    elements.append(Paragraph("<b>DPDP Act 2023 Compliance Report</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    # ===== Website Info =====
    elements.append(Paragraph(f"<b>Website:</b> {website_url}", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    # ===== Summary Box =====
    summary_data = [
        ["Overall Compliance Score", f"{result['overall_score']} %"],
        ["Risk Level", result["risk_level"]]
    ]

    summary_table = Table(summary_data, colWidths=[3 * inch, 2 * inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 0.4 * inch))

    # ===== Clause-wise Table =====
    elements.append(Paragraph("<b>Clause-wise Analysis</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    table_data = [["Clause", "Score (%)", "Status"]]

    for clause, details in result["section_analysis"].items():
        table_data.append([
            clause,
            str(details["similarity_score"]),
            details["status"]
        ])

    clause_table = Table(table_data, colWidths=[2.5 * inch, 1.5 * inch, 1.5 * inch])

    clause_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ]))

    elements.append(clause_table)
    elements.append(Spacer(1, 0.4 * inch))

    # ===== Missing Clauses =====
    elements.append(Paragraph("<b>Missing Clauses</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    if result["missing_clauses"]:
        missing_list = [
            ListItem(Paragraph(clause, styles["Normal"]))
            for clause in result["missing_clauses"]
        ]
        elements.append(ListFlowable(missing_list, bulletType='bullet'))
    else:
        elements.append(Paragraph("No missing clauses identified.", styles["Normal"]))

    elements.append(Spacer(1, 0.4 * inch))

    # ===== Recommendations =====
    elements.append(Paragraph("<b>AI Recommendations</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    recommendation_list = [
        ListItem(Paragraph(rec, styles["Normal"]))
        for rec in result["recommendations"]
    ]
    elements.append(ListFlowable(recommendation_list, bulletType='bullet'))

    elements.append(Spacer(1, 0.5 * inch))

    # ===== Graph =====
    if os.path.exists(result["graph_path"]):
        elements.append(Paragraph("<b>Clause Similarity Graph</b>", styles["Heading2"]))
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Image(result["graph_path"], width=5 * inch, height=3 * inch))

    doc.build(elements)

    return file_path