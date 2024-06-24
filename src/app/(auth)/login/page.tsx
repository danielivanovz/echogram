import Link from "next/link"
import { cookies } from "next/headers"
import { redirect } from "next/navigation"
import { LoginForm } from "@/components/forms/login"

export default function Login() {
  const sessions = cookies().get("access_token")

  if (sessions) return redirect("/space")

  return (
    <main className="flex min-h-screen flex-col items-center gap-4 bg-background p-4 md:px-24">
      <LoginForm />
      <Link href="/" className="group transition-all duration-1000 ease-in-out">
        &larr; Back
        <span className="block h-0.5 max-w-0 bg-neutral-500 transition-all duration-500 group-hover:max-w-full" />
      </Link>
    </main>
  )
}
