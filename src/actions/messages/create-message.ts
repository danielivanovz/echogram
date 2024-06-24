"use server"

import { redirect } from "next/navigation"

import { createClient } from "@/utils/supabase/server"
import { getUserByEmail } from "@/actions/users/get-user-by-email"

type TCreateMessage = {
  title: string
  message: string
  email: string
}

export const createMessage = async ({ message, title, email }: TCreateMessage) => {
  const client = createClient()

  const { user_id } = await getUserByEmail({ email })

  // will calculate these as background jobs
  // const emotion = await getEmotion({ text: message })
  // const sentiment = await getSentiment({ text: message })

  if (!user_id) redirect("/login")

  await client.from("emails").insert({
    user_id: user_id,
    subject: title,
    body: message,
    received_on: new Date().toISOString(),
  })

  redirect(`/${user_id}`)
}
