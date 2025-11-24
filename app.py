from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import imaplib

app = FastAPI()

# السماح بالوصول من أي مصدر للواجهة
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Email Checker API Running"}

@app.post("/check")
def check_email(email: str = Form(...), password: str = Form(...), provider: str = Form(...)):
    imap_servers = {
        "gmail": "imap.gmail.com",
        "yahoo": "imap.mail.yahoo.com",
        "outlook": "imap-mail.outlook.com"
    }

    server = imap_servers.get(provider.lower())
    if not server:
        return {"status": "fail", "message": "Unsupported provider"}

    try:
        mail = imaplib.IMAP4_SSL(server)
        mail.login(email, password)
        mail.logout()
        return {"status": "success", "message": "Password is valid"}
    except imaplib.IMAP4.error:
        return {"status": "fail", "message": "Invalid email or password"}
