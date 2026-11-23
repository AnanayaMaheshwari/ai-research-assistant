# 🔎 AI Research Assistant

An intelligent, multi-agent research application designed to automate the research process using AI agents. The system breaks down complex research topics into smaller tasks, gathers information, analyzes findings, verifies facts, and generates structured research reports.

Built using **Strands Agents, Google Gemini, FastAPI, Streamlit, and MySQL**.

---

## 🚀 Overview

The AI Research Assistant uses a multi-agent architecture where specialized agents collaborate to complete different stages of a research task.

Instead of relying on a single AI model to handle the entire research process, the application distributes responsibilities among multiple agents.

### Key Capabilities

- **Automated Research Planning:** Breaks down research topics into manageable tasks.
- **Information Gathering:** Researches relevant information based on the generated plan.
- **AI-Powered Analysis:** Analyzes collected information and identifies important insights.
- **Fact Checking:** Reviews research findings for accuracy and consistency.
- **Report Generation:** Produces structured research reports.
- **Multiple Orchestration Strategies:** Supports different approaches to coordinating AI agents.
- **Research History:** Stores and retrieves previous research sessions and reports.
- **Interactive Dashboard:** Displays research statistics, activity, and recent reports.
- **Streaming Research:** Provides real-time research progress and generated responses.

---

## 🧠 Multi-Agent Architecture

The application consists of five specialized agents:

| Agent | Responsibility |
|---|---|
| Planner Agent | Creates a structured research plan. |
| Researcher Agent | Gathers relevant information. |
| Analyst Agent | Analyzes research findings and extracts insights. |
| Fact Checker Agent | Reviews findings and checks consistency. |
| Report Writer Agent | Generates the final research report. |

### Research Workflow

```text
             Research Topic
                   |
                   v
             Planner Agent
                   |
                   v
            Researcher Agent
                   |
                   v
              Analyst Agent
                   |
                   v
           Fact Checker Agent
                   |
                   v
           Report Writer Agent
                   |
                   v
             Final Report
```

---

## ⚙️ Orchestration Strategies

The application supports multiple approaches to agent coordination:

| Strategy | Description |
|---|---|
| Sequential | Agents execute one after another in a defined sequence. |
| Agents as Tools | A coordinating agent delegates tasks to specialized agents. |
| Graph | Research execution follows a structured graph-based workflow. |
| Swarm | Multiple agents collaborate through a dynamic coordination approach. |

These approaches allow different research execution patterns to be explored and compared.

---

## 🛠️ Technology Stack

### Backend
- Python
- FastAPI
- Strands Agents SDK
- Google Gemini

### Frontend
- Streamlit
- Python

### Database
- MySQL
- SQLAlchemy

### AI Architecture
- Multi-agent systems
- Agent orchestration
- Prompt engineering
- Tool integration
- Streaming responses

---

## 📁 Project Structure

```text
ai-research-assistant/
│
├── agents/
│   ├── planner.py
│   ├── researcher.py
│   ├── analyst.py
│   ├── fact_checker.py
│   ├── report_writer.py
│   ├── orchestrator.py
│   └── workflows/
│       ├── agents_as_tools.py
│       ├── research_graph.py
│       └── research_swarm.py
│
├── backend/
│   ├── main.py
│   ├── api/
│   │   └── routes/
│   └── services/
│
├── frontend/
│   ├── app.py
│   ├── pages/
│   ├── components/
│   └── services/
│
├── database/
│   ├── database.py
│   ├── models.py
│   └── repositories.py
│
├── memory/
│   └── session_manager.py
│
├── reports/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── SETUP.md
```

---

## 💻 Getting Started

For installation instructions, environment configuration, database setup, and commands to run the application, refer to **[SETUP.md](SETUP.md)**.

---

## 📊 Application Modules

### Dashboard
Provides an overview of research activity, completed reports, research statistics, and recent activity.

### New Research
Allows users to enter a research topic, select an orchestration strategy, and execute the research workflow.

### Research History
Provides access to previous research reports and conversations.

### Settings
Displays application configuration and backend information.

---

## 🔮 Future Enhancements

- Web search and external information retrieval integration.
- Source citations and reference tracking.
- Advanced research quality evaluation.
- Export reports to PDF and DOCX.
- User authentication and role-based access.
- More advanced agent collaboration strategies.
- Improved conversation memory and contextual follow-up questions.
- Research comparison and analytics.

---

## 🎯 Project Objective

The primary objective of this project is to explore and implement a practical multi-agent AI system capable of handling complex research tasks through specialized agents and different orchestration strategies.

It also serves as a practical implementation of agent-based AI development using the Strands Agents SDK.

---

## 👩‍💻 Built With

Python · Strands Agents · Google Gemini · FastAPI · Streamlit · MySQL

**AI-powered research. Specialized agents. Structured insights.**
