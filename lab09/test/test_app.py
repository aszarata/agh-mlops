import pytest
from fastapi.testclient import TestClient
from main.app import app
from api.models.prediction import PredictRequest, PredictResponse
from sentence_transformers import SentenceTransformer
import joblib


client = TestClient(app)


def test_input_validation_model_inference_response_validation():
    response = client.post("/predict", json={"text": "I would really like seeing it again in hell."})
    assert response.status_code == 200
    data = response.json()
    prediction = data["prediction"]
    assert prediction in ["negative", "neutral", "positive"]
    assert isinstance(prediction, str)
    assert isinstance(data, dict)


def test_input_text_should_be_non_empty_string():
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422
    error_data = response.json()['detail'][0]['msg']
    assert 'Empty string is not valid' in error_data


def test_model_loads_without_errors():
    sentence_model = SentenceTransformer('model/sentence_transformer.model')
    model = joblib.load('model/classifier.joblib')
    assert sentence_model is not None
    assert model is not None


def test_inference_should_work_for_sample_strings():
    test_cases = [
        "Implementing this feels like I'm dying",
        "Implementing this feels like I'm walking",
        "Implementing this feels like I'm on my holiday in Bahamas",
        "?!./[{*&"
    ]

    for text in test_cases:
        response = client.post("/predict", json={"text": text})
        assert response.status_code == 200
        data = response.json()
        prediction = data["prediction"]
        assert isinstance(data, dict)
        assert isinstance(prediction, str)
        assert prediction in ["negative", "neutral", "positive"]


def test_output_should_be_valid_json_response():
    response = client.post("/predict", json={"text": "Random text"})
    assert response.status_code == 200
    data = response.json()
    prediction = data["prediction"]
    assert prediction in ["negative", "neutral", "positive"]


def test_invalid_input_should_return_json_with_error_explanation():
    response = client.post("/predict", json={"text": 123})
    assert response.status_code == 422
    error_data = response.json()['detail'][0]['msg']
    assert 'Input should be a valid string' in error_data