import requests
import urllib3
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.compliance_model import ComplianceResult

# Disable SSL warnings (Development only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

router = APIRouter()


# ==============================
# POST - Check Compliance
# ==============================
@router.post("/check-compliance")
def check_compliance(data: dict):
    website_url = data.get("website_url")

    if not website_url:
        return {"error": "Website URL is required"}

    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(
            website_url,
            headers=headers,
            timeout=5,
            verify=False
        )

        response.raise_for_status()
        content = response.text.lower()

    except Exception as e:
        return {"error": f"Unable to fetch website: {str(e)}"}

    # ==============================
    # Detailed Compliance Detection
    # ==============================

    privacy_found = "privacy" in content
    consent_found = "consent" in content
    retention_found = "retention" in content
    grievance_found = "grievance" in content or "complaint" in content
    personal_data_found = "personal data" in content or "personal information" in content

    # ==============================
    # Score Calculation
    # ==============================

    score = 0

    if privacy_found:
        score += 25

    if consent_found:
        score += 20

    if retention_found:
        score += 20

    if grievance_found:
        score += 15

    if personal_data_found:
        score += 20

    # ==============================
    # Risk Level Classification
    # ==============================

    if score >= 70:
        risk_level = "Low Risk"
    elif score >= 40:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    # ==============================
    # Save to Database
    # ==============================

    db: Session = SessionLocal()

    new_record = ComplianceResult(
        website_url=website_url,
        compliance_percentage=score,
        risk_level=risk_level
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    db.close()

    # ==============================
    # Return Response
    # ==============================

    return {
        "message": "Compliance check completed",
        "compliance_percentage": score,
        "risk_level": risk_level,
        "details": {
            "privacy_policy_found": privacy_found,
            "consent_mechanism_found": consent_found,
            "data_retention_policy_found": retention_found,
            "grievance_mechanism_found": grievance_found,
            "personal_data_reference_found": personal_data_found
        }
    }


# ==============================
# GET - All Reports
# ==============================
@router.get("/reports")
def get_reports():
    db: Session = SessionLocal()

    reports = (
        db.query(ComplianceResult)
        .order_by(ComplianceResult.created_at.desc())
        .all()
    )

    db.close()
    return reports


# ==============================
# GET - Report by ID
# ==============================
@router.get("/reports/{report_id}")
def get_report_by_id(report_id: int):
    db: Session = SessionLocal()

    report = db.query(ComplianceResult).filter(
        ComplianceResult.id == report_id
    ).first()

    db.close()

    if not report:
        return {"error": "Report not found"}

    return report


# ==============================
# DELETE - Report by ID
# ==============================
@router.delete("/reports/{report_id}")
def delete_report(report_id: int):
    db: Session = SessionLocal()

    report = db.query(ComplianceResult).filter(
        ComplianceResult.id == report_id
    ).first()

    if not report:
        db.close()
        return {"error": "Report not found"}

    db.delete(report)
    db.commit()
    db.close()

    return {"message": f"Report {report_id} deleted successfully"}
