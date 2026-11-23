# AI Research Assistant — Strands Agents POC

A full-stack research assistant built with Strands Agents + Gemini, FastAPI,
Streamlit and SQLite. It plans a research question, searches the web, fetches
pages, analyzes evidence, checks claims for support, and writes a Markdown/DOCX report.

## 1. Setup (Windows PowerShell)

```powershell
# From the project root, activate your existing virtual environment
.\.venv\Scripts\Activate.ps1

# Install project dependencies
python -m pip install -r requirements.txt

# Create your local environment file
Copy-Item .env.example .env
# Edit .env and add your Google AI Studio API key

# Start the backend (Terminal 1)
uvicorn backend.main:app --reload

# Start the frontend (Terminal 2)
streamlit run frontend/app.py
```

Open Streamlit at http://localhost:8501 and API docs at http://localhost:8000/docs.

## 2. Project modes

- `sequential`: explicit Python orchestration (default, easiest to understand)
- `graph`: Strands Graph with a fixed planner → researcher → analyst → fact-checker → writer path
- `swarm`: Strands Swarm with autonomous agent handoffs
- `agents_as_tools`: manager agent delegates to specialist agents

## 3. Notes

- Web search uses DDGS; search availability/rate limits depend on the provider.
- Search snippets and fetched pages are evidence, not guaranteed truth. The
  fact-checking agent identifies unsupported claims; it does not guarantee truth.
- Gemini API usage may incur charges or be subject to free-tier quotas.
- Never commit `.env` or expose your API key.
- Reports are saved under `reports/`; SQLite data is stored locally.
- This is a learning POC, not a production-grade fact verification system.

## 4. API endpoints

- `GET /api/health`
- `POST /api/research`
- `GET /api/history`
- `GET /api/history/{research_id}`

## 5. Course mapping

The project demonstrates model configuration, agent prompts, custom tools,
agent invocation, tool use, multi-agent delegation, Graph, Swarm, sessions,
API integration, persistence, evaluation and application deployment.
