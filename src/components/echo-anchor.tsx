import { cn } from "@/lib/utils"
import Link from "next/link"

export const Anchor = ({ userId }) => {
  return (
    <Link
      href={userId}
      prefetch={true}
      className={cn(
        "my-1 ml-6 block text-md transition-colors",
        "hover:animate-pulse",
        "group transition-all duration-1000 ease-in-out",
      )}
    >
      - {userId.slice(0, 23)} &rarr;
      <span className="block h-0.5 max-w-0 bg-neutral-500 transition-all duration-500 group-hover:max-w-full" />
    </Link>
  )
}
