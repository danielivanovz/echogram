"use server"

import { env } from "@/env.mjs"

export async function signIn({ email }) {
  const response = await fetch(`${env.NEXT_PUBLIC_BACKEND_URL}/auth/magiclink/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email }),
  })

  if (!response.ok) console.log("Error sending magic link email", response.statusText)

  return await response.json()
}
