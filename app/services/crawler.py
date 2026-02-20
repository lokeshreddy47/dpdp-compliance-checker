import requests
from bs4 import BeautifulSoup


def fetch_privacy_policy(url: str):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove junk elements
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # Extract text from paragraphs AND divs
        paragraphs = soup.find_all(["p", "div"])

        text_chunks = []

        for tag in paragraphs:
            content = tag.get_text(strip=True)
            if len(content) > 50:
                text_chunks.append(content)

        cleaned_text = " ".join(text_chunks)

        print("Extracted length:", len(cleaned_text))

        if len(cleaned_text) < 500:
            return None

        return cleaned_text

    except Exception as e:
        print("Crawler Error:", e)
        return None