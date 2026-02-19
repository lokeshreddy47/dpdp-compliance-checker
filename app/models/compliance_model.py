from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.db import Base

class ComplianceResult(Base):
    __tablename__ = "compliance_results"

    id = Column(Integer, primary_key=True, index=True)
    website_url = Column(String, nullable=False)
    compliance_percentage = Column(Integer)
    risk_level = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
