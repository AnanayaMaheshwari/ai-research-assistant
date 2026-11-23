import os
from dotenv import load_dotenv
from strands.models.gemini import GeminiModel

load_dotenv()

def get_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.startswith("replace_"):
        raise RuntimeError("Set a valid GEMINI_API_KEY in the project-root .env file.")
    return GeminiModel(
        client_args={"api_key": api_key},
        model_id=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        params={"temperature": 0.2, "max_output_tokens": 4096},
    )
    