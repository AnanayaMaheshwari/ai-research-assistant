import requests
from bs4 import BeautifulSoup
from strands import tool

@tool
def web_fetch(url: str, max_chars: int = 12000) -> str:
    '''Fetch readable text from a public webpage. Args: url: Full http/https URL. max_chars: Maximum characters to return.'''
    if not url.startswith(("http://", "https://")):
        return "Invalid URL: only http and https URLs are allowed."
    try:
        response = requests.get(
            url, timeout=20,
            headers={"User-Agent": "Mozilla/5.0 (compatible; ResearchAssistant/1.0)"}
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for node in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            node.decompose()
        text = " ".join(soup.get_text(" ").split())
        return text[:max(1000, min(int(max_chars), 20000))]
    except Exception as exc:
        return f"Fetch error for {url}: {type(exc).__name__}: {exc}"
