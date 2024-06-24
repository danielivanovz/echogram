import type { Database } from "@/utils/supabase/types"

export type TPost = Database["public"]["Tables"]["emails"]["Row"]
