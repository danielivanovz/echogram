"use server"
import { env } from "@/env.mjs"

export async function getSentiment({ text }: { text: string }) {
  const _sentiment = await fetch(`${env.NEXT_PUBLIC_BACKEND_URL}/analyzer/sentiments`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  })

  const sentiment = await _sentiment.json()

  return sentiment.output
}