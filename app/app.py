from fastapi import FastAPI
from pydantic import BaseModel
from ml.model import load_model

model = None
app = FastAPI()

class SentimentResponse(BaseModel):
    text: str
    sentiment_label: str
    sentiment_score: float

# Создаем маршрут
@app.get("/")
def index():
    return {"text": "Sentiment Analysis"}

# Объявляем функцию, которая будет работать при запуске
@app.on_event("startup")
def startip_event():
    global model
    model = load_model()

#
@app.get('/predict')
def predict_sentiment(text: str):
    sentiment = model(text)

    response = SentimentResponse(
        text=text,
        sentiment_label=sentiment.label,
        sentiment_score=sentiment.score,
    )
    return response