import type { Metadata } from "next"
import { Cormorant_Garamond } from "next/font/google"
import "./globals.css"
import { Toaster } from "@/components/ui/toaster"

const garamond = Cormorant_Garamond({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
})

export const metadata: Metadata = {
  title: "Echogram",
  description: "Your email, your way.",
}

export const viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: 1,
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={garamond.className}>{children}
        <Toaster />
      </body>
    </html>
  )
}
