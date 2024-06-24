import { Timeline } from "@/components/timeline"
import { createClient } from "@/utils/supabase/server"
import Link from "next/link"
import { redirect } from "next/navigation"

type TProps = {
  params: {
    userId: string
  }
}

export default async function Post({ params }: TProps) {
  const supabase = createClient()

  const { data } = await supabase.from("emails").select("*").eq("user_id", params.userId)

  if (!data) return redirect("/")

  return (
    <main className="flex min-h-screen flex-col items-center gap-4 bg-background p-4 md:px-24">
      <div className="w-full">
        <Timeline posts={data} />
      </div>
      <Link href="/" className="group transition-all duration-1000 ease-in-out">
        &larr; Back
        <span className="block h-0.5 max-w-0 bg-neutral-500 transition-all duration-500 group-hover:max-w-full" />
      </Link>
    </main>
  )
}
