# 설치 및 설정 가이드

## 1. 네이버 개발자 센터 설정

### 1.1 애플리케이션 등록

1. [네이버 개발자 센터](https://developers.naver.com/apps/#/register)에 접속
2. "애플리케이션 등록" 클릭
3. 다음 정보를 입력:
   - 애플리케이션 이름: RPG Lucky Draw (또는 원하는 이름)
   - 사용 API: 네이버 로그인
   - 제공 정보: 이메일, 이름 (필요한 정보 선택)

### 1.2 Callback URL 설정

개발 환경:
```
http://localhost:3000/api/auth/naver/callback
```

프로덕션 환경:
```
https://your-domain.vercel.app/api/auth/naver/callback
```

### 1.3 Client ID 및 Client Secret 확인

- 등록 후 발급되는 Client ID와 Client Secret을 안전하게 보관

## 2. 로컬 개발 환경 설정

### 2.1 저장소 클론

```bash
git clone https://github.com/honux77/rpg-lucky-draw.git
cd rpg-lucky-draw
```

### 2.2 의존성 설치

```bash
npm install
```

### 2.3 환경 변수 설정

`.env.local` 파일을 생성하고 다음 내용을 입력:

```env
# 네이버 개발자 센터에서 발급받은 정보
NAVER_CLIENT_ID=your_client_id_here
NAVER_CLIENT_SECRET=your_client_secret_here

# 브라우저에서 접근 가능한 환경 변수
NEXT_PUBLIC_NAVER_CLIENT_ID=your_client_id_here
NEXT_PUBLIC_NAVER_REDIRECT_URI=http://localhost:3000/api/auth/naver/callback
```

⚠️ **주의**: `.env.local` 파일은 절대 Git에 커밋하지 마세요!

### 2.4 개발 서버 실행

```bash
npm run dev
```

브라우저에서 http://localhost:3000 접속

## 3. Vercel 배포

### 3.1 Vercel 계정 생성

1. [Vercel](https://vercel.com)에 접속하여 계정 생성 (GitHub 계정으로 로그인 권장)

### 3.2 프로젝트 가져오기

1. Vercel 대시보드에서 "Add New Project" 클릭
2. GitHub 저장소 연결
3. "rpg-lucky-draw" 저장소 선택
4. "Import" 클릭

### 3.3 환경 변수 설정

Vercel 프로젝트 설정에서 다음 환경 변수를 추가:

| 변수 이름 | 값 |
|----------|-----|
| `NAVER_CLIENT_ID` | 네이버 Client ID |
| `NAVER_CLIENT_SECRET` | 네이버 Client Secret |
| `NEXT_PUBLIC_NAVER_CLIENT_ID` | 네이버 Client ID (동일) |
| `NEXT_PUBLIC_NAVER_REDIRECT_URI` | `https://your-app.vercel.app/api/auth/naver/callback` |

### 3.4 배포

1. "Deploy" 클릭
2. 배포 완료 후 생성된 URL 확인
3. 네이버 개발자 센터에서 해당 URL을 Callback URL에 추가

### 3.5 자동 배포 설정

- main 브랜치에 push하면 자동으로 프로덕션 배포
- PR 생성 시 자동으로 프리뷰 환경 생성

## 4. 네이버 카페 API 설정 (선택사항)

현재 구현은 샘플 데이터를 반환합니다. 실제 카페 API를 사용하려면:

### 4.1 카페 API 권한 신청

1. 네이버 개발자 센터에서 카페 API 사용 신청
2. 카페 관리자 권한 필요
3. API 사용 승인 대기 (영업일 기준 3-5일 소요)

### 4.2 API 엔드포인트

- 게시글 목록: `GET https://openapi.naver.com/v1/cafe/{cafeId}/articles`
- 게시글 상세: `GET https://openapi.naver.com/v1/cafe/{cafeId}/articles/{articleId}`

### 4.3 구현 업데이트

`app/api/cafe/posts/route.ts` 파일의 mock 데이터를 실제 API 호출로 교체:

```typescript
const response = await axios.get(
  `https://openapi.naver.com/v1/cafe/${cafeId}/articles`,
  {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  }
)
```

자세한 내용은 [네이버 카페 API 문서](https://developers.naver.com/docs/login/cafe-api/)를 참고하세요.

## 5. 문제 해결

### 로그인이 안 돼요

1. Client ID와 Client Secret이 올바른지 확인
2. Callback URL이 정확히 설정되었는지 확인
3. 브라우저 콘솔에서 오류 메시지 확인

### 빌드가 실패해요

```bash
npm run build
```

실행 후 오류 메시지를 확인하고:
- 패키지 버전 충돌 확인
- TypeScript 에러 수정
- 환경 변수 설정 확인

### Vercel 배포가 안 돼요

1. 빌드 로그에서 오류 확인
2. 환경 변수가 모두 설정되었는지 확인
3. 네이버 개발자 센터의 Callback URL에 Vercel 도메인이 추가되었는지 확인

## 6. 추가 리소스

- [Next.js 문서](https://nextjs.org/docs)
- [Tailwind CSS 문서](https://tailwindcss.com/docs)
- [네이버 로그인 API](https://developers.naver.com/docs/login/api/)
- [Vercel 문서](https://vercel.com/docs)
