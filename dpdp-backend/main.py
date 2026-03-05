from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

import os
import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

from services.scoring_engine import analyze_compliance


app = FastAPI(title="DPDP Compliance Checker API")


# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ensure reports folder exists
if not os.path.exists("reports"):
    os.makedirs("reports")


# Serve generated files (charts, reports)
app.mount("/reports", StaticFiles(directory="reports"), name="reports")


@app.get("/")
def read_root():
    return {"message": "DPDP Compliance API Running"}


# ==========================
# Analyze Privacy Policy (File Upload)
# ==========================
@app.post("/analyze-policy")
async def analyze_policy(file: UploadFile = File(...)):

    # Read uploaded file
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    # Run AI compliance analysis
    result = analyze_compliance(text)

    # Save Report History
    save_report(file.filename, result)

    return result


# ==========================
# URL Input Model
# ==========================
class URLRequest(BaseModel):
    url: str


# ==========================
# Analyze Privacy Policy from URL
# ==========================
@app.post("/analyze-url")
def analyze_url(data: URLRequest):

    try:
        response = requests.get(data.url)

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract main policy content
        policy_section = soup.find("main") or soup.find("article") or soup.find("div")

        if policy_section:
            text = policy_section.get_text(separator=" ")
        else:
            text = soup.get_text(separator=" ")

        # Run AI analysis
        result = analyze_compliance(text)

        save_report(data.url, result)

        return result

    except Exception as e:
        return {"error": str(e)}

# ==========================
# Save Report History
# ==========================
def save_report(source, result):

    report = {
        "filename": source,
        "score": result["overall_score"],
        "risk": result["risk_level"],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    reports_file = "reports/report_history.json"

    if os.path.exists(reports_file):
        with open(reports_file, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append(report)

    with open(reports_file, "w") as f:
        json.dump(history, f, indent=2)


# ==========================
# Get Report History
# ==========================
@app.get("/reports-history")
def get_reports():

    reports_file = "reports/report_history.json"

    if not os.path.exists(reports_file):
        return []

    with open(reports_file, "r") as f:
        history = json.load(f)

    return history


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)