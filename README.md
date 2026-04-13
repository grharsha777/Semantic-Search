
Overview
--------
This repository contains a secure, production-focused scaffold for a semantic-search / sentiment-analysis project that uses Google Gemini embeddings and generation APIs. It includes:

- A small Python package (`semantic_search`) with config and API helpers
- A FastAPI service exposing lightweight endpoints for embedding and labeling
- Dockerfile for containerising the service
- CI (GitHub Actions) running unit tests
- Scripts to remove hardcoded secrets from notebooks and load secrets from `.env`

Quick Start (local)
-------------------
1. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`.

2. Create virtual environment and install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
```

3. Run the API locally:

```powershell
uvicorn semantic_search.app:app --reload --port 8000
```

API Endpoints
-------------
- POST `/embed` — JSON body `{ "texts": ["...", "..."] }` returns `embeddings` (list of vectors)
- POST `/label` — JSON body `{ "texts": ["...", "..."] }` returns `labels` (list of sentiment labels)

Example (curl):

```bash
curl -X POST http://localhost:8000/embed \
	-H "Content-Type: application/json" \
	-d '{"texts":["I love this","This is ok"]}'

curl -X POST http://localhost:8000/label \
	-H "Content-Type: application/json" \
	-d '{"texts":["I love this","This is ok"]}'
```

Docker (build & run)
--------------------
```bash
docker build -t semantic-search:latest .
docker run --rm -p 8080:8080 --env-file .env semantic-search:latest
```

CI / Tests
----------
The repository includes a GitHub Actions workflow that installs dependencies and runs `pytest`.

Security Best Practices
----------------------
- Never commit `.env` or secrets; use `.env.example` as a template.
- Use GitHub Secrets / environment variables for CI and deployments.
- Rotate API keys regularly and avoid embedding them in notebooks.

Resume-ready Highlights
----------------------
- Built an LLM-driven sentiment-labeling pipeline using Google Gemini for both generation and embeddings.
- Implemented production API using `FastAPI`, containerised with `Docker` and CI-tested with GitHub Actions.
- Added secure secret management (dotenv + notebook sanitizer) and robust retry/fallback logic for API calls.
- Created reproducible data-processing pipeline, visualisations, and model evaluation artifacts.

Files of interest
-----------------
- `semantic_search/` — core package (`config.py`, `search.py`, `app.py`)
- `scripts/fix_notebook_secrets.py` — patches notebooks to load secrets from environment
- `Dockerfile` — container image for deployment
- `.github/workflows/ci.yml` — CI pipeline (runs `pytest`)

Next steps
----------
- Add more unit/integration tests for the `semantic_search` module and API.
- Add linting (flake8/ruff) and type checks (mypy) to CI.
- Optionally, add deployment manifest (Helm / Kubernetes / Azure/GCP) for production rollout.

If you want, I can now: (A) push these README changes to GitHub, (B) add more tests and linting, or (C) produce a concise resume bullet list and demo screenshots. Which should I do next?
