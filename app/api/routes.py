from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.compliance_model import ComplianceResult
from app.services.scoring_engine import analyze_compliance, generate_recommendations
from app.services.report_generator import generate_pdf_report
from app.services.crawler import fetch_privacy_policy
import json
import os

router = APIRouter()

@router.post("/check-compliance/")
def check_compliance(
    website_url: str = Form(...),
    db: Session = Depends(get_db)
):

    policy_text = fetch_privacy_policy(website_url)

    if not policy_text:
        raise HTTPException(status_code=400, detail="Unable to fetch privacy content.")

    result = analyze_compliance(policy_text)
    recommendations = generate_recommendations(result)
    result["recommendations"] = recommendations

    # Save to DB
    db_record = ComplianceResult(
        website_url=website_url,
        compliance_percentage=result["overall_score"],
        risk_level=result["risk_level"],
        section_analysis=json.dumps(result["section_analysis"]),
        missing_clauses=json.dumps(result["missing_clauses"])
    )

    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    pdf_path = generate_pdf_report(result, website_url)

    if os.path.exists(pdf_path):
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename="dpdp_compliance_report.pdf"
        )

    raise HTTPException(status_code=500, detail="PDF generation failed.")