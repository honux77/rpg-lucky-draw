# API 문서

## 인증 API

### 1. 네이버 로그인 콜백

**Endpoint**: `GET /api/auth/naver/callback`

네이버 OAuth 인증 후 리다이렉트되는 콜백 엔드포인트입니다.

**Parameters**:
- `code` (query string): OAuth 인증 코드
- `state` (query string): CSRF 방지용 상태 값

**Response**:
- 성공 시: HTML 페이지 (토큰을 localStorage에 저장 후 메인 페이지로 리다이렉트)
- 실패 시: 에러 파라미터와 함께 메인 페이지로 리다이렉트

**Example**:
```
GET /api/auth/naver/callback?code=ABC123&state=random_state
```

### 2. 사용자 정보 조회

**Endpoint**: `GET /api/auth/naver/user`

네이버 API를 통해 현재 로그인한 사용자의 정보를 조회합니다.

**Headers**:
- `Authorization: Bearer {access_token}`

**Response**:
```json
{
  "success": true,
  "user": {
    "id": "naver_user_id",
    "name": "홍길동",
    "email": "user@example.com",
    "nickname": "닉네임"
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "message": "No token provided"
}
```

**Status Codes**:
- 200: 성공
- 401: 인증 토큰 없음
- 400: 사용자 정보 조회 실패
- 500: 서버 오류

## 카페 API

### 3. 카페 게시글 목록 조회

**Endpoint**: `POST /api/cafe/posts`

네이버 카페의 게시글 목록을 조회합니다.

**Headers**:
- `Authorization: Bearer {access_token}`
- `Content-Type: application/json`

**Request Body**:
```json
{
  "cafeUrl": "cafe.naver.com/cafeId"
}
```

**Response**:
```json
{
  "success": true,
  "posts": [
    {
      "title": "게시글 제목",
      "author": "작성자",
      "date": "2024-01-01",
      "content": "게시글 내용"
    }
  ],
  "message": "실제 구현을 위해서는 네이버 카페 API 권한이 필요합니다. 현재는 샘플 데이터입니다."
}
```

**Error Response**:
```json
{
  "success": false,
  "message": "Cafe URL is required"
}
```

**Status Codes**:
- 200: 성공
- 400: 잘못된 요청 (카페 URL 누락 또는 형식 오류)
- 401: 인증 토큰 없음
- 500: 서버 오류

**참고사항**:
현재 버전은 샘플 데이터를 반환합니다. 실제 네이버 카페 API를 사용하려면:
1. 네이버 개발자 센터에서 카페 API 권한 신청
2. 카페 관리자 권한 획득
3. `app/api/cafe/posts/route.ts` 파일에서 실제 API 호출 코드로 교체

## 에러 처리

모든 API는 다음과 같은 형식의 에러를 반환합니다:

```json
{
  "success": false,
  "message": "에러 메시지"
}
```

### 공통 에러 코드

- **401 Unauthorized**: 인증 토큰이 없거나 유효하지 않음
- **400 Bad Request**: 잘못된 요청 파라미터
- **500 Internal Server Error**: 서버 내부 오류

## 보안

### 토큰 관리

- 액세스 토큰은 클라이언트의 localStorage에 저장됩니다
- 모든 API 요청에는 `Authorization: Bearer {token}` 헤더가 필요합니다
- 토큰 만료 시 재로그인이 필요합니다

### CORS

Next.js API Routes는 기본적으로 동일 출처에서만 접근 가능합니다.

### 환경 변수

민감한 정보는 반드시 환경 변수로 관리하고, 클라이언트에 노출되지 않도록 주의합니다:

- `NAVER_CLIENT_SECRET`: 서버에서만 사용 (절대 클라이언트 노출 금지)
- `NEXT_PUBLIC_NAVER_CLIENT_ID`: 클라이언트에서 사용 가능

## Rate Limiting

네이버 API는 다음과 같은 호출 제한이 있습니다:
- 로그인 API: 일 25,000회
- 카페 API: 별도 협의 필요

자세한 내용은 [네이버 개발자 센터](https://developers.naver.com)를 참고하세요.
