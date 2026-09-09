'use client'

import { Eye, LockKeyhole, Mail } from "lucide-react";
import { authenticate } from "./actions";
import { useActionState } from "react";
import { Button } from "@/components/ui/button";

export default function Login() {

    const [errorMessage, action, isPending] = useActionState(authenticate, undefined)

    if (errorMessage) {
        console.log({ errorMessage })
    }

    return <form className="mt-10 space-y-6" action={action}>
        <label className="block font-mono text-[13px]" htmlFor="email">Email Address<div className="relative mt-2"><Mail className="absolute left-4 top-4 text-app-subtle" size={17} />
            <input className="h-12 w-full rounded-lg border border-app-surface/60 bg-app-surface/50 pl-12 outline-none" placeholder="name@company.com" type="email" autoComplete="email" name="email" required />
        </div></label>
        <label className="block font-mono text-[13px]" htmlFor="password">Password<div className="relative mt-2"><LockKeyhole className="absolute left-4 top-4 text-app-subtle" size={17} />
            <input className="h-12 w-full rounded-lg border border-app-surface/60 bg-app-surface/50 pl-12" placeholder="••••••••" type="password" autoComplete="current-password" name="password" minLength={8} /><Eye className="absolute right-4 top-4 text-app-subtle" size={17} />
        </div></label>
        <div className="flex justify-between text-sm"><label className="flex gap-3 text-app-muted"><input type="checkbox" />Remember me</label>
            <a className="font-mono text-[13px] text-brand" href="#">Forgot Password?</a></div>
        <Button type="submit" className="flex h-12 w-full items-center justify-center rounded-lg bg-brand font-mono text-[13px] text-primary-foreground" disabled={isPending}>Sign In</Button>
    </form>
}