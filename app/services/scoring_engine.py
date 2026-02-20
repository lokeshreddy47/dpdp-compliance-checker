import matplotlib
matplotlib.use("Agg")

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import numpy as np
import os


# Load lightweight semantic model
model = SentenceTransformer("all-MiniLM-L6-v2")


DPDP_CLAUSES = {
    "Notice": "The data fiduciary must provide clear notice before collecting personal data.",
    "Consent": "Personal data must be collected only after obtaining free and informed consent.",
    "Data Principal Rights": "Data principals have the right to access, correct and erase personal data.",
    "Data Security": "Reasonable security safeguards must be implemented to protect personal data.",
    "Grievance Redressal": "A grievance officer must be appointed to address complaints."
}


def analyze_compliance(policy_text: str):

    results = {}
    missing = []
    total_score = 0
    clause_names = []
    clause_scores = []

    # Split into chunks
    sentences = [s.strip() for s in policy_text.split(".") if len(s.strip()) > 15]

    # Encode all sentences once
    sentence_embeddings = model.encode(sentences)

    for clause, clause_text in DPDP_CLAUSES.items():

        clause_embedding = model.encode([clause_text])

        similarities = cosine_similarity(
            clause_embedding,
            sentence_embeddings
        )[0]

        max_score = np.max(similarities) * 100
        final_score = round(float(max_score), 2)

        clause_names.append(clause)
        clause_scores.append(final_score)
        total_score += final_score

        if final_score > 35:
            results[clause] = {
                "similarity_score": final_score,
                "status": "Matched",
                "matched_clause_text": clause_text
            }
        else:
            missing.append(clause)
            results[clause] = {
                "similarity_score": final_score,
                "status": "Missing",
                "matched_clause_text": None
            }

    overall_score = round(total_score / len(DPDP_CLAUSES), 2)

    if overall_score >= 75:
        risk = "Low Risk"
    elif overall_score >= 45:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    # Generate Graph
    if not os.path.exists("reports"):
        os.makedirs("reports")

    graph_path = "reports/compliance_chart.png"

    plt.figure()
    plt.bar(clause_names, clause_scores)
    plt.xlabel("Clauses")
    plt.ylabel("Semantic Similarity Score (%)")
    plt.title("DPDP Compliance Semantic Analysis")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(graph_path)
    plt.close()

    return {
        "overall_score": overall_score,
        "risk_level": risk,
        "section_analysis": results,
        "missing_clauses": missing,
        "graph_path": graph_path
    }


def generate_recommendations(result: dict):

    recommendations = []

    if result["missing_clauses"]:
        for clause in result["missing_clauses"]:
            recommendations.append(
                f"The policy lacks sufficient coverage for '{clause}'. Consider strengthening this section."
            )
    else:
        recommendations.append(
            "The privacy policy demonstrates strong semantic alignment with DPDP Act 2023 provisions."
        )

    return recommendations