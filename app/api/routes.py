from fastapi import APIRouter
from pydantic import BaseModel
from app.services.crawler import crawl_website
from app.services.nlp_analyzer import analyze_text
from app.services.scoring_engine import calculate_score

router = APIRouter()

class URLRequest(BaseModel):
    url: str


@router.post("/check-compliance")
def check_compliance(request: URLRequest):
    content = crawl_website(request.url)
    analysis = analyze_text(content)
    score = calculate_score(analysis)

    return {
        "website": request.url,
        "result": score,
        "details": analysis
    }
