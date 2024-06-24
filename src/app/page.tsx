import { createClient } from "@/utils/supabase/server"

import { EnterIcon, InfoCircledIcon, ReloadIcon } from "@radix-ui/react-icons"
import Link from "next/link"
import { Anchor } from "@/components/echo-anchor"

export default async function Home() {
  const supabase = createClient()
  const { data } = await supabase.from("users").select("*")

  if (!data) return <ReloadIcon className="animate-spin" width={24} height={24} />

  return (
    <main className="flex min-h-screen flex-col items-center gap-4 bg-background p-4 md:px-24">
      <Link className="ml-auto pr-4" href={"/login"}>
        <EnterIcon width={18} height={18} />
      </Link>
      <div className="mb-2 w-fit">
        <div className="flex items-center gap-2">
          <InfoCircledIcon />
          <h1 className="font-bold text-lg">Explore Echoes:</h1>
        </div>
        {shuffle(data).map((user) => (
          <Anchor key={user.user_id} userId={user.user_id} />
        ))}
      </div>
    </main>
  )
}

const shuffle = (arr) => arr.sort(() => Math.random() - 0.5)
