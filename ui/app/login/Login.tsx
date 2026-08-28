'use client'

import { Eye, LockKeyhole, Mail } from "lucide-react";
import { authenticate } from "./actions";
import { useActionState } from "react";
import { Button } from "@/components/ui/button";
import z from "zod";
import { Controller, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { AuthSchema } from "./schema";

export default function Login() {

    const {
        handleSubmit,
        control,
        formState: { errors }
    } = useForm<z.infer<typeof AuthSchema>>({
        defaultValues: {
            email: "",
            password: ""
        },
        resolver: zodResolver(AuthSchema)
    })

    const [errorMessage, action, isPending] = useActionState(authenticate, undefined)

    if (errorMessage) {
        console.log({ errorMessage })
    }

    return <form className="mt-10 space-y-6" onSubmit={handleSubmit(action)}>
        <label className="block font-mono text-[13px]" htmlFor="email">Email Address<div className="relative mt-2"><Mail className="absolute left-4 top-4 text-app-subtle" size={17} />
            <Controller name="email" control={control} render={({ field }) => <Input className="h-12 w-full rounded-lg border border-app-surface/60 bg-app-surface/50 pl-12 outline-none" placeholder="name@company.com" type="email" autoComplete="email" name="email" value={field.value} onChange={(e) => field.onChange(e.target.value)} />} />
            <span className={cn(errors.email ? "" : "hidden", "text-xs text-destructive")}>{errors.email?.message}</span>
        </div></label>
        <label className="block font-mono text-[13px]" htmlFor="password">Password<div className="relative mt-2"><LockKeyhole className="absolute left-4 top-4 text-app-subtle" size={17} />
            <Controller name="password" control={control} render={({ field }) => <><Input {...field} className="h-12 w-full rounded-lg border border-app-surface/60 bg-app-surface/50 pl-12" placeholder="••••••••" type="password" autoComplete="current-password" value={field.value} onChange={(e) => field.onChange(e.target.value)} /><Eye className="absolute right-4 top-4 text-app-subtle" size={17} /></>} />
            <span className={cn(errors.password ? "" : "hidden", "text-xs text-destructive")}>{errors.password?.message}</span>
        </div></label>
        <div className="flex justify-between text-sm"><label className="flex gap-3 text-app-muted"><input type="checkbox" />Remember me</label>
            <a className="font-mono text-[13px] text-brand" href="#">Forgot Password?</a></div>
        <Button type="submit" className="flex h-12 w-full items-center justify-center rounded-lg bg-brand font-mono text-[13px] text-primary-foreground" disabled={isPending}>Sign In</Button>
    </form>
}