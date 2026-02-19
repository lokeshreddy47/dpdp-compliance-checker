from fastapi import FastAPI
from app.database.db import engine, Base
from app.api.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DPDP Act 2023 Compliance Checker",
    version="3.0"
)

app.include_router(router)
