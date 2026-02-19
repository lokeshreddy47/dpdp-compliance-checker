import requests
import urllib3
from fastapi import APIRouter
from sqlalchemy.orm import Session
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from app.database.db import SessionLocal
from app.models.compliance_model import ComplianceResult

# Disable SSL warnings (Development only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

router = APIRouter()


# =========================================================
# POST - DPDP Compliance Check
# =========================================================
@router.post("/check-compliance")
def check_compliance(data: dict):
    website_url = data.get("website_url")

    if not website_url:
        return {"error": "Website URL is required"}

    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        # Fetch homepage
        response = requests.get(
            website_url,
            headers=headers,
            timeout=5,
            verify=False
        )
        response.raise_for_status()

        homepage_content = response.text
        soup = BeautifulSoup(homepage_content, "html.parser")

        combined_content = homepage_content.lower()

        # ==========================================
        # Detect Privacy Policy Page
        # ==========================================
        privacy_link = None

        for link in soup.find_all("a", href=True):
            if "privacy" in link.text.lower() or "privacy" in link["href"].lower():
                privacy_link = urljoin(website_url, link["href"])
                break

        # Fetch privacy policy page if found
        if privacy_link:
            try:
                privacy_response = requests.get(
                    privacy_link,
                    headers=headers,
                    timeout=5,
                    verify=False
                )
                privacy_response.raise_for_status()
                combined_content += privacy_response.text.lower()
            except:
                pass

    except Exception as e:
        return {"error": f"Unable to fetch website: {str(e)}"}

    # =========================================================
    # DPDP Act 2023 Section-Based Compliance Detection
    # =========================================================

    section_5_notice = "privacy" in combined_content or "notice" in combined_content
    section_6_consent = "consent" in combined_content
    section_7_lawful_use = "purpose" in combined_content or "lawful" in combined_content
    section_8_obligations = "data protection" in combined_content or "safeguard" in combined_content
    section_9_retention = "retention" in combined_content
    section_13_grievance = "grievance" in combined_content or "complaint" in combined_content
    section_10_dpo = "data protection officer" in combined_content or "dpo" in combined_content
    data_principal_rights = (
        "right" in combined_content
        or "access" in combined_content
        or "correction" in combined_content
    )

    # =========================================================
    # Score Calculation (100 Max)
    # =========================================================

    score = 0

    if section_5_notice:
        score += 15
    if section_6_consent:
        score += 15
    if section_7_lawful_use:
        score += 10
    if section_8_obligations:
        score += 15
    if section_9_retention:
        score += 15
    if section_13_grievance:
        score += 10
    if section_10_dpo:
        score += 10
    if data_principal_rights:
        score += 10

    # =========================================================
    # Risk Level Classification
    # =========================================================

    if score >= 70:
        risk_level = "Low Risk"
    elif score >= 40:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    # =========================================================
    # Save to Database
    # =========================================================

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

    # =========================================================
    # Response
    # =========================================================

    return {
        "message": "Compliance check completed",
        "compliance_percentage": score,
        "risk_level": risk_level,
        "privacy_page_detected": privacy_link if privacy_link else None,
        "dpdp_section_analysis": {
            "Section_5_Notice": section_5_notice,
            "Section_6_Consent": section_6_consent,
            "Section_7_Lawful_Use": section_7_lawful_use,
            "Section_8_Obligations": section_8_obligations,
            "Section_9_Data_Retention": section_9_retention,
            "Section_10_DPO": section_10_dpo,
            "Section_13_Grievance_Redressal": section_13_grievance,
            "Data_Principal_Rights": data_principal_rights
        }
    }


# =========================================================
# GET - All Reports
# =========================================================
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


# =========================================================
# GET - Report by ID
# =========================================================
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


# =========================================================
# DELETE - Report by ID
# =========================================================
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
