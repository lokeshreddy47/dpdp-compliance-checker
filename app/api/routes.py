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
    # Improved Scoring Logic
    # ==============================
    score = 0

    if "privacy" in content:
        score += 25

    if "consent" in content:
        score += 20

    if "retention" in content:
        score += 20

    if "grievance" in content or "complaint" in content:
        score += 15

    if "personal data" in content or "personal information" in content:
        score += 20

    # Risk Level Logic
    if score >= 70:
        risk_level = "Low Risk"
    elif score >= 40:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    # Save to Database
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

    return {
        "message": "Compliance check completed",
        "compliance_percentage": score,
        "risk_level": risk_level
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
