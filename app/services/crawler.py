import requests
from bs4 import BeautifulSoup


def fetch_privacy_policy(url: str):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted elements
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # Extract only paragraph text
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])

        cleaned_text = " ".join(text.split())

        print("Extracted length:", len(cleaned_text))  # DEBUG

        if len(cleaned_text) < 1000:
            print("Content too small.")
            return None

        return cleaned_text

    except Exception as e:
        print("Crawler Error:", e)
        return None