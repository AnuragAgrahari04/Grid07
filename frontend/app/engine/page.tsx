'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'

import { generatePost } from '@/lib/api'
import { PostOutput } from '@/lib/types'

const BOTS = [
  { id: 'bot_a', name: 'TechMaximalist', accent: 'text-red-400' },
  { id: 'bot_b', name: 'DigitalDoomer', accent: 'text-blue-400' },
  { id: 'bot_c', name: 'FinanceBro', accent: 'text-green-400' },
]

export default function EnginePage() {
  const [botId, setBotId] = useState('bot_a')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<PostOutput | null>(null)

  async function onGenerate() {
    setLoading(true)
    setError(null)
    try {
      const output = await generatePost(botId)
      setResult(output)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl">
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-1">Phase 2 - LangGraph Content Engine</h2>
        <p className="text-zinc-400 text-sm">
          Generates an original, opinionated post using graph flow: decide topic, fetch context, draft output.
        </p>
      </div>

      <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 mb-4 space-y-4">
        <div>
          <label className="text-sm text-zinc-400 mb-2 block">Select Bot Persona</label>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
            {BOTS.map(bot => (
              <button
                key={bot.id}
                onClick={() => setBotId(bot.id)}
                className={`text-left px-3 py-2 rounded-lg border text-sm transition-colors ${
                  botId === bot.id
                    ? 'bg-zinc-800 border-zinc-600 text-white'
                    : 'bg-zinc-900 border-zinc-800 text-zinc-400 hover:bg-zinc-800 hover:text-zinc-200'
                }`}
              >
                <span className={bot.accent}>{bot.name}</span>
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={onGenerate}
          disabled={loading}
          className="px-6 py-2 bg-white text-black text-sm font-medium rounded-lg hover:bg-zinc-200 disabled:opacity-40 transition-colors"
        >
          {loading ? 'Generating...' : 'Run Content Engine ->'}
        </button>

        {error && (
          <div className="text-sm text-red-300 bg-red-500/10 border border-red-500/20 rounded-lg p-3">
            {error}
          </div>
        )}
      </div>

      {result && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 space-y-4"
        >
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Generated Post</h3>
            <span className="text-xs text-zinc-500 font-mono">{result.post_content.length} chars</span>
          </div>

          <div className="text-sm">
            <p className="text-zinc-400 mb-1">Topic</p>
            <p className="text-zinc-100 font-medium">{result.topic}</p>
          </div>

          <div className="text-sm">
            <p className="text-zinc-400 mb-1">Post Content</p>
            <p className="text-zinc-100 leading-relaxed">{result.post_content}</p>
          </div>

          <div>
            <p className="text-zinc-400 text-xs mb-2">Raw JSON</p>
            <pre className="bg-zinc-950 border border-zinc-800 rounded-lg p-3 text-xs text-zinc-200 overflow-auto">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        </motion.div>
      )}
    </div>
  )
}
