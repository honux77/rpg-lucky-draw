import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import httpx
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

load_dotenv()

app = FastAPI()
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY", "MY_SECRET_KEY"))

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "YOUR_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
NAVER_REDIRECT_URI = os.getenv("NAVER_REDIRECT_URI", "http://localhost:8000/callback")
CAFE_URL = "https://cafe.naver.com/paramsx"
templates = Jinja2Templates(directory="templates")

# 라우터 등록
from login import router as login_router
from posts import router as posts_router

app.include_router(login_router)
app.include_router(posts_router)
