import matplotlib
matplotlib.use("Agg")

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.core.config import settings


# ==============================
# Load Semantic Model (from .env)
# ==============================
model = SentenceTransformer(settings.MODEL_NAME)


# ==============================
# Load DPDP Clauses from JSON
# ==============================
def load_clauses():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file_path = os.path.join(base_dir, "data", "dpdp_clauses.json")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ==============================
# Analyze Compliance
# ==============================
def analyze_compliance(policy_text: str):

    clauses = load_clauses()

    results = {}
    missing = []
    total_score = 0
    clause_names = []
    clause_scores = []

    # Split policy into meaningful sentences
    sentences = [
        s.strip()
        for s in policy_text.split(".")
        if len(s.strip()) > 20
    ]

    if not sentences:
        return {
            "overall_score": 0,
            "risk_level": "High Risk",
            "section_analysis": {},
            "missing_clauses": [],
            "graph_path": ""
        }

    # Encode policy sentences once
    sentence_embeddings = model.encode(sentences)

    for clause in clauses:
        clause_title = clause["title"]
        clause_text = clause["description"]

        clause_embedding = model.encode([clause_text])

        similarities = cosine_similarity(
            clause_embedding,
            sentence_embeddings
        )[0]

        max_score = float(np.max(similarities)) * 100
        final_score = round(max_score, 2)

        clause_names.append(clause_title)
        clause_scores.append(final_score)
        total_score += final_score

        # Use threshold from .env
        if final_score >= settings.SIMILARITY_THRESHOLD:
            results[clause_title] = {
                "similarity_score": final_score,
                "status": "Matched",
                "matched_clause_text": clause_text
            }
        else:
            missing.append(clause_title)
            results[clause_title] = {
                "similarity_score": final_score,
                "status": "Missing",
                "matched_clause_text": None
            }

    overall_score = round(total_score / len(clauses), 2)

    # Risk Classification
    if overall_score >= 75:
        risk = "Low Risk"
    elif overall_score >= 45:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    # ==============================
    # Generate Graph
    # ==============================
    if not os.path.exists("reports"):
        os.makedirs("reports")

    graph_path = "reports/compliance_chart.png"

    plt.figure()
    plt.bar(clause_names, clause_scores)
    plt.xlabel("DPDP Clauses")
    plt.ylabel("Semantic Similarity Score (%)")
    plt.title("DPDP Compliance Clause Analysis")
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


# ==============================
# Generate Recommendations
# ==============================
def generate_recommendations(result: dict):

    recommendations = []

    if result["missing_clauses"]:
        for clause in result["missing_clauses"]:
            recommendations.append(
                f"The policy lacks sufficient coverage for '{clause}'. Consider strengthening this section."
            )
    else:
        recommendations.append(
            "The privacy policy demonstrates strong alignment with DPDP Act 2023 provisions."
        )

    return recommendations