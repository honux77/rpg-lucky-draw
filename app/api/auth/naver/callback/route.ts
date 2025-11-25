import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const code = searchParams.get('code')
  const state = searchParams.get('state')

  if (!code || !state) {
    return NextResponse.redirect(new URL('/?error=no_code', request.url))
  }

  try {
    // Exchange code for access token
    const tokenResponse = await fetch('https://nid.naver.com/oauth2.0/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        client_id: process.env.NAVER_CLIENT_ID!,
        client_secret: process.env.NAVER_CLIENT_SECRET!,
        code: code,
        state: state,
      }),
    })

    const tokenData = await tokenResponse.json()

    if (tokenData.access_token) {
      // Create an HTML page that will store the token and redirect
      // Using JSON.stringify to properly escape the token value
      const escapedToken = JSON.stringify(tokenData.access_token)
      const html = `
        <!DOCTYPE html>
        <html>
          <head>
            <title>로그인 중...</title>
          </head>
          <body>
            <script>
              localStorage.setItem('naver_token', ${escapedToken});
              window.location.href = '/';
            </script>
            <p>로그인 처리 중...</p>
          </body>
        </html>
      `
      
      return new NextResponse(html, {
        headers: { 'Content-Type': 'text/html' },
      })
    } else {
      return NextResponse.redirect(new URL('/?error=token_failed', request.url))
    }
  } catch (error) {
    console.error('Naver OAuth error:', error)
    return NextResponse.redirect(new URL('/?error=server_error', request.url))
  }
}
