# ReAct Agent

A personal-assistant agent built with LangChain's `create_agent`, running on Groq, with tool access to Notion (notes + calendar). Served via FastAPI with a simple static web front-end.

## Features

- **ReAct-style agent** (`agent/bot.py`) using `langchain.agents.create_agent` with `ChatGroq` as the model backend.
- **Auto-updating model selection** (`utils/groq_models.py`) — fetches Groq's live model list at runtime and picks the best currently available free model, instead of relying on a hardcoded model ID that can silently break once Groq retires it.
- **Tools**:
  - `tools/notion_notes.py` — read and add notes in Notion.
  - `tools/notion_calender.py` — read and add calendar events in Notion.
- **FastAPI server** (`api/server.py`) exposing the agent, with a static HTML/CSS/JS front-end (`static/`) for chatting with it in the browser.
- **Setup script** (`scripts/setup_notion_databases.py`) to create the Notion databases the tools expect.
- **Test script** (`scripts/test_agent.py`) for quick agent sanity checks.
- Dockerfile, docker-compose, and a GitHub Actions deploy workflow.

## Requirements

- Python 3.12
- [uv](https://docs.astral.sh/uv/) (there's a `uv.lock`) or pip
- A [Groq API key](https://console.groq.com/keys)
- A Notion integration token + database IDs (for the Notion tools)

## Installation

```bash
git clone <this-repo>
cd ReAct_agent-main
uv sync
# or: pip install -r requirements.txt
```

Create a `.env` file:

```bash
GROQ_API_KEY=your-groq-key
# GROQ_MODEL=openai/gpt-oss-120b   # optional — see note below
NOTION_API_KEY=your-notion-integration-token
NOTION_NOTES_DB_ID=your-notes-database-id
NOTION_CALENDAR_DB_ID=your-calendar-database-id
```

> **Model selection:** `GROQ_MODEL` is optional. If it's left unset, `agent/bot.py` calls `utils/groq_models.py`, which queries Groq's `/openai/v1/models` endpoint at runtime, filters it down to chat-capable models, and picks the best one currently available (cached for an hour). This keeps the agent working automatically even after Groq deprecates a model — set `GROQ_MODEL` explicitly only if you want to pin a specific model instead.

If you're starting from scratch, run the Notion setup script first to create the databases:

```bash
python scripts/setup_notion_databases.py
```

## Usage

Run the API server:

```bash
uvicorn api.server:app --host 0.0.0.0 --port 8000
```

Then open `static/index.html` (served by the API, or directly in a browser pointed at the server) to chat with the agent.

Or explore the agent directly in the notebook:

```bash
jupyter notebook experiment.ipynb
```

Run the test script:

```bash
python scripts/test_agent.py
```

## Deployment

- `Dockerfile` / `docker-compose.yml` for containerized runs.
- `.github/workflows/deploy.yml` for CI/CD.

## Model

The agent auto-detects the best available free Groq model at runtime (`utils/groq_models.py`) rather than hardcoding one — see the `.env` section above for how to override this if you want a specific model.

## Tech stack

LangChain (`create_agent`) · langchain-groq · FastAPI · Groq (LLM inference) · Notion API

## Credits

This project is based on a project idea/tutorial from [Krish Naik's Projects](https://www.krishnaik.in/projects). I built and extended it as a hands-on learning project, including the auto-updating Groq model selection described above.