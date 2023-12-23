from fastapi.testclient import TestClient
from main import app
import pytest
import os
import pandas as pd

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "<h1>TapexTokenizer</h1>"
    
@pytest.fixture
def upload_file():
    headers = {'accept': 'application/json'}
    response = client.post("/uploadfile/",
                            headers=headers,
                            files={"file": ('countries.csv', open("countries.csv", 'rb'), 'text/csv')})
    for i in range(3):
        print(response.status_code)
    return response

@pytest.fixture
def my_request():
    response = client.post("/request/", params={'my_request': "canada population"})
    return response.status_code

def test_tokenize(upload_file, my_request):
    response = client.get("/tokenize/")
    assert response.status_code == 200
    assert response.json()['response'][0].strip() == "38.05"
