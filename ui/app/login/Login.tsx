'use client'

import Link from "next/link"
import { Eye, LockKeyhole, Mail } from "lucide-react";
import { authenticate } from "./actions";
import { useActionState } from "react";

export default function Login() {

    const [errorMessage, formAction, isPending] = useActionState(authenticate, undefined)

    return <form className="mt-10 space-y-6" action={formAction}>
        <label className="block font-mono text-[13px]">Email Address<div className="relative mt-2"><Mail className="absolute left-4 top-4 text-app-subtle" size={17} />
            <input className="h-12 w-full rounded-lg border border-app-surface/60 bg-app-surface/50 pl-12 outline-none" placeholder="name@company.com" type="email" />
        </div></label>
        <label className="block font-mono text-[13px]">Password<div className="relative mt-2"><LockKeyhole className="absolute left-4 top-4 text-app-subtle" size={17} /><input className="h-12 w-full rounded-lg border border-app-surface/60 bg-app-surface/50 pl-12" placeholder="••••••••" type="password" /><Eye className="absolute right-4 top-4 text-app-subtle" size={17} /></div></label>
        <div className="flex justify-between text-sm"><label className="flex gap-3 text-app-muted"><input type="checkbox" />Remember me</label>
            <a className="font-mono text-[13px] text-brand" href="#">Forgot Password?</a></div>
        <Link className="flex h-12 items-center justify-center rounded-lg bg-brand font-mono text-[13px] text-primary-foreground" href="/chat">Sign In</Link>
    </form>
}