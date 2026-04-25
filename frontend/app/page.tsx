export default function DashboardPage() {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Grid07 Dashboard</h2>
      <p className="text-zinc-400 text-sm">
        Explore Phase 1 routing, Phase 2 content generation, and Phase 3 combat defense.
      </p>
      <div className="grid gap-4 md:grid-cols-3">
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4">
          <h3 className="font-semibold">Phase 1</h3>
          <p className="text-zinc-400 text-sm mt-1">Vector similarity router with ChromaDB.</p>
        </div>
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4">
          <h3 className="font-semibold">Phase 2</h3>
          <p className="text-zinc-400 text-sm mt-1">LangGraph-driven original post generation.</p>
        </div>
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4">
          <h3 className="font-semibold">Phase 3</h3>
          <p className="text-zinc-400 text-sm mt-1">RAG combat engine with injection defense.</p>
        </div>
      </div>
    </div>
  )
}
