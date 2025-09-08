# Real-time Story Generation via LLMs and Prompt Engineering

An end-to-end project that streams short stories in real-time from a Large Language Model, with a prompt-engineering toolkit, evaluation scripts, and an MLOps-ready deployment stack.

## Quickstart (Local Dev with Streamlit)

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # set HF_TOKEN and ENDPOINT_MODE
streamlit run app/streamlit_app.py
```

## Use gdown to fetch from Drive into ./models

pip install gdown

## API Server (FastAPI)

```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

## Docker

```bash
docker build -t story-rt:latest .
docker run --env-file .env -p 8000:8000 story-rt:latest
```

## Project Structure

```
app/                # FastAPI + Streamlit apps
src/                # core library: prompts, clients, metrics
notebooks/          # experiments & prompt engineering
mlops/              # CI/CD, docker, make targets , Github actions
data/               # (gitignored) sample inputs/outputs
report/             # final report template
tests/              # unit tests
```

## MLOps Highlights

- **Config via `.env`**: switch between `INFERENCE_API` and `INFERENCE_ENDPOINT` modes
- **GitHub Actions**: lint, test, build
- **Dockerized**: production-ready FastAPI server
- **Eval**: automatic metrics (distinct-n, repetition rate, readability, perplexity proxy)

> ⚠️ Note: Running 70B models locally is not feasible for most machines. This project uses Hugging Face Inference API or a managed Inference Endpoint. Provide your `HF_TOKEN` in `.env`.
