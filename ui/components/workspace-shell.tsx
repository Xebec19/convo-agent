import Link from "next/link";
import { BookOpen, Bot, HelpCircle, LogOut, MessageSquare, Plus, Settings } from "lucide-react";

export function WorkspaceShell({ active, children }: { active: "chat" | "knowledge"; children: React.ReactNode }) {
  const items = [
    { key: "chat", href: "/chat", label: "Chat", Icon: MessageSquare },
    { key: "knowledge", href: "/knowledge-base", label: "Knowledge Base", Icon: BookOpen },
    { key: "settings", href: "#", label: "Settings", Icon: Settings },
  ];
  return <div className="min-h-screen bg-app-background text-app-foreground md:flex">
    <aside className="flex w-full shrink-0 flex-col border-b border-app-border-strong bg-white/75 p-6 backdrop-blur md:sticky md:top-0 md:h-screen md:w-[280px] md:border-b-0 md:border-r">
      <div className="flex items-center gap-4"><div className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-brand-accent to-brand text-primary-foreground"><Bot size={20} /></div><div><b className="text-xl">Enterprise RAG</b><p className="text-sm text-app-subtle">Workspace</p></div></div>
      <nav className="mt-10 flex gap-2 md:flex-col">{items.map(({ key, href, label, Icon }) => <Link key={key} href={href} className={`flex items-center gap-4 rounded-xl px-4 py-3 ${active === key ? "bg-app-surface-muted text-brand" : "text-app-muted"}`}><Icon size={18} /><span>{label}</span></Link>)}</nav>
      <Link href="/knowledge-base" className="mt-6 flex items-center justify-center gap-2 rounded-xl bg-brand py-3 font-mono text-[13px] text-primary-foreground md:mt-auto"><Plus size={15} />Upload Documents</Link>
      <div className="mt-6 flex gap-5 text-sm text-app-subtle"><HelpCircle size={18} /><LogOut size={18} /></div>
    </aside>{children}</div>;
}
