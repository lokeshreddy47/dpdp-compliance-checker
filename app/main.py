from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="DPDP Compliance Analyzer API",
    description="AI-powered API to analyze website privacy policies and check compliance with the Digital Personal Data Protection (DPDP) Act 2023.",
    version="1.0.0",
    contact={
        "name": "Lokesh Reddy",
        "email": "support@example.com"
    }
)

app.include_router(router)