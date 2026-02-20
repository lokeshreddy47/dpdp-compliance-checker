import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MODEL_NAME = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 35))
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dpdp_compliance.db")

settings = Settings()