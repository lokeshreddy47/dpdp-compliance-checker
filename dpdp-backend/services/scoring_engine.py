import matplotlib
matplotlib.use("Agg")

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from core.config import settings


# ==============================
# Load Semantic Model
# ==============================
model = SentenceTransformer(settings.MODEL_NAME)


# ==============================
# Load DPDP Clauses
# ==============================
def load_clauses():

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file_path = os.path.join(base_dir, "data", "dpdp_clauses.json")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ==============================
# AI Compliance Analysis
# ==============================
def analyze_compliance(policy_text: str):

    clauses = load_clauses()

    results = {}
    missing = []
    total_score = 0
    clause_names = []
    clause_scores = []
    explanations = []

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
            "recommendations": [],
            "graph_path": "",
            "explanations": []
        }

    # Encode policy sentences
    sentence_embeddings = model.encode(sentences)

    for clause in clauses:

        clause_title = clause["title"]
        clause_text = clause["description"]
        clause_section = clause["section"]
        clause_category = clause["category"]

        clause_embedding = model.encode([clause_text])

        similarities = cosine_similarity(
            clause_embedding,
            sentence_embeddings
        )[0]

        best_index = int(np.argmax(similarities))
        best_sentence = sentences[best_index]

        similarity_score = float(similarities[best_index]) * 100
        final_score = round(similarity_score, 2)

        clause_names.append(clause_title)
        clause_scores.append(final_score)

        total_score += final_score

        explanations.append({
            "clause_title": clause_title,
            "section": clause_section,
            "category": clause_category,
            "policy_sentence": best_sentence,
            "similarity_score": final_score
        })

        if final_score >= settings.SIMILARITY_THRESHOLD:

            results[clause_title] = {
                "section": clause_section,
                "category": clause_category,
                "similarity_score": final_score,
                "status": "Matched"
            }

        else:

            missing.append(clause_title)

            results[clause_title] = {
                "section": clause_section,
                "category": clause_category,
                "similarity_score": final_score,
                "status": "Missing"
            }

    overall_score = round(total_score / len(clauses), 2)

    # ==============================
    # Risk Classification
    # ==============================
    if overall_score >= 75:
        risk = "Low Risk"
    elif overall_score >= 45:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    # ==============================
    # Generate Recommendations
    # ==============================
    recommendations = []

    if missing:
        for clause in missing:
            recommendations.append(
                f"The privacy policy should include a section for '{clause}' to improve DPDP compliance."
            )
    else:
        recommendations.append(
            "The privacy policy appears well aligned with DPDP Act 2023 requirements."
        )

    # ==============================
    # Generate Compliance Graph
    # ==============================
    if not os.path.exists("reports"):
        os.makedirs("reports")

    graph_path = "reports/compliance_chart.png"

    plt.figure(figsize=(10, 5))
    plt.bar(clause_names, clause_scores)
    plt.xlabel("DPDP Clauses")
    plt.ylabel("Similarity Score (%)")
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
        "recommendations": recommendations,
        "graph_path": graph_path,
        "explanations": explanations
    }