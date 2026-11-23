import os
from ddgs import DDGS
from strands import tool
from dotenv import load_dotenv

load_dotenv()

@tool
def web_search(query: str, max_results: int = 5) -> str:
    '''Search the web for relevant pages. Args: query: Search phrase. max_results: Number of results (1–10).'''
    try:
        limit = max(1, min(int(max_results), 10))
        results = DDGS().text(query, max_results=limit)
        if not results:
            return "No results returned. Try a different query."
        lines = []
        for i, item in enumerate(results, 1):
            lines.append(
                f"{i}. {item.get('title', 'Untitled')}\n"
                f"URL: {item.get('href', '')}\n"
                f"Snippet: {item.get('body', '')}"
            )
        return "\n\n".join(lines)
    except Exception as exc:
        return f"Search error: {type(exc).__name__}: {exc}"
