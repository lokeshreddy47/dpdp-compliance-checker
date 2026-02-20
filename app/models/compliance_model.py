from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from datetime import datetime
from app.database.db import Base


class ComplianceResult(Base):
    __tablename__ = "compliance_results"

    id = Column(Integer, primary_key=True, index=True)
    website_url = Column(String, nullable=False)

    compliance_percentage = Column(Float)
    risk_level = Column(String)

    section_analysis = Column(Text)
    missing_clauses = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)