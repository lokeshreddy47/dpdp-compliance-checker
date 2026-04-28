import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "DPDP Compliance API Running"}


def test_analyze_url_invalid():
    response = client.post("/analyze-url", json={"url": "not-a-valid-url"})
    assert response.status_code == 200
    assert "error" in response.json()


def test_reports_history_empty():
    response = client.get("/reports-history")
    assert response.status_code == 200
    assert response.json() == []


def test_cors_headers():
    response = client.options("/")
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

