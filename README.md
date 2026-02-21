# ML Web Service on FastAPI (Sentiment Analysis)

A small educational project to demonstrate **FastAPI** skills: a REST web service with ML inference (NLP sentiment analysis) using a Hugging Face model.

The project uses the **`seara/rubert-base-cased-russian-sentiment`** model (labels: `neutral`, `positive`, `negative`).

## Features
- REST API built with FastAPI
- `/predict` endpoint for sentiment prediction
- Automatic Swagger/OpenAPI docs (`/docs`)
- Pytest tests for the ML part
- Local run and Docker run

## Project structure
- `app/` — FastAPI application
- `ml/` — model loading + config
- `tests/` — tests (pytest)
- `Dockerfile` — containerization
- `requirements.txt`, `requirements-dev.txt` — dependencies
- `setup.py` — packaging (editable install)

## API

### `GET /`
Health check.

Example response:
```json
{"text": "Sentiment Analysis"}
```
`GET /predict?text=...`

Predict sentiment for the given text.

Example request:

- `GET /predict?text=очень%20хорошо`

Example response:
```json
{
  "text": "очень хорошо",
  "sentiment_label": "positive",
  "sentiment_score": 0.98
}
```

## Local development (Windows PowerShell)
1) Create and activate a virtual environment
```PowerShell
 py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```
2) Install dependencies

### Editable install:

`pip install -e .`

### Dev dependencies:

`pip install -e ".[dev]"`

3) Run the app

`uvicorn app.app:app --reload --host 127.0.0.1 --port 8080`

Open:

http://127.0.0.1:8080/

http://127.0.0.1:8080/docs

### Tests

Run all tests:

`python -m pytest -q`

Run only ML tests:

`python -m pytest -q tests/test_ml.py`
## Docker
Build

`docker build -t ml-app .`

Run

`docker run --rm -p 8080:8080 ml-app`

Open:

http://127.0.0.1:8080/

http://127.0.0.1:8080/docs

In Docker, uvicorn must listen on 0.0.0.0, otherwise the container won’t be reachable from the host.
