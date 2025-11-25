import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const authHeader = request.headers.get('authorization')
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return NextResponse.json(
      { success: false, message: 'No token provided' },
      { status: 401 }
    )
  }

  const token = authHeader.substring(7)

  try {
    // Fetch user info from Naver
    const response = await fetch('https://openapi.naver.com/v1/nid/me', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })

    const data = await response.json()

    if (data.resultcode === '00') {
      return NextResponse.json({
        success: true,
        user: {
          id: data.response.id,
          name: data.response.name,
          email: data.response.email,
          nickname: data.response.nickname,
        },
      })
    } else {
      return NextResponse.json(
        { success: false, message: 'Failed to fetch user info' },
        { status: 400 }
      )
    }
  } catch (error) {
    console.error('Error fetching user info:', error)
    return NextResponse.json(
      { success: false, message: 'Server error' },
      { status: 500 }
    )
  }
}
