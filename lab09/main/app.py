from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import joblib
from api.models.prediction import PredictRequest, PredictResponse
import os

app = FastAPI()

# sentence_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

sentiment_classes = {0: 'negative', 1: 'neutral', 2: 'positive'}
encoder = SentenceTransformer('model/sentence_transformer.model')
classifier = joblib.load('model/classifier.joblib')

@app.get("/")
def root():
    return {"message": "Sentiment Analysis API"}


@app.post("/predict")
def predict_sentiment(request: PredictRequest):
    embedding = encoder.encode([request.text])
    prediction = classifier.predict(embedding)[0]
    return PredictResponse(prediction=sentiment_classes[prediction])