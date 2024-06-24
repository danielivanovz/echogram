import type { SupabaseClient } from "@supabase/supabase-js"
import type { Database } from "./types"

export type Client = SupabaseClient<Database>
