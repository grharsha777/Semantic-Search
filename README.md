Semantic Search — Secure, production-ready scaffold

Quick start

1. Copy `.env.example` to `.env` and fill `GEMINI_API_KEY`.

2. Create a virtual env and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

3. (Optional) Patch the original notebook to remove hardcoded keys:

```bash
python scripts/fix_notebook_secrets.py "C:\\Users\\G R  HARSHA\\OneDrive\\Desktop\\Semantic Search.ipynb"
```

This creates `Semantic Search.secure.ipynb` with GEMINI_API_KEY loaded from environment.

4. Run the FastAPI app (example):

```bash
uvicorn semantic_search.app:app --reload --port 8000
```

5. Git / GitHub

```bash
git init
git add .
git commit -m "Initial scaffold: secure keys, package, CI"
git remote add origin https://github.com/grharsha777/Semantic-Search.git
git branch -M main
git push -u origin main
```

Files added
- `.env.example` — example environment variables
- `.gitignore` — ignore secrets & artifacts
- `requirements.txt` — pinned deps for the project
- `scripts/fix_notebook_secrets.py` — helper to patch the notebook safely
- `semantic_search/` — library + FastAPI app
- `Dockerfile`, `.github/workflows/ci.yml` — CI / deployment

Security notes
- Never commit `.env` or real API keys. Use GitHub Secrets for CI and deployment.

If you want, I can run the notebook-fix script now and/or initialize a local git repo and create the first commit for you.