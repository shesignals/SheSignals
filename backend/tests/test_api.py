import sys
import os
import pytest

# Ensure the backend root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from server import app


@pytest.fixture(scope="module")
def client():
    """Use as context manager so lifespan events (model loading) fire."""
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert len(data["loaded_models"]) > 0
    assert data["feature_names_loaded"] is True


def test_predict_success_lr(client):
    payload = {
        "model": "lr",
        "features": {
            "Age of the girl": 5,
        }
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "Recommendation" in data
    assert data["model_used"] == "lr"
    assert "probability" in data
    assert "0" in data["probability"]
    assert "1" in data["probability"]


def test_predict_success_rf(client):
    payload = {
        "model": "rf",
        "features": {
            "Age of the girl": 8,
        }
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 200
    assert response.json()["model_used"] == "rf"


def test_predict_success_xgb(client):
    payload = {
        "model": "xgb",
        "features": {
            "Age of the girl": 10,
        }
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 200
    assert response.json()["model_used"] == "xgb"


def test_predict_invalid_model(client):
    payload = {
        "model": "invalid_model_abc",
        "features": {},
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 400
    assert "invalid_model_abc" in response.json()["detail"]


def test_predict_invalid_data_type(client):
    payload = {
        "model": "lr",
        "features": {
            "Age of the girl": "not-a-number",
        }
    }
    response = client.post("/v1/predict", json=payload)
    # Pydantic should catch this and return a 422 Unprocessable Entity
    assert response.status_code == 422


def test_predict_extra_field_rejected(client):
    """Schema has extra='forbid', so unknown features should be rejected."""
    payload = {
        "model": "lr",
        "features": {
            "Age of the girl": 5,
            "totally_fake_feature": 99,
        }
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 422


def test_predict_default_model(client):
    """If no model is specified, should default to 'lr'."""
    payload = {
        "features": {},
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 200
    assert response.json()["model_used"] == "lr"
