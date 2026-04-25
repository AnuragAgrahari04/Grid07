'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Cpu, GitBranch, Swords, LayoutDashboard } from 'lucide-react'

const nav = [
  { href: '/', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/router', label: 'Phase 1 - Router', icon: Cpu, badge: 'Vector' },
  { href: '/engine', label: 'Phase 2 - Engine', icon: GitBranch, badge: 'LangGraph' },
  { href: '/combat', label: 'Phase 3 - Combat', icon: Swords, badge: 'RAG' },
]

export function Sidebar() {
  const path = usePathname()
  return (
    <aside className="w-64 border-r border-zinc-800 flex flex-col p-6 gap-2">
      <div className="mb-6">
        <h1 className="text-xl font-bold text-white">Grid07</h1>
        <p className="text-xs text-zinc-500">Cognitive Engine v1.0</p>
      </div>
      {nav.map(({ href, label, icon: Icon, badge }) => (
        <Link
          key={href}
          href={href}
          className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
            path === href
              ? 'bg-zinc-800 text-white'
              : 'text-zinc-400 hover:text-white hover:bg-zinc-900'
          }`}
        >
          <Icon size={16} />
          <span className="flex-1">{label}</span>
          {badge && (
            <span className="text-xs px-2 py-0.5 bg-zinc-700 text-zinc-300 rounded-full">{badge}</span>
          )}
        </Link>
      ))}
    </aside>
  )
}
