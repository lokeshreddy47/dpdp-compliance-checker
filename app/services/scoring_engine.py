def calculate_score(analysis: dict):
    found = analysis.get("found_categories", [])
    total_categories = 6  # total DPDP categories

    score = int((len(found) / total_categories) * 100)

    if score >= 80:
        risk = "Low Risk"
    elif score >= 50:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    return {
        "compliance_percentage": score,
        "risk_level": risk
    }
