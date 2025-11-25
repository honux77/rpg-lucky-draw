# Architecture Overview

## Project Structure

```
rpg-lucky-draw/
├── app/                          # Next.js App Router
│   ├── api/                      # Backend API Routes
│   │   ├── auth/
│   │   │   └── naver/
│   │   │       ├── callback/     # OAuth callback handler
│   │   │       │   └── route.ts
│   │   │       └── user/         # User info endpoint
│   │   │           └── route.ts
│   │   └── cafe/
│   │       └── posts/            # Cafe posts endpoint
│   │           └── route.ts
│   ├── globals.css               # Tailwind CSS imports
│   ├── layout.tsx                # Root layout component
│   └── page.tsx                  # Home page (main UI)
├── docs/                         # Documentation
│   ├── API.md                    # API documentation
│   ├── FEATURES.md               # Feature list
│   └── SETUP.md                  # Setup guide
├── .env.example                  # Environment template
├── .env.local                    # Local environment (not in git)
├── .eslintrc.json                # ESLint configuration
├── .gitignore                    # Git ignore rules
├── next.config.js                # Next.js configuration
├── package.json                  # NPM dependencies
├── postcss.config.js             # PostCSS configuration
├── tailwind.config.ts            # Tailwind CSS configuration
├── tsconfig.json                 # TypeScript configuration
├── vercel.json                   # Vercel deployment config
└── README.md                     # Main documentation
```

## Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript (target: ES2017)
- **Styling**: Tailwind CSS 3.4
- **UI Library**: React 18

### Backend
- **API**: Next.js API Routes
- **Runtime**: Node.js 20+
- **HTTP**: Native Fetch API

### Authentication
- **Provider**: Naver OAuth 2.0
- **Token Storage**: localStorage (client-side)
- **Security**: CSRF protection via state parameter

### Deployment
- **Platform**: Vercel
- **CI/CD**: Automatic deployment on push
- **Region**: ICN1 (Seoul)

## Data Flow

### 1. Authentication Flow

```
User clicks "네이버 로그인"
    ↓
Redirect to Naver OAuth
    ↓
User authorizes app
    ↓
Naver redirects to /api/auth/naver/callback?code=...
    ↓
Backend exchanges code for access token
    ↓
HTML page stores token in localStorage
    ↓
Redirect to home page
    ↓
Frontend fetches user info with token
    ↓
Display user information
```

### 2. Cafe Posts Flow (Current Implementation)

```
User enters cafe URL
    ↓
Click "불러오기" button
    ↓
POST /api/cafe/posts with token
    ↓
Backend validates token
    ↓
Return mock data (sample posts)
    ↓
Display posts in UI
```

### 3. Cafe Posts Flow (Future Implementation)

```
User enters cafe URL
    ↓
Click "불러오기" button
    ↓
POST /api/cafe/posts with token
    ↓
Backend validates token
    ↓
Backend calls Naver Cafe API
    ↓
Parse and format response
    ↓
Return real cafe posts
    ↓
Display posts in UI
```

## API Endpoints

### Authentication

**GET /api/auth/naver/callback**
- Purpose: OAuth callback handler
- Input: code, state (query params)
- Output: HTML with token storage script
- Auth: None (public)

**GET /api/auth/naver/user**
- Purpose: Get current user info
- Input: Bearer token (header)
- Output: User profile JSON
- Auth: Required

### Cafe

**POST /api/cafe/posts**
- Purpose: Get cafe posts
- Input: Bearer token (header), cafeUrl (body)
- Output: Posts array JSON
- Auth: Required

## Security Features

### 1. Environment Variables
- Secrets kept in `.env.local` (gitignored)
- Server-only vars: `NAVER_CLIENT_SECRET`
- Client vars: `NEXT_PUBLIC_*`

### 2. Authentication
- OAuth 2.0 standard flow
- CSRF protection via state parameter
- Token-based API authentication
- XSS-safe token storage (JSON.stringify)

### 3. API Security
- Bearer token validation
- Request body validation
- Error handling without info leakage

## Type Safety

### TypeScript Interfaces

```typescript
// User information
interface UserInfo {
  id: string
  name: string
  email: string
  nickname?: string
}

// Cafe post
interface CafePost {
  title: string
  author: string
  date: string
  content: string
}
```

## Build Process

1. **Development**: `npm run dev`
   - Starts dev server on port 3000
   - Hot module replacement
   - Fast refresh

2. **Production Build**: `npm run build`
   - TypeScript compilation
   - Static page generation
   - Code optimization
   - Tree shaking

3. **Linting**: `npm run lint`
   - ESLint checks
   - Next.js specific rules

## Deployment Strategy

### Vercel Automatic Deployment

1. **Push to main branch**
   - Triggers production build
   - Deploys to production URL
   - Updates live site

2. **Create pull request**
   - Creates preview deployment
   - Unique preview URL
   - Test before merging

3. **Environment variables**
   - Set in Vercel dashboard
   - Available during build and runtime
   - Secure storage

## Performance Optimizations

1. **Static Generation**
   - Home page pre-rendered
   - Fast initial load

2. **Code Splitting**
   - Automatic by Next.js
   - Load only needed code

3. **Tree Shaking**
   - Remove unused code
   - Smaller bundle size

4. **Image Optimization**
   - Next.js Image component ready
   - Automatic format conversion
   - Lazy loading

## Future Enhancements

### Phase 1: Real Cafe API Integration
- Apply for Naver Cafe API access
- Implement real API calls
- Add pagination
- Add filtering/sorting

### Phase 2: Database Integration
- Add PostgreSQL/Supabase
- Store events and results
- User preferences

### Phase 3: Random Draw Feature
- Select random winners from posts
- Exclude duplicates
- Export results

### Phase 4: Admin Dashboard
- Event management
- Statistics and analytics
- Winner history

## Development Guidelines

1. **Type Safety**: Always use TypeScript types, avoid `any`
2. **Security**: Never commit secrets, use environment variables
3. **Styling**: Use Tailwind utilities consistently
4. **Components**: Keep components small and focused
5. **API Routes**: Validate inputs, handle errors properly
6. **Testing**: Build and lint before committing

## Environment Configuration

### Development
```env
NAVER_CLIENT_ID=your_dev_client_id
NAVER_CLIENT_SECRET=your_dev_secret
NEXT_PUBLIC_NAVER_CLIENT_ID=your_dev_client_id
NEXT_PUBLIC_NAVER_REDIRECT_URI=http://localhost:3000/api/auth/naver/callback
```

### Production
```env
NAVER_CLIENT_ID=your_prod_client_id
NAVER_CLIENT_SECRET=your_prod_secret
NEXT_PUBLIC_NAVER_CLIENT_ID=your_prod_client_id
NEXT_PUBLIC_NAVER_REDIRECT_URI=https://your-app.vercel.app/api/auth/naver/callback
```

## Troubleshooting

### Build Failures
- Check TypeScript errors
- Verify all imports exist
- Ensure environment variables are set

### Authentication Issues
- Verify callback URL in Naver console
- Check Client ID/Secret
- Inspect browser console for errors

### Deployment Issues
- Check Vercel build logs
- Verify environment variables in Vercel
- Test build locally first

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Naver Developers](https://developers.naver.com)
- [Tailwind CSS](https://tailwindcss.com)
- [Vercel Platform](https://vercel.com)
