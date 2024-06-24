"use client"

import { Textarea } from "@/components/ui/textarea"
import { toast } from "@/components/ui/use-toast"
import { cn } from "@/lib/utils"
import { Label } from "@radix-ui/react-dropdown-menu"
import { useEffect, useState } from "react"
import { z } from "zod"

import { zodResolver } from "@hookform/resolvers/zod"

import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"

import { useForm } from "react-hook-form"
import { Input } from "@/components/ui/input"
import { createMessage } from "@/actions/messages/create-message"
import { ReloadIcon } from "@radix-ui/react-icons"

const FormSchema = z.object({
  title: z.string().min(3, {
    message: "Title must be at least 3 characters.",
  }),
  message: z
    .string()
    .min(10, {
      message: "Message must be at least 10 characters.",
    })
    .max(600, {
      message: "Message must not be longer than 30 characters.",
    }),
})

export default function EchoForm({ email }) {
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
  })

  async function onSubmit(data: z.infer<typeof FormSchema>) {
    await createMessage({ ...data, email })

    toast({
      description: "Your Echo has been sent!",
    })
  }

  const [chars, setChars] = useState<string>("")

  const handleCountChars = (event) => {
    console.log("event.target.value: ", event.target.value)
    setChars(event.target.value)
  }

  useEffect(() => {
    if (chars.length > 600) {
      setChars(chars.slice(0, 600))
    }
  }, [chars])

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="w-full space-y-6 px-4 pt-16 md:my-auto md:w-2/3">
        <Label className="self-center">Send a new Echo:</Label>
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem className="flex items-end justify-start space-x-4">
              <FormLabel>Title</FormLabel>
              <FormControl>
                <Input id="title" type="text" className="w-36" required placeholder="What's on your mind?" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="message"
          render={({ field }) => (
            <FormItem className="w-full">
              <FormLabel>Content</FormLabel>
              <FormControl onChange={handleCountChars}>
                <Textarea placeholder="Tell us a little bit about yourself" className="h-52 resize-y" {...field} />
              </FormControl>
              <FormDescription className="flex justify-between space-x-2 text-muted-foreground text-xs">
                <span>You won&apos;t be able to edit or delete this message.</span>
                <span>{chars.length}/600</span>
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <button
          type="submit"
          className={cn(
            "group mt-2 transition-opacity duration-1000 ease-in-out",
            chars.length > 10 ? "opacity-100" : "pointer-events-none opacity-0",
            "flex w-full items-center justify-center space-x-2",
            form.formState.isSubmitting && "pointer-events-none opacity-50",
          )}
        >
          {form.formState.isSubmitting && <ReloadIcon className="h-3 w-3 animate-spin" />}
          <div>
            Submit
            <span className="block h-0.5 max-w-0 bg-neutral-500 transition-all duration-500 group-hover:max-w-full" />
          </div>
        </button>
      </form>
    </Form>
  )
}
