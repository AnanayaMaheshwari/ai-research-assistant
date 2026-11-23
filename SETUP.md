# ⚙️ AI Research Assistant – Setup Guide

This guide explains how to configure, install, and run the AI Research Assistant locally.

## 1. Prerequisites

Install the following before setting up the project:

- Python 3.12
- Git
- MySQL Server or XAMPP
- Google Gemini API key

Check your Python installation:

```powershell
python --version
```

## 2. Clone the Repository

```powershell
git clone https://github.com/YOUR_USERNAME/ai-research-assistant.git

cd ai-research-assistant
```

Replace `YOUR_USERNAME` with your GitHub username.

## 3. Create a Virtual Environment

Create a Python virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

## 4. Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the project dependencies:

```powershell
pip install -r requirements.txt
```

## 5. Configure Environment Variables

Create a `.env` file in the project root.

Use the following template and adjust the variable names to match those referenced in your project configuration:

```env
# Google Gemini
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_configured_gemini_model

# Database
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/research_assistant?charset=utf8mb4

# Backend API
BACKEND_URL=http://127.0.0.1:8000
```

**Important:**
- Replace the API key with your own Gemini API key.
- Use the Gemini model configured in the project.
- Never commit your `.env` file to GitHub.
- Check the environment variable names in the source code and match them exactly.

## 6. Configure MySQL Database

Start MySQL using XAMPP or your local MySQL installation.

Open phpMyAdmin or MySQL and create the database:

```sql
CREATE DATABASE research_assistant
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

The application should connect using the database URL configured in `.env`.

Ensure the database username, password, host, and port match your local MySQL configuration.

## 7. Run the Backend

Open a terminal in the project root.

Activate the virtual environment if necessary:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start the FastAPI server:

```powershell
python -m uvicorn backend.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Keep this terminal running.

## 8. Run the Frontend

Open a second PowerShell terminal in the project root.

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start Streamlit:

```powershell
python -m streamlit run frontend/app.py
```

The frontend will be available at:

```text
http://localhost:8501
```

## 9. Application Workflow

Once both servers are running:

1. Open the Streamlit application.
2. Navigate to **New Research**.
3. Enter a research topic.
4. Select an orchestration strategy.
5. Start the research process.
6. Monitor agent execution and research progress.
7. View the generated research report.
8. Access previous reports through **Research History**.

## 10. Troubleshooting

### Database Connection Error

- Ensure MySQL is running.
- Verify the database exists.
- Check the database credentials in `.env`.
- Confirm that the configured MySQL port is correct.

### Gemini API Error

- Verify your Gemini API key.
- Check that the configured model is available.
- Ensure the API key has not expired or exceeded its usage limits.

### Backend Connection Error

- Ensure FastAPI is running on port `8000`.
- Check the `BACKEND_URL` value in `.env`.
- Verify that the backend routes are accessible.

### Missing Python Dependencies

Run:

```powershell
pip install -r requirements.txt
```

### Port Already in Use

If port `8000` or `8501` is already occupied, stop the existing process or configure another available port.

---

## 11. Running Both Services

The application requires two running processes:

| Service | Command | URL |
|---|---|---|
| Backend | `python -m uvicorn backend.main:app --reload` | `http://127.0.0.1:8000` |
| Frontend | `python -m streamlit run frontend/app.py` | `http://localhost:8501` |

Both terminals must remain open while using the application.

---

## 12. Security Notes

- Never upload API keys or passwords.
- Keep `.env` excluded through `.gitignore`.
- Use `.env.example` to share configuration templates.
- Do not commit virtual environments or local database files.

---

**Setup complete!** Your AI Research Assistant should now be running locally.