# Quick Start Guide

빠르게 시작하기 위한 가이드입니다.

## 5분 만에 시작하기

### 1. 네이버 개발자 센터 설정 (2분)

1. https://developers.naver.com/apps/#/register 접속
2. 애플리케이션 등록
   - 이름: 아무거나 입력
   - 사용 API: "네이버 로그인" 선택
   - 제공 정보: 이메일, 이름 선택
   - 서비스 URL: http://localhost:3000
   - Callback URL: **http://localhost:3000/api/auth/naver/callback** (정확히 입력!)
3. Client ID와 Client Secret 복사

### 2. 프로젝트 설치 (2분)

```bash
# 저장소 클론
git clone https://github.com/honux77/rpg-lucky-draw.git
cd rpg-lucky-draw

# 패키지 설치
npm install

# 환경 변수 설정
cp .env.example .env.local
```

### 3. 환경 변수 입력 (1분)

`.env.local` 파일을 열고 Client ID와 Secret을 입력하세요:

```env
NAVER_CLIENT_ID=여기에_Client_ID_붙여넣기
NAVER_CLIENT_SECRET=여기에_Client_Secret_붙여넣기
NEXT_PUBLIC_NAVER_CLIENT_ID=여기에_Client_ID_다시_붙여넣기
NEXT_PUBLIC_NAVER_REDIRECT_URI=http://localhost:3000/api/auth/naver/callback
```

### 4. 실행! (30초)

```bash
npm run dev
```

브라우저에서 http://localhost:3000 접속!

## 주요 기능

### ✅ 네이버 로그인
1. "네이버 로그인" 버튼 클릭
2. 네이버 계정으로 로그인
3. 권한 동의
4. 자동으로 앱에 로그인됨

### ✅ 사용자 정보 표시
로그인 후 이름, 이메일이 자동으로 표시됩니다.

### ⚠️ 카페 게시글 읽기 (샘플 데이터)
- 카페 URL을 입력하면 샘플 데이터가 표시됩니다
- 실제 카페 API 연동은 네이버 승인이 필요합니다

## Vercel 배포 (5분)

### 방법 1: GitHub 연동 (추천)

1. https://vercel.com 접속 및 로그인
2. "Add New Project" 클릭
3. GitHub 저장소 선택
4. Environment Variables 추가:
   - `NAVER_CLIENT_ID`
   - `NAVER_CLIENT_SECRET`
   - `NEXT_PUBLIC_NAVER_CLIENT_ID`
   - `NEXT_PUBLIC_NAVER_REDIRECT_URI` (https://your-app.vercel.app/api/auth/naver/callback)
5. Deploy 클릭!

⚠️ **중요**: 배포 후 생성된 URL을 네이버 개발자 센터의 Callback URL에 추가하세요!

### 방법 2: CLI

```bash
npm install -g vercel
vercel
```

## 문제 해결

### Q: 로그인이 안 돼요
A: 
1. Callback URL이 정확한지 확인 (끝에 `/` 없어야 함)
2. Client ID/Secret이 올바른지 확인
3. 브라우저 콘솔에서 에러 확인

### Q: 빌드가 안 돼요
A:
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Q: "Cannot find module" 에러
A:
```bash
npm install
```

### Q: Vercel에서 환경 변수가 안 먹혀요
A:
1. Vercel 대시보드 → Settings → Environment Variables 확인
2. 변수 추가 후 "Redeploy" 필요
3. `NEXT_PUBLIC_` 접두사 확인

## 다음 단계

1. [SETUP.md](docs/SETUP.md) - 상세 설정 가이드
2. [API.md](docs/API.md) - API 문서
3. [FEATURES.md](docs/FEATURES.md) - 전체 기능 목록
4. [ARCHITECTURE.md](ARCHITECTURE.md) - 아키텍처 설명

## 도움이 필요하신가요?

- Issue 생성: https://github.com/honux77/rpg-lucky-draw/issues
- 네이버 개발자 센터: https://developers.naver.com

## 체크리스트

로컬 실행:
- [ ] 네이버 개발자 센터에 앱 등록
- [ ] Client ID/Secret 복사
- [ ] 저장소 클론
- [ ] npm install 실행
- [ ] .env.local 파일 생성 및 값 입력
- [ ] npm run dev 실행
- [ ] http://localhost:3000 접속
- [ ] 네이버 로그인 테스트

Vercel 배포:
- [ ] Vercel 계정 생성
- [ ] GitHub 저장소 연동
- [ ] 환경 변수 입력 (4개)
- [ ] Deploy 클릭
- [ ] 배포된 URL 확인
- [ ] 네이버 개발자 센터에 프로덕션 Callback URL 추가
- [ ] 프로덕션에서 로그인 테스트

축하합니다! 🎉 이제 RPG Lucky Draw를 사용할 수 있습니다!
