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

@app.get("/posts", response_class=HTMLResponse)
async def show_form():
	html = """
	<h2>닉네임으로 카페 게시글 조회</h2>
	<form method='post'>
	  <input type='text' name='nickname' placeholder='닉네임 입력' required>
	  <button type='submit'>조회</button>
	</form>
	"""
	return HTMLResponse(content=html)

@app.post("/posts", response_class=HTMLResponse)
async def get_posts(nickname: str = Form(...)):
	# 네이버 검색 API 호출
	search_url = "https://openapi.naver.com/v1/search/cafearticle.json"
	headers = {
		"X-Naver-Client-Id": NAVER_CLIENT_ID,
		"X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
	}
	params = {
		"query": nickname,
		"display": 20,  # 최대 20개까지 조회
		"sort": "date"
	}
	async with httpx.AsyncClient() as client:
		res = await client.get(search_url, headers=headers, params=params)
		data = res.json()

	# 해당 카페에서 닉네임이 포함된 게시글만 필터링
	items = data.get("items", [])
	filtered = [item for item in items if CAFE_URL in item.get("link", "")]
	# 10개만 추출
	filtered = filtered[:10]

	# 결과 HTML 생성
	html = f"<h2>{nickname} 님의 게시글 (최신 10개)</h2>"
	if not filtered:
		html += "<p>게시글이 없습니다.</p>"
	else:
		html += "<ul>"
		for post in filtered:
			html += f"<li><a href='{post['link']}' target='_blank'>{post['title']}</a> ({post['postdate']})</li>"
		html += "</ul>"
	html += "<a href='/my-cafe-posts'>다시 조회</a>"
	return HTMLResponse(content=html)


@app.get("/")
async def index(request: Request):
    naver_auth_url = (
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code"
        f"&client_id={NAVER_CLIENT_ID}"
        f"&redirect_uri={NAVER_REDIRECT_URI}"
        f"&state=RANDOM_STATE"
    )
    return templates.TemplateResponse("index.html", {"request": request, "naver_auth_url": naver_auth_url})

@app.get("/callback")
async def callback(request: Request):
	code = request.query_params.get("code")
	state = request.query_params.get("state")
	if not code:
		return HTMLResponse(content="인증 코드가 없습니다.")

	# 네이버 토큰 요청
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
		return HTMLResponse(content=f"토큰 오류: {token_data}")

	# 토큰 정보를 세션에 저장
	request.session["access_token"] = access_token

	# 네이버 프로필 정보 요청
	headers = {"Authorization": f"Bearer {access_token}"}
	async with httpx.AsyncClient() as client:
		res = await client.get("https://openapi.naver.com/v1/nid/me", headers=headers)
		profile = res.json()

	return HTMLResponse(content=f"<pre>{profile}</pre><br><a href='/me'>내 토큰 확인</a>")

# 세션에 저장된 토큰 확인용 엔드포인트
@app.get("/me")
async def me(request: Request):
	access_token = request.session.get("access_token")
	if not access_token:
		return HTMLResponse(content="세션에 토큰이 없습니다.")
	return HTMLResponse(content=f"세션 토큰: {access_token}")
