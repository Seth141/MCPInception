import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'MCPInception',
  description: 'MCPInception Application',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="purple-glow" />
        <main className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black relative z-10">
          {children}
        </main>
      </body>
    </html>
  )
}
