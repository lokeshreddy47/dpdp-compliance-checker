import requests
from bs4 import BeautifulSoup

def crawl_website(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator=" ")
        cleaned_text = " ".join(text.split())

        return cleaned_text.lower()

    except Exception as e:
        return ""
