from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.compliance_model import ComplianceResult

router = APIRouter()


@router.post("/check-compliance")
def check_compliance(data: dict):
    website_url = data.get("website_url")

    # Dummy compliance logic (for now)
    compliance_percentage = 50
    risk_level = "Medium Risk"

    db: Session = SessionLocal()

    new_record = ComplianceResult(
        website_url=website_url,
        compliance_percentage=compliance_percentage,
        risk_level=risk_level
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    db.close()

    return {
        "message": "Compliance check completed",
        "compliance_percentage": compliance_percentage,
        "risk_level": risk_level
    }


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

