from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

# السماح للواجهة بالتواصل مع السيرفر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# تحقق من البريد الإلكتروني
def is_valid_email(email: str):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

# تحقق من كلمة السر (مثال: 8 حروف على الأقل)
def is_valid_password(password: str):
    return len(password) >= 8

@app.post("/check")
async def check_email(email: str = Form(...), password: str = Form(...)):
    return {
        "email_valid": is_valid_email(email),
        "password_valid": is_valid_password(password)
    }

@app.get("/")
def home():
    return {"message": "Email Checker API Running"}
