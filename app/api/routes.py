from fastapi import APIRouter, Depends, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.compliance_model import ComplianceResult
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import json
import os
import requests
from bs4 import BeautifulSoup

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import qrcode

# AI imports
from sentence_transformers import SentenceTransformer, util
import torch

router = APIRouter()

# Load AI model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Legal Requirements
# -----------------------------
LEGAL_REQUIREMENTS = {
    "Consent": "The policy must clearly state that user consent is obtained before processing personal data and that consent can be withdrawn.",
    "Data Retention": "The policy must specify how long personal data is retained and the criteria used to determine retention period.",
    "Data Security": "The policy must describe security safeguards such as encryption or technical measures used to protect personal data.",
    "Grievance Officer": "The policy must provide details of a grievance officer or contact mechanism for resolving complaints.",
    "Notice": "The policy must inform users about what personal data is collected and the purpose of collection.",
    "Third Party Sharing": "The policy must disclose whether personal data is shared with third parties or affiliates."
}

SECTION_WEIGHTS = {
    "Consent": 20,
    "Data Retention": 15,
    "Data Security": 20,
    "Grievance Officer": 15,
    "Notice": 15,
    "Third Party Sharing": 15
}

# -----------------------------
# Fetch Policy Text
# -----------------------------
def fetch_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text(separator=" ")
        return text.lower()

    except:
        return ""


# -----------------------------
# AI Semantic Analyzer
# -----------------------------
def analyze_policy_ai(text):

    results = {}
    total_score = 0

    sentences = text.split(".")
    paragraphs = [s.strip() for s in sentences if len(s.strip()) > 40]

    if not paragraphs:
        return {}, 0

    paragraph_embeddings = model.encode(paragraphs, convert_to_tensor=True)

    for section, requirement in LEGAL_REQUIREMENTS.items():

        req_embedding = model.encode(requirement, convert_to_tensor=True)
        similarities = util.cos_sim(req_embedding, paragraph_embeddings)[0]
        max_similarity = torch.max(similarities).item()

        weight = SECTION_WEIGHTS[section]

        if max_similarity > 0.65:
            status = "COMPLIANT"
            total_score += weight
        elif max_similarity > 0.45:
            status = "PARTIAL"
            total_score += weight * 0.5
        else:
            status = "NON-COMPLIANT"

        results[section] = status

    return results, round(total_score, 2)


# -----------------------------
# Main Route
# -----------------------------
@router.post("/check-compliance/")
def check_compliance(
    website: str = Form(...),
    db: Session = Depends(get_db)
):

    if not website.startswith("http"):
        website = "https://" + website

    privacy_url = website

    policy_text = fetch_text(privacy_url)

    if not policy_text:
        return {"error": "Unable to fetch privacy content."}

    section_data, score = analyze_policy_ai(policy_text)

    if score >= 75:
        risk = "Low Risk"
    elif score >= 50:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    compliant = list(section_data.values()).count("COMPLIANT")
    partial = list(section_data.values()).count("PARTIAL")
    non_compliant = list(section_data.values()).count("NON-COMPLIANT")

    values = [compliant, partial, non_compliant]

    if sum(values) == 0:
        values = [0, 0, 1]

    plt.figure(figsize=(4, 4))
    plt.pie(
        values,
        labels=["Compliant", "Partial", "Non-Compliant"],
        autopct="%1.1f%%"
    )
    chart_path = "chart.png"
    plt.savefig(chart_path)
    plt.close()

    new_result = ComplianceResult(
        website_url=website,
        compliance_percentage=int(score),
        risk_level=risk,
        section_analysis=json.dumps(section_data)
    )

    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    qr = qrcode.make(f"Report ID: {new_result.id} | Score: {score}%")
    qr_path = "qr.png"
    qr.save(qr_path)

    file_path = f"report_{new_result.id}.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)
    y = 750

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "AI-Based DPDP Compliance Audit Report")
    y -= 40

    c.drawString(50, y, f"Privacy Policy URL: {privacy_url}")
    y -= 20
    c.drawString(50, y, f"Compliance Score: {score}%")
    y -= 20
    c.drawString(50, y, f"Risk Level: {risk}")
    y -= 30

    for section, status in section_data.items():
        if status == "COMPLIANT":
            c.setFillColor(colors.green)
        elif status == "PARTIAL":
            c.setFillColor(colors.orange)
        else:
            c.setFillColor(colors.red)

        c.drawString(60, y, f"{section}: {status}")
        y -= 20

    c.setFillColor(colors.black)
    c.drawImage(chart_path, 300, 400, width=200, height=200)

    c.save()

    os.remove(chart_path)
    os.remove(qr_path)

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="AI_DPDP_Report.pdf"
    )
