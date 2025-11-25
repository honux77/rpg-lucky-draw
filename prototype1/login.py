from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "YOUR_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
NAVER_REDIRECT_URI = os.getenv("NAVER_REDIRECT_URI", "http://localhost:8000/callback")

@router.get("/")
async def index(request: Request):
    naver_auth_url = (
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code"
        f"&client_id={NAVER_CLIENT_ID}"
        f"&redirect_uri={NAVER_REDIRECT_URI}"
        f"&state=RANDOM_STATE"
    )
    return templates.TemplateResponse("index.html", {"request": request, "naver_auth_url": naver_auth_url})

@router.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    if not code:
        return templates.TemplateResponse("error.html", {"request": request, "message": "인증 코드가 없습니다."})

    token_url = "https://nid.naver.com/oauth2.0/token"
    params = {
        "grant_type": "authorization_code",
        "client_id": NAVER_CLIENT_ID,
        "client_secret": NAVER_CLIENT_SECRET,
        "code": code,
        "state": state,
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(token_url, params=params)
        token_data = res.json()

    access_token = token_data.get("access_token")
    if not access_token:
        return templates.TemplateResponse("error.html", {"request": request, "message": f"토큰 오류: {token_data}"})

    request.session["access_token"] = access_token

    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        res = await client.get("https://openapi.naver.com/v1/nid/me", headers=headers)
        profile = res.json()
        request.session["profile"] = profile

    return RedirectResponse(url="/profile")


# 프로필 페이지 엔드포인트
@router.get("/profile")
async def profile(request: Request):
    profile = request.session.get("profile")
    if not profile:
        return templates.TemplateResponse("error.html", {"request": request, "message": "세션에 프로필 정보가 없습니다."})
    return templates.TemplateResponse("profile.html", {"request": request, "profile": profile})
