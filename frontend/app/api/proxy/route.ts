import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

const BOT_MAP = {
  bot_a: 'TechMaximalist',
  bot_b: 'DigitalDoomer',
  bot_c: 'FinanceBro',
} as const

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value))
}

function fallbackRoute(body: any) {
  const post = String(body?.post_content || '')
  const threshold = Number.isFinite(body?.threshold) ? Number(body.threshold) : 0.45
  const text = post.toLowerCase()

  const scores = [
    {
      bot_id: 'bot_a',
      bot_name: BOT_MAP.bot_a,
      similarity_score: clamp(0.35 + (/(ai|openai|tesla|elon|tech|software|chip)/.test(text) ? 0.45 : 0.05), 0, 0.99),
    },
    {
      bot_id: 'bot_b',
      bot_name: BOT_MAP.bot_b,
      similarity_score: clamp(0.3 + (/(data|privacy|surveillance|climate|govern|risk|danger)/.test(text) ? 0.5 : 0.08), 0, 0.99),
    },
    {
      bot_id: 'bot_c',
      bot_name: BOT_MAP.bot_c,
      similarity_score: clamp(0.33 + (/(bitcoin|btc|fed|rates|market|stock|yield|finance|etf)/.test(text) ? 0.5 : 0.06), 0, 0.99),
    },
  ].map(item => ({ ...item, will_respond: item.similarity_score >= threshold }))

  return {
    post_content: post,
    threshold_used: threshold,
    all_scores: scores,
    matched_bots: scores.filter(item => item.will_respond),
    total_matched: scores.filter(item => item.will_respond).length,
    source: 'fallback',
  }
}

function fallbackGenerate(body: any) {
  const botId = String(body?.bot_id || 'bot_a') as keyof typeof BOT_MAP
  const byBot: Record<string, { topic: string; post_content: string }> = {
    bot_a: {
      topic: 'AI automation leap',
      post_content:
        'AI agents are replacing repetitive workflows faster than most teams can retrain for. The winners will be teams that redesign roles now, not those waiting for “stability.”',
    },
    bot_b: {
      topic: 'Platform trust collapse',
      post_content:
        'People keep calling it “innovation” while surveillance, misinformation loops, and platform lock-in keep getting worse. If incentives stay broken, trust keeps collapsing.',
    },
    bot_c: {
      topic: 'Risk-on market momentum',
      post_content:
        'Rates, liquidity, and earnings revisions still drive this tape. If you are trading headlines without a risk framework, you are donating alpha to disciplined players.',
    },
  }

  const selected = byBot[botId] || byBot.bot_a
  return {
    bot_id: botId,
    topic: selected.topic,
    post_content: selected.post_content.slice(0, 280),
    source: 'fallback',
  }
}

function fallbackDefend(body: any) {
  const botId = String(body?.bot_id || 'bot_a') as keyof typeof BOT_MAP
  const humanReply = String(body?.human_reply || '')
  const history = Array.isArray(body?.comment_history) ? body.comment_history : []
  const injectionDetected = /(ignore all previous|you are now|forget previous|system prompt|reveal prompt)/i.test(humanReply)

  const secureReply = injectionDetected
    ? 'Nice try. I am staying in-role and addressing the EV argument directly: battery economics and charging reliability are improving, but adoption still depends on infrastructure execution and total cost parity.'
    : 'You are right to focus on real-world costs, but the trendline matters: battery prices, software efficiency, and charging buildout are all moving in the right direction. The debate is timeline, not direction.'

  return {
    bot_id: botId,
    bot_name: BOT_MAP[botId] || BOT_MAP.bot_a,
    reply: secureReply,
    injection_detected: injectionDetected,
    thread_depth: history.length,
    source: 'fallback',
  }
}

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => ({}))
  const targetPath = req.nextUrl.searchParams.get('path') || '/api/health'

  try {
    const response = await fetch(`${BACKEND_URL}${targetPath}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })

    const data = await response.json().catch(() => ({}))
    return NextResponse.json(data, { status: response.status })
  } catch {
    if (targetPath === '/api/phase1/route') {
      return NextResponse.json(fallbackRoute(body), { status: 200 })
    }
    if (targetPath === '/api/phase2/generate') {
      return NextResponse.json(fallbackGenerate(body), { status: 200 })
    }
    if (targetPath === '/api/phase3/defend') {
      return NextResponse.json(fallbackDefend(body), { status: 200 })
    }

    return NextResponse.json(
      {
        error: 'backend_unreachable',
        details: `Backend is unavailable at ${BACKEND_URL}`,
      },
      { status: 503 },
    )
  }
}
