import { Cloud, FolderPlus, Search, Upload } from "lucide-react";
import { WorkspaceShell } from "@/components/workspace-shell";
const docs = [
    ["EUR_Q3_Financials_v2.pdf", "PDF", "2.4 MB", "Indexed"],
    ["Renewables_Strategy_2024.docx", "DOCX", "1.8 MB", "Processing"],
    ["European Division Reports", "Folder", "—", "Indexed"],
    ["Market Analysis.xlsx", "XLSX", "856 KB", "Failed"],
];
export default function KnowledgeBase() {
    return (
        <WorkspaceShell active="knowledge">
            <main className="flex-1 p-6 md:p-10">
                <header className="flex flex-col gap-5 border-b border-app-border-strong pb-6 sm:flex-row sm:items-center sm:justify-between">
                    <div>
                        <h1 className="text-[32px] font-semibold tracking-tight">
                            Knowledge Base
                        </h1>
                        <p className="text-app-muted">
                            Manage your connected data sources and documents for RAG
                            retrieval.
                        </p>
                    </div>
                    <div className="flex gap-3">
                        <button className="rounded-xl border bg-app-surface px-4 py-3 font-mono text-[13px]">
                            <FolderPlus className="mr-2 inline" size={16} />
                            Add Folder
                        </button>
                        <button className="rounded-xl border bg-app-surface px-4 py-3 font-mono text-[13px]">
                            <Cloud className="mr-2 inline" size={16} />
                            Connect Cloud Storage
                        </button>
                    </div>
                </header>
                <section className="mt-10 rounded-2xl border-2 border-dashed border-app-border bg-app-surface/70 px-6 py-10 text-center">
                    <div className="mx-auto grid h-16 w-16 place-items-center rounded-full bg-app-border-strong">
                        <Upload size={25} />
                    </div>
                    <h2 className="mt-5 text-2xl font-semibold">Upload Documents</h2>
                    <p className="mx-auto mt-2 max-w-md text-app-muted">
                        Drag & drop your PDF, DOCX, TXT, or CSV files here, or click to
                        browse your local machine.
                    </p>
                    <button className="mt-6 rounded-xl bg-brand px-6 py-3 text-primary-foreground">
                        Select Files
                    </button>
                    <p className="mt-4 font-mono text-[13px] text-app-subtle">
                        Max file size: 50MB. Supported formats: .pdf, .docx, .txt, .csv
                    </p>
                </section>
                <section className="mt-10">
                    <div className="flex rounded-xl border bg-app-surface p-2">
                        <Search className="m-3 text-app-subtle" size={18} />
                        <input
                            className="flex-1 outline-none"
                            placeholder="Search documents..."
                        />
                    </div>
                    <div className="mt-6 overflow-hidden rounded-xl border bg-app-surface">
                        <table className="w-full text-left">
                            <thead className="border-b bg-app-background text-sm text-app-subtle">
                                <tr>
                                    <th className="p-5">Name</th>
                                    <th>Type</th>
                                    <th>Size</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {docs.map((d) => (
                                    <tr key={d[0]} className="border-b last:border-0">
                                        <td className="p-5 font-medium">{d[0]}</td>
                                        <td>{d[1]}</td>
                                        <td>{d[2]}</td>
                                        <td>
                                            <span
                                                className={`rounded-full px-3 py-1 text-sm ${d[3] === "Failed" ? "bg-danger-soft text-danger-foreground" : "bg-app-surface-muted text-brand"}`}
                                            >
                                                {d[3]}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </section>
            </main>
        </WorkspaceShell>
    );
}
