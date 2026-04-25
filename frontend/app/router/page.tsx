'use client'
import { useState } from 'react'
import { motion } from 'framer-motion'

import { routePost } from '@/lib/api'

const BOTS = [
  { id: 'bot_a', name: 'TechMaximalist', emoji: '🚀', color: 'text-red-400', bg: 'bg-red-400/10 border-red-400/20' },
  { id: 'bot_b', name: 'DigitalDoomer', emoji: '🌍', color: 'text-blue-400', bg: 'bg-blue-400/10 border-blue-400/20' },
  { id: 'bot_c', name: 'FinanceBro', emoji: '📈', color: 'text-green-400', bg: 'bg-green-400/10 border-green-400/20' },
]

const EXAMPLE_POSTS = [
  'OpenAI just released a new model that might replace junior developers.',
  'Bitcoin hits new ATH. The financial revolution is unstoppable.',
  'Big Tech companies are harvesting your data and selling it to governments.',
  'Fed raises rates again. Yield curve inversion deepens.',
  'Elon Musk announces new AI chip that will power all Teslas.',
]

export default function RouterPage() {
  const [post, setPost] = useState('')
  const [threshold, setThreshold] = useState(0.45)
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleRoute() {
    if (!post.trim()) return
    setLoading(true)
    setError(null)
    try {
      const output = await routePost(post, threshold)
      setResult(output)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to route post'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl">
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-1">Phase 1 - Vector Persona Router</h2>
        <p className="text-zinc-400 text-sm">
          Finds which bots would care about a post using cosine similarity on persona embeddings.
        </p>
      </div>

      <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 mb-4">
        <label className="text-sm text-zinc-400 mb-2 block">Post Content</label>
        <textarea
          value={post}
          onChange={e => setPost(e.target.value)}
          placeholder="Type a social media post to route..."
          className="w-full bg-zinc-800 border border-zinc-700 rounded-lg p-3 text-sm text-white resize-none h-24 focus:outline-none focus:border-zinc-500"
        />
        <div className="flex gap-2 mt-3 flex-wrap">
          {EXAMPLE_POSTS.map(ex => (
            <button
              key={ex}
              onClick={() => setPost(ex)}
              className="text-xs px-3 py-1 bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 rounded-full text-zinc-300 transition-colors"
            >
              {ex.slice(0, 40)}...
            </button>
          ))}
        </div>

        <div className="flex items-center gap-4 mt-4">
          <div className="flex-1">
            <label className="text-xs text-zinc-500 mb-1 block">
              Threshold: <span className="text-zinc-300 font-mono">{threshold}</span>
            </label>
            <input
              type="range"
              min="0.1"
              max="0.9"
              step="0.05"
              value={threshold}
              onChange={e => setThreshold(parseFloat(e.target.value))}
              className="w-full"
            />
          </div>
          <button
            onClick={handleRoute}
            disabled={loading || !post.trim()}
            className="px-6 py-2 bg-white text-black text-sm font-medium rounded-lg hover:bg-zinc-200 disabled:opacity-40 transition-colors"
          >
            {loading ? 'Routing...' : 'Route Post ->'}
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 text-sm text-red-300 bg-red-500/10 border border-red-500/20 rounded-lg p-3">
          {error}
        </div>
      )}

      {result && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-3">
          {result.all_scores?.map((bot: any) => {
            const meta = BOTS.find(b => b.id === bot.bot_id)
            const pct = Math.round(bot.similarity_score * 100)
            return (
              <div
                key={bot.bot_id}
                className={`border rounded-xl p-4 ${bot.will_respond ? meta?.bg : 'bg-zinc-900 border-zinc-800 opacity-50'}`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span>{meta?.emoji}</span>
                    <span className={`font-medium text-sm ${bot.will_respond ? meta?.color : 'text-zinc-500'}`}>
                      {bot.bot_name}
                    </span>
                    {bot.will_respond && (
                      <span className="text-xs px-2 py-0.5 bg-white/10 text-white rounded-full">Will respond</span>
                    )}
                  </div>
                  <span className="font-mono text-sm text-zinc-300">{pct}%</span>
                </div>
                <div className="h-1.5 bg-zinc-800 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${pct}%` }}
                    transition={{ duration: 0.6, ease: 'easeOut' }}
                    className={`h-full rounded-full ${bot.will_respond ? 'bg-white' : 'bg-zinc-600'}`}
                  />
                </div>
              </div>
            )
          })}
        </motion.div>
      )}
    </div>
  )
}
