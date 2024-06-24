import { createClient } from "@/utils/supabase/server"

export async function getUserByEmail({ email }: { email: string }) {
  const client = createClient()

  const { data, error } = await client.from("users").select("*").eq("email", email).single()

  return {
    user_id: data?.user_id,
    email: data?.email,
    created_on: data?.created_on,
  }
}