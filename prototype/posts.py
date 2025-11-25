from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
import httpx
import os

router = APIRouter()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "YOUR_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
CAFE_URL = "https://cafe.naver.com/paramsx"

@router.get("/posts", response_class=HTMLResponse)
async def show_form():
    html = """
    <h2>닉네임으로 카페 게시글 조회</h2>
    <form method='post'>
      <input type='text' name='nickname' placeholder='닉네임 입력' required>
      <button type='submit'>조회</button>
    </form>
    """
    return HTMLResponse(content=html)

@router.post("/posts", response_class=HTMLResponse)
async def get_posts(nickname: str = Form(...)):
    search_url = "https://openapi.naver.com/v1/search/cafearticle.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {
        "query": nickname,
        "display": 20,
        "sort": "date"
    }
    async with httpx.AsyncClient() as client:
        res = await client.get(search_url, headers=headers, params=params)
        data = res.json()

    items = data.get("items", [])
    filtered = [item for item in items if CAFE_URL in item.get("link", "")]
    filtered = filtered[:10]

    html = f"<h2>{nickname} 님의 게시글 (최신 10개)</h2>"
    if not filtered:
        html += "<p>게시글이 없습니다.</p>"
    else:
        html += "<ul>"
        for post in filtered:
            html += f"<li><a href='{post['link']}' target='_blank'>{post['title']}</a> ({post['postdate']})</li>"
        html += "</ul>"
    html += "<a href='/posts'>다시 조회</a>"
    return HTMLResponse(content=html)
