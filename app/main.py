from fastapi import FastAPI
from app.api.routes import router
from app.database.db import Base, engine
from app.models import compliance_model

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(router)
