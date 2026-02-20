from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import engine, Base
from app.api.routes import router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DPDP Act 2023 Compliance Checker",
    version="4.0",
    description="AI-powered DPDP Act Compliance Analyzer"
)

# ==============================
# CORS CONFIGURATION
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later we can restrict to React URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)