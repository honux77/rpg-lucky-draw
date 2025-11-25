import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'RPG Lucky Draw',
  description: '랜덤 뽑기 앱',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body className="font-sans">{children}</body>
    </html>
  )
}
