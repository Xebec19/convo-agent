import Image from "next/image";

const features = [
  {
    icon: "/figma/privacy.svg",
    title: "Data Privacy",
    description:
      "Your documents are processed securely and never used to train public models. Isolated environments guarantee compliance.",
  },
  {
    icon: "/figma/citations.svg",
    title: "Accurate Citations",
    description:
      "Every answer includes verifiable citations linking directly to the source document, eliminating AI hallucinations.",
  },
  {
    icon: "/figma/knowledge-base.svg",
    title: "Custom Knowledge Bases",
    description:
      "Create isolated vector stores for different departments, projects, or clients to maintain contextual relevance.",
  },
];

const steps = [
  ["01", "Connect", "Securely upload documents or connect your existing data sources."],
  ["02", "Index", "RAG-Intel processes, chunks, and indexes your data for retrieval."],
  ["03", "Ask anything", "Query your knowledge base and get precise answers with sources."],
];

export default function Home() {
  return (
    <main className="landing-page min-h-screen overflow-hidden bg-app-background text-app-foreground">
      <header className="sticky top-0 z-20 border-b border-app-border/30 bg-app-surface/80 backdrop-blur-md">
        <nav className="mx-auto flex h-[72px] max-w-[1440px] items-center justify-between px-5 sm:px-10">
          <div className="flex items-center gap-6 sm:gap-8">
            <a className="text-2xl font-semibold tracking-[-0.04em]" href="#top">RAG-Intel</a>
            <div className="hidden items-center gap-6 text-sm text-app-muted sm:flex">
              <a href="#features">Features</a>
              <a href="#how-it-works">How it works</a>
            </div>
          </div>
          <div className="flex items-center gap-4 text-sm">
            <a className="hidden text-app-muted sm:block" href="#login">Log in</a>
            <a className="rounded-full bg-brand px-5 py-2.5 font-mono text-[13px] font-medium tracking-wide text-primary-foreground" href="#get-started">Get Started</a>
          </div>
        </nav>
      </header>

      <section id="top" className="relative isolate px-5 pb-24 pt-24 sm:px-10 sm:pb-[120px] sm:pt-[120px]">
        <div className="hero-glow absolute left-1/2 top-1/2 -z-10 h-[500px] w-[500px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-brand/5 blur-[32px] sm:h-[800px] sm:w-[800px]" />
        <div className="mx-auto flex max-w-[896px] flex-col items-center text-center">
          <h1 className="max-w-3xl text-4xl font-bold leading-tight tracking-[-0.045em] sm:text-5xl sm:leading-[1.17]">
            Transform your documents into intelligence
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-app-muted sm:text-lg sm:leading-[1.625]">
            Upload, index, and query your enterprise data with pinpoint accuracy. RAG-Intel provides secure, verifiable answers instantly.
          </p>
          <div className="flex flex-wrap justify-center gap-4 pb-16 pt-8">
            <a id="get-started" className="inline-flex items-center gap-1 rounded-full bg-brand px-6 py-3.5 font-mono text-[13px] font-medium tracking-wide text-primary-foreground shadow-lg shadow-brand/15" href="#how-it-works">
              Get Started <Image alt="" height={12} width={12} src="/figma/arrow-right.svg" />
            </a>
            <a className="rounded-full border border-app-surface/40 bg-app-surface/70 px-6 py-3.5 font-mono text-[13px] font-medium tracking-wide text-app-foreground shadow-glass backdrop-blur-md" href="#features">
              View Documentation
            </a>
          </div>

          <div className="w-full rounded-3xl border border-app-surface/60 bg-app-surface/70 p-2 shadow-glass backdrop-blur-md">
            <div className="overflow-hidden rounded-[20px] border border-app-border/30 bg-app-surface/50">
              <div className="flex h-10 items-center gap-2 border-b border-app-border/30 bg-app-surface/80 px-5">
                <i className="h-3 w-3 rounded-full bg-danger/80" />
                <i className="h-3 w-3 rounded-full bg-browser-blue/80" />
                <i className="h-3 w-3 rounded-full bg-browser-lavender/80" />
              </div>
              <div className="relative min-h-[300px] bg-app-surface/60 p-6 text-left backdrop-blur-md">
                <div className="absolute right-8 top-8 hidden h-48 w-64 rotate-3 rounded-xl border border-brand/10 bg-gradient-to-br from-brand/5 to-brand-accent/5 md:block" />
                <div className="absolute right-14 top-14 hidden h-48 w-64 -rotate-2 rounded-xl border border-brand/10 bg-gradient-to-br from-brand/5 to-brand-accent/5 md:block" />
                <div className="relative max-w-[690px] border-y border-r border-brand-accent border-l-[3px] bg-app-surface/80 px-6 py-6 shadow-sm backdrop-blur-md">
                  <p className="text-base leading-[26px] text-app-foreground"><strong className="font-semibold text-brand-accent">AI:</strong> Based on the uploaded Q3 financial report, the projected growth is 14%.</p>
                  <span className="mt-2 inline-flex items-center gap-1 rounded-md border border-app-border/50 bg-app-surface-muted px-2 py-1 font-mono text-[13px] font-medium text-brand"><Image alt="" height={12} width={12} src="/figma/citation.svg" /> pg. 12</span>
                </div>
                <div className="relative mt-12 rounded-xl border border-app-border/50 bg-app-surface/90 py-[19px] pl-5 pr-16 shadow-sm">
                  <span className="text-base text-app-subtle">Ask a question about your documents...</span>
                  <button aria-label="Send question" className="absolute right-2 top-1/2 -translate-y-1/2 rounded-lg p-2.5"><Image alt="" height={13} width={16} src="/figma/send.svg" /></button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="features" className="relative px-5 py-24 sm:px-10 sm:py-[100px]">
        <div className="absolute inset-0 -z-10 bg-gradient-to-b from-transparent via-app-surface-muted/50 to-transparent" />
        <div className="mx-auto max-w-[1200px]">
          <h2 className="text-center text-3xl font-semibold tracking-[-0.04em] sm:text-[32px]">Enterprise-Grade Retrieval</h2>
          <div className="mt-16 grid gap-6 md:grid-cols-3">
            {features.map((feature) => <article key={feature.title} className="rounded-3xl border border-app-surface/40 bg-app-surface/70 p-8 shadow-glass backdrop-blur-md">
              <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-strong to-brand shadow-sm"><Image alt="" className="max-h-6 max-w-6" height={24} width={24} src={feature.icon} /></div>
              <h3 className="mt-5 pt-3 text-2xl font-semibold tracking-[-0.02em]">{feature.title}</h3>
              <p className="mt-3 text-base leading-[26px] text-app-muted">{feature.description}</p>
            </article>)}
          </div>
        </div>
      </section>

      <section id="how-it-works" className="px-5 py-24 sm:px-10 sm:py-[100px]">
        <div className="mx-auto max-w-[1200px]">
          <h2 className="text-center text-3xl font-semibold tracking-[-0.04em] sm:text-[32px]">How it Works</h2>
          <div className="relative mt-20 grid gap-12 md:grid-cols-3 md:gap-10">
            <div className="absolute left-[15%] right-[15%] top-9 hidden h-px bg-app-border/60 md:block" />
            {steps.map(([number, title, description]) => <article key={number} className="relative text-center">
              <div className="mx-auto flex h-[72px] w-[72px] items-center justify-center rounded-3xl border border-app-surface/60 bg-app-surface/70 text-[40px] font-light tracking-[-0.06em] shadow-glass backdrop-blur-md">{number}</div>
              <h3 className="mt-8 text-2xl font-semibold tracking-[-0.03em]">{title}</h3>
              <p className="mx-auto mt-3 max-w-xs text-base leading-[26px] text-app-muted">{description}</p>
            </article>)}
          </div>
        </div>
      </section>

      <footer id="login" className="border-t border-app-border/30 bg-app-surface/60 px-5 py-12 sm:px-10">
        <div className="mx-auto flex max-w-[1200px] flex-col items-center justify-between gap-6 text-sm text-app-muted md:flex-row">
          <span className="text-2xl font-semibold tracking-[-0.04em] text-app-foreground">RAG-Intel</span>
          <div className="flex gap-6"><a href="#top">Privacy</a><a href="#top">Terms</a><a href="#top">Contact</a></div>
          <span>© 2025 RAG-Intel. All rights reserved.</span>
        </div>
      </footer>
    </main>
  );
}
