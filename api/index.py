from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from uuid import uuid4
from fastapi import FastAPI, HTTPException
import secrets
from datetime import datetime
import requests
from datetime import datetime

from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    user_login: str
    user_token: str
    user_password: str
    user_id: str

class AuthUser(BaseModel):
    user_login: str
    user_password: str

TOKEN = '6027542967:AAH634BtIzZSQiYOIn33WcV1-RQ_9v7bfk0'
# bot = Bot(token=bot_token)
# dp = Dispatcher()

client = MongoClient(
    "mongodb://admin:TEST!SRV1_!%23%23%23@nik.ydns.eu:402"
    # "mongodb://localhost:27017"
    )

db = client.resfull_test
users_collection = db['users']

app = FastAPI()
origins = ["*"]  # Разрешаем все источники

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы запросов (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки запросов
)

@app.get("/test")
async def root():
    return {"message": "Test successful"}

# СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ CORRECT
@app.post("/registration")
def create_user(user: User):
    user_id = str(uuid4())
    user.user_id = user_id
    user_dict = user.dict()
    user_dict['user_password'] = bcrypt.hashpw(user_dict["user_password"].encode('utf-8'), bcrypt.gensalt())
    user_dict['user_token'] =f'{secrets.token_hex(20)}'

    if users_collection.find_one({"user_login": user.user_login}):
        raise HTTPException(status_code=404, detail="This login already exists")
    else:
        users_collection.insert_one(user_dict)
        return {"message": "User has successfully registered"}
    
# Авторизация пользователя CORRECT
@app.post('/login')
def login(user: AuthUser):
    user_ex = users_collection.find_one({"user_login": user.user_login})
    if user_ex:
        if bcrypt.checkpw(user.user_password.encode('utf-8'), user_ex['user_password']):
            return User(**user_ex)
        else:
            raise HTTPException(status_code=404, detail="User password wrong")
    else:
        raise HTTPException(status_code=404, detail="That login does not exist")
    


@app.post('/send_msg')
def send_msg(msg:str, token: str, id:str):
    user_ex = users_collection.find_one({"user_token": token})
    if user_ex:
        url = f"https://api.telegram.org/bot{TOKEN}"
        print(requests.get(url).json())
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("Today's date:", dt_string)
        msg+=f"\n Today's date: {dt_string}"
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={id}&text={msg}"
        print(requests.get(url).json())
    else:
        raise HTTPException(status_code=404, detail="ERROR")
    