import type { Metadata } from 'next'
import { Inter, Poppins, Space_Grotesk } from 'next/font/google'
import './globals.css'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const poppins = Poppins({ 
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700', '800'],
  variable: '--font-poppins',
  display: 'swap',
})

const spaceGrotesk = Space_Grotesk({ 
  subsets: ['latin'],
  variable: '--font-space-grotesk',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'AI Text Humanizer - Make AI Text Sound Human',
  description: 'Transform AI-generated text into natural, human-like content. Bypass AI detection with advanced paraphrasing technology.',
  keywords: 'AI humanizer, text humanizer, AI detection bypass, paraphrasing, content rewriting',
  openGraph: {
    title: 'AI Text Humanizer',
    description: 'Transform AI-generated text into natural, human-like content',
    type: 'website',
  },
  manifest: '/manifest.json',
  themeColor: '#2563eb',
  viewport: 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'AI Humanizer',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${poppins.variable} ${spaceGrotesk.variable} font-sans`}>{children}</body>
    </html>
  )
}
