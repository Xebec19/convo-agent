import Link from "next/link";
import { Bot, Eye, LockKeyhole, Mail } from "lucide-react";

export default function LoginPage() {
    return <main className="login-page grid min-h-screen place-items-center bg-app-background p-6">
        <section className="w-full max-w-110 rounded-3xl border border-app-surface/50 bg-app-surface/60 p-10 shadow-glass backdrop-blur-xl"><header className="text-center">
            <div className="mx-auto grid h-14 w-14 place-items-center rounded-xl bg-linear-to-br from-brand-strong to-brand-accent text-primary-foreground"><Bot size={30} /></div><h1 className="mt-6 text-[32px] font-semibold tracking-tight">Convo</h1><p className="mt-2 text-app-muted">Secure access to your enterprise knowledge base.</p></header>
            <form className="mt-10 space-y-6">
                <label className="block font-mono text-[13px]">Email Address<div className="relative mt-2"><Mail className="absolute left-4 top-4 text-app-subtle" size={17} />
                    <input className="h-12 w-full rounded-lg border border-app-surface/60 bg-app-surface/50 pl-12 outline-none" placeholder="name@company.com" type="email" />
                </div></label>
                <label className="block font-mono text-[13px]">Password<div className="relative mt-2"><LockKeyhole className="absolute left-4 top-4 text-app-subtle" size={17} /><input className="h-12 w-full rounded-lg border border-app-surface/60 bg-app-surface/50 pl-12" placeholder="••••••••" type="password" /><Eye className="absolute right-4 top-4 text-app-subtle" size={17} /></div></label>
                <div className="flex justify-between text-sm"><label className="flex gap-3 text-app-muted"><input type="checkbox" />Remember me</label>
                    <a className="font-mono text-[13px] text-brand" href="#">Forgot Password?</a></div>
                <Link className="flex h-12 items-center justify-center rounded-lg bg-brand font-mono text-[13px] text-primary-foreground" href="/chat">Sign In</Link>
            </form>
        </section>
    </main>
}
