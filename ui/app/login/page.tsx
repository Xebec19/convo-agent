import { Bot } from "lucide-react";
import Login from "./Login";

export default function LoginPage() {
    return <main className="login-page grid min-h-screen place-items-center bg-app-background p-6">
        <section className="w-full max-w-110 rounded-3xl border border-app-surface/50 bg-app-surface/60 p-10 shadow-glass backdrop-blur-xl"><header className="text-center">
            <div className="mx-auto grid h-14 w-14 place-items-center rounded-xl bg-linear-to-br from-brand-strong to-brand-accent text-primary-foreground"><Bot size={30} /></div><h1 className="mt-6 text-[32px] font-semibold tracking-tight">Convo</h1><p className="mt-2 text-app-muted">Secure access to your enterprise knowledge base.</p></header>
            <Login />
        </section>
    </main>
}
