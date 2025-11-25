# RPG Lucky Draw

랜덤 뽑기 앱 - Next.js + Tailwind CSS + Naver Login

## 기능

- 네이버 로그인 (OAuth 2.0)
- 네이버 카페 게시글 읽기
- Vercel 배포 지원

## 시작하기

### 1. 패키지 설치

```bash
npm install
```

### 2. 환경 변수 설정

`.env.local` 파일을 생성하고 네이버 개발자 센터에서 발급받은 Client ID와 Client Secret을 입력하세요:

```env
NAVER_CLIENT_ID=your_naver_client_id_here
NAVER_CLIENT_SECRET=your_naver_client_secret_here
NEXT_PUBLIC_NAVER_CLIENT_ID=your_naver_client_id_here
NEXT_PUBLIC_NAVER_REDIRECT_URI=http://localhost:3000/api/auth/naver/callback
```

네이버 개발자 센터: https://developers.naver.com/apps/#/register

### 3. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000)을 열어 앱을 확인하세요.

### 4. 빌드

```bash
npm run build
npm start
```

## Vercel 배포

### 1. Vercel CLI 설치 (선택사항)

```bash
npm install -g vercel
```

### 2. Vercel에 배포

```bash
vercel
```

또는 GitHub 저장소를 Vercel에 연결하면 자동으로 배포됩니다.

### 3. 환경 변수 설정

Vercel 대시보드에서 다음 환경 변수를 설정하세요:

- `NAVER_CLIENT_ID`
- `NAVER_CLIENT_SECRET`
- `NEXT_PUBLIC_NAVER_CLIENT_ID`
- `NEXT_PUBLIC_NAVER_REDIRECT_URI` (예: https://your-app.vercel.app/api/auth/naver/callback)

## 기술 스택

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **Authentication**: Naver OAuth 2.0
- **Deployment**: Vercel

## 네이버 카페 API 참고사항

현재 카페 게시글 읽기 기능은 샘플 데이터를 반환합니다. 실제 네이버 카페 API를 사용하려면:

1. 네이버 개발자 센터에서 카페 API 권한 신청
2. API 엔드포인트: `https://openapi.naver.com/v1/cafe/`
3. 인증 방식: OAuth 2.0 토큰 사용

자세한 내용은 [네이버 카페 API 문서](https://developers.naver.com/docs/login/cafe-api/)를 참고하세요.
