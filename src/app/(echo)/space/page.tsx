import EchoForm from "@/components/forms/echo"
import { cookies } from "next/headers"
import Link from "next/link"

export default function Space() {
  const email_kv = cookies().get("user_email")

  return (
    <main className="flex min-h-screen flex-col items-center gap-4 bg-background p-4 md:px-24">
      <EchoForm email={email_kv?.value} />
      <Link href="/" className="group transition-all duration-1000 ease-in-out">
        &larr; Back
        <span className="block h-0.5 max-w-0 bg-neutral-500 transition-all duration-500 group-hover:max-w-full" />
      </Link>
    </main>
  )
}
