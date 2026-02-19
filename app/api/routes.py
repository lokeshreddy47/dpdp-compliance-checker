from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.compliance_model import ComplianceResult

router = APIRouter()   # ← THIS LINE IS REQUIRED


@router.get("/reports")
def get_reports():
    db: Session = SessionLocal()
    reports = db.query(ComplianceResult).all()
    db.close()
    return reports
