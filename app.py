from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import imaplib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginData(BaseModel):
    email: str
    password: str
    server: str = "imap.gmail.com"

results = []

def check_email_password(email, password, server):
    try:
        mail = imaplib.IMAP4_SSL(server)
        mail.login(email, password)
        mail.logout()
        return True
    except:
        return False

@app.post("/check")
def check_password(data: LoginData):
    ok = check_email_password(data.email, data.password, data.server)
    result = {"email": data.email, "server": data.server, "valid": ok}
    results.append(result)
    return result

@app.get("/results")
def get_results():
    return results

@app.get("/")
def home():
    return {"message": "Email Checker API Running"}
