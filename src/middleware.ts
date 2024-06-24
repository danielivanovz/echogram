import { env } from "@/env.mjs"
import { type NextRequest, NextResponse } from "next/server"

import type { Database } from "@/utils/supabase/types"

interface Session {
  user: Database["public"]["Tables"]["users"]["Row"]
  access_token: string
}

const validate = async (token: string): Promise<Session> => {
  const response = await fetch(`${env.NEXT_PUBLIC_BACKEND_URL}/auth/magiclink/validate/${token}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })

  if (!response.ok) console.log("Error validating magic link", response.statusText)

  return await response.json()
}

const COOKIE_CONFIG = {
  path: "/",
  secure: true,
  httpOnly: true,
  expires: new Date(Date.now() + 24 * 60 * 60 * 1000),
}

const updateCookie = (session: Session, response: NextResponse) => {
  response.cookies.set("access_token", session.access_token, COOKIE_CONFIG)
  response.cookies.set("user_email", decodeURIComponent(session.user.email), COOKIE_CONFIG)
  return response
}

export async function middleware(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith("/auth/magiclink/validate/")) {
    const token = request.nextUrl.pathname.split("/").pop() as string
    const session = await validate(token)

    if (!session.access_token) return NextResponse.redirect(new URL("/", request.url))

    const response = NextResponse.redirect(new URL("/space", request.url))
    return updateCookie(session, response)
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)"],
}
