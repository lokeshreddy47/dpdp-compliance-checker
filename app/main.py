from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import engine, Base
from app.api.routes import router
from app.core.logging_config import logger


# ==============================
# Create Database Tables
# ==============================
Base.metadata.create_all(bind=engine)


# ==============================
# Create FastAPI App
# ==============================
app = FastAPI(
    title="DPDP Act 2023 Compliance Checker",
    version="4.0",
    description="AI-powered semantic DPDP Act compliance analyzer"
)


# ==============================
# Logging Startup
# ==============================
logger.info("DPDP Compliance Backend Started Successfully")


# ==============================
# CORS Configuration
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# Include API Routes
# ==============================
app.include_router(router)