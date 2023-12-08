from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import asyncio
import uvicorn
import TapexTokenizer
import pandas as pd

class Item(BaseModel):
    text: str

app = FastAPI()



"""
    Функция, которая обрабатывает корневую конечную точку ("/") приложения.
    
    Возвращает:
        HTMLResponse: Объект ответа, содержащий отображаемый HTML-контент.
    """
@app.get("/")
def read_root():
    html_content = "<h1>TapexTokenizer</h1>"
    return HTMLResponse(content=html_content)


"""
    Создание загружаемого файла.
    Параметры:
    - file (UploadFile): Файл для загрузки.
    Возвращает:
    - dict: Словарь, содержащий имя файла и dataframe, преобразованный в словарь.
    """
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    df = pd.read_csv(file.file, encoding='utf-8', sep=';')
    app.state.df = df
    return {"filename": file.filename, "dataframe": df.to_dict()}


"""
    Создание нового запроса.
    Параметры:
        my_request (str): Запрос, который необходимо создать.
    Возвращает:
        dict: Словарь, содержащий созданный запрос.
    """
@app.post("/request/")
async def create_request(my_request: str):
    app.state.request = my_request
    return {"Request": my_request}


 """
    Эта функция является асинхронным обработчиком маршрута для конечной точки API "/tokenize/". Она отвечает за токенизацию данных в `df` DataFrame с помощью класса TapexTokenizer.
    Параметры:
        None
    Возвращает:
        dict: Словарь, содержащий ответ от метода TapexTokenizer.tapex_tokenizer. Ответ хранится под ключом "response".
    """
@app.get("/tokenize/")
async def tokenize():
    df = app.state.df
    df = df.astype(str)
    my_request = app.state.request
    response = TapexTokenizer.tapex_tokenizer(df, my_request)
    return {"response": response}
    

 """
    Асинхронная функция, обслуживающая основное приложение.
    :return: None
    """
async def main():
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())