from fastapi import FastAPI
from app.api.routes import router
from app.database.db import engine
from app.database.db import Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DPDP Act 2023 Compliance Checker",
    description="Automated DPDP compliance auditing tool for Indian web applications",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "DPDP Compliance Checker API is running successfully"
    }
