import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(
    dotenv_path=PROJECT_ROOT / ".env",
    override=True
)

BASE_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).strip().rstrip("/")

# Prevent duplicate /api/api URLs.
while BASE_URL.endswith("/api"):
    BASE_URL = BASE_URL[:-4]


def health_check():
    response = requests.get(
        f"{BASE_URL}/api/health",
        timeout=10
    )

    response.raise_for_status()
    return response.json()


def create_session():
    response = requests.post(
        f"{BASE_URL}/api/sessions",
        json={},
        timeout=20
    )

    response.raise_for_status()
    return response.json()


def get_session(session_id: str):
    response = requests.get(
        f"{BASE_URL}/api/sessions/{session_id}",
        timeout=20
    )

    response.raise_for_status()
    return response.json()


def get_sessions():
    response = requests.get(
        f"{BASE_URL}/api/sessions",
        timeout=30
    )

    response.raise_for_status()
    return response.json()


def delete_session(session_id: str):
    response = requests.delete(
        f"{BASE_URL}/api/sessions/{session_id}",
        timeout=30
    )

    response.raise_for_status()
    return response.json()


def start_research(
    topic,
    mode="sequential",
    session_id=None
):
    response = requests.post(
        f"{BASE_URL}/api/research",
        json={
            "topic": topic,
            "mode": mode,
            "session_id": session_id
        },
        timeout=1800
    )

    response.raise_for_status()
    return response.json()


def stream_research(
    topic,
    mode="sequential",
    session_id=None
):
    """
    Yield decoded Server-Sent Event payloads
    from the streaming endpoint.
    """

    with requests.post(
        f"{BASE_URL}/api/research/stream",
        json={
            "topic": topic,
            "mode": mode,
            "session_id": session_id
        },
        headers={
            "Accept": "text/event-stream"
        },
        stream=True,
        timeout=(20, 1800)
    ) as response:

        response.raise_for_status()
        response.encoding = "utf-8"

        for line in response.iter_lines(
            decode_unicode=True
        ):
            if not line or not line.startswith("data:"):
                continue

            payload = line[len("data:"):].strip()

            if payload:
                yield json.loads(payload)


def get_history(limit=50):
    response = requests.get(
        f"{BASE_URL}/api/history",
        params={"limit": limit},
        timeout=20
    )

    response.raise_for_status()
    return response.json()


def get_research(research_id):
    response = requests.get(
        f"{BASE_URL}/api/history/{research_id}",
        timeout=20
    )

    response.raise_for_status()
    return response.json()


def delete_research(research_id):
    response = requests.delete(
        f"{BASE_URL}/api/history/{research_id}",
        timeout=20
    )

    response.raise_for_status()
    return response.json()