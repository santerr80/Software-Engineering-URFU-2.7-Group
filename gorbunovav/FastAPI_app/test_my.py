from fastapi.testclient import TestClient
from main import app
import pytest
import pandas as pd

client = TestClient(app)

def test_root():
    "Проверка работы сервиса."
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
    "Проверка работы модели."
    response = client.get("/tokenize/")
    assert response.status_code == 200
    assert response.json()['response'][0].strip() == "38.05"


def test_df_upload(upload_file):
    "Проверка правильной загрузки таблицы."
