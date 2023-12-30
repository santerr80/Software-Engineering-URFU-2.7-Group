from fastapi.testclient import TestClient
from main import app
import pytest
import os
import pandas as pd
import requests

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "<h1>TapexTokenizer</h1>"
    
@pytest.fixture
def upload_file():
    headers = {'accept': 'application/json'}
    file_path = "gorbunovav/FastAPI_app/countries.csv"
    response = client.post("/uploadfile/",
                            headers=headers,
                            files={"file": ('countries.csv', open(file_path, 'rb'), 'text/csv')})
    return response.status_code

@pytest.fixture
def my_request():
    response = client.post("/request/", params={'my_request': "canada population"})
    return response.status_code

def test_tokenize(upload_file, my_request):
    response = client.get("/tokenize/")
    assert response.status_code == 200
    assert response.json()['response'][0].strip() == "38.05"


def test_translation_endpoint():
    input_text = "Пример входного текста для перевода на английский."
    response = requests.post("http://localhost:8000/translate", json={"text": input_text})
    assert response.status_code == 200
    assert "translation" in response.json()
