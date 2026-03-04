import spacy
import spacy

nlp = spacy.load("en_core_web_sm")

DPDP_REQUIREMENTS = {
    "consent": ["consent", "agree"],
    "data_retention": ["data retention", "retain"],
    "user_rights": ["right to delete", "right to correct"],
    "grievance_officer": ["grievance officer"],
    "purpose_limitation": ["purpose of processing"],
    "data_protection": ["security", "encryption"]
}

def analyze_text(text: str):
    found = []
    missing = []

    for category, keywords in DPDP_REQUIREMENTS.items():
        if any(keyword in text for keyword in keywords):
            found.append(category)
        else:
            missing.append(category)

    return {
        "found_categories": found,
        "missing_categories": missing
    }
