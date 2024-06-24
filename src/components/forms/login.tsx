"use client"

import { signIn } from "@/actions/auth/sign-in"
import { Form, FormControl, FormField, FormItem, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { cn } from "@/lib/utils"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"

const FormSchema = z.object({
  email: z.string().email(),
})

export const LoginForm = () => {
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
  })

  async function onSubmit(data: z.infer<typeof FormSchema>) {
    await signIn({ email: data.email })
  }

  return (
    <div className="my-auto w-fit space-y-4">
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col items-center justify-center space-y-4">
          <Label className="self-center text-md">Insert your email:</Label>
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem className="flex items-end justify-start space-x-4">
                <FormControl>
                  <Input
                    id="email"
                    type="email"
                    className="w-52 border-b text-center text-md outline-none"
                    required
                    placeholder="name@example.com"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <button
            className={cn(
              "group transition-all duration-1000 ease-in-out",
              (form.formState.isSubmitting || form.formState.isSubmitted) && "pointer-events-none",
            )}
            type="submit"
          >
            {getLabel(form.formState)}
            <span className="block h-0.5 max-w-0 bg-neutral-500 transition-all duration-500 group-hover:max-w-full" />
          </button>
        </form>
      </Form>
    </div>
  )
}

const getLabel = (formState) => {
  if (formState.isSubmitted)
    return "Sent! Check your email for a link to sign in. If it doesn't appear, check your spam folder."

  if (formState.isSubmitting) return "Sending..."

  return "Send"
}
