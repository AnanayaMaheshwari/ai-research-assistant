import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    app_name = "AI Research Assistant"
    backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    max_search_results = int(os.getenv("MAX_SEARCH_RESULTS", "5"))

settings = Settings()
