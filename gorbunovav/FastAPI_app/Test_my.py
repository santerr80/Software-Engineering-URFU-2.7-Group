from fastapi.testclient import TestClient
from main import app
import pytest
import os
import pandas as pd

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "TapexTokenizer"}
    
@pytest.fixture
def upload_file():
    data_frame = pd.read_csv(r"C:\Python\Environments\Program_of_engeneer\Test_app\countries.csv", encoding='utf-8', sep=';')
    df = data_frame.astype(str)
    return df

@pytest.fixture
def my_request():
    return "Get me most small country"

def test_tokenize(upload_file, my_request):
    print(upload_file)
    print(my_request)
    responce = client.get("/tokenize/")
    assert responce.status_code == 200
    assert responce.json() == {"response": "belarus"}
    
    
print(upload_file())