"use server"
import { env } from "@/env.mjs"

export async function getEmotion({ text }: { text: string }) {
  const _emotion = await fetch(`${env.NEXT_PUBLIC_BACKEND_URL}/analyzer/emotion`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  })

  const emotion = await _emotion.json()

  return emotion.output
}