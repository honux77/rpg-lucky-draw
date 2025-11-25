'use client'

import { useState, useEffect } from 'react'

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [userInfo, setUserInfo] = useState<any>(null)
  const [cafePosts, setCafePosts] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [cafeUrl, setCafeUrl] = useState('')

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('naver_token')
    if (token) {
      setIsLoggedIn(true)
      fetchUserInfo(token)
    }
  }, [])

  const handleNaverLogin = () => {
    const clientId = process.env.NEXT_PUBLIC_NAVER_CLIENT_ID
    const redirectUri = encodeURIComponent(process.env.NEXT_PUBLIC_NAVER_REDIRECT_URI || window.location.origin + '/api/auth/naver/callback')
    const state = Math.random().toString(36).substring(7)
    localStorage.setItem('naver_state', state)
    
    const naverAuthUrl = `https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&state=${state}`
    window.location.href = naverAuthUrl
  }

  const fetchUserInfo = async (token: string) => {
    try {
      const response = await fetch('/api/auth/naver/user', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      const data = await response.json()
      if (data.success) {
        setUserInfo(data.user)
      }
    } catch (error) {
      console.error('Failed to fetch user info:', error)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('naver_token')
    setIsLoggedIn(false)
    setUserInfo(null)
    setCafePosts([])
  }

  const fetchCafePosts = async () => {
    if (!cafeUrl) {
      alert('카페 URL을 입력해주세요')
      return
    }

    setLoading(true)
    try {
      const token = localStorage.getItem('naver_token')
      const response = await fetch('/api/cafe/posts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ cafeUrl })
      })
      const data = await response.json()
      if (data.success) {
        setCafePosts(data.posts)
      } else {
        alert(data.message || '게시글을 불러오는데 실패했습니다')
      }
    } catch (error) {
      console.error('Failed to fetch cafe posts:', error)
      alert('게시글을 불러오는데 실패했습니다')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold text-center mb-8">
          RPG Lucky Draw
        </h1>
        <p className="text-center mb-8 text-lg">
          랜덤 뽑기 앱
        </p>

        {!isLoggedIn ? (
          <div className="flex flex-col items-center space-y-4">
            <button
              onClick={handleNaverLogin}
              className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
            >
              네이버 로그인
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            {userInfo && (
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
                <h2 className="text-2xl font-bold mb-4">사용자 정보</h2>
                <p>이름: {userInfo.name}</p>
                <p>이메일: {userInfo.email}</p>
                <button
                  onClick={handleLogout}
                  className="mt-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
                >
                  로그아웃
                </button>
              </div>
            )}

            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
              <h2 className="text-2xl font-bold mb-4">카페 게시글 읽기</h2>
              <div className="flex space-x-2 mb-4">
                <input
                  type="text"
                  value={cafeUrl}
                  onChange={(e) => setCafeUrl(e.target.value)}
                  placeholder="카페 URL 입력 (예: cafe.naver.com/cafeId)"
                  className="flex-1 px-4 py-2 border rounded text-black dark:text-white dark:bg-gray-700"
                />
                <button
                  onClick={fetchCafePosts}
                  disabled={loading}
                  className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors disabled:bg-gray-400"
                >
                  {loading ? '로딩 중...' : '불러오기'}
                </button>
              </div>

              {cafePosts.length > 0 && (
                <div className="space-y-2">
                  <h3 className="font-bold text-lg">게시글 목록</h3>
                  <ul className="space-y-2">
                    {cafePosts.map((post, index) => (
                      <li key={index} className="p-3 bg-gray-100 dark:bg-gray-700 rounded">
                        <h4 className="font-semibold">{post.title}</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          작성자: {post.author} | 날짜: {post.date}
                        </p>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </main>
  )
}
