import { CombatResult, PostOutput, RoutingResult, ThreadMessage } from './types'

const PROXY_URL = '/api/proxy'

type ApiErrorBody = {
  error?: string
  details?: string
  detail?: string
}

async function postViaProxy<T>(path: string, payload: unknown): Promise<T> {
  const res = await fetch(`${PROXY_URL}?path=${encodeURIComponent(path)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  const body = (await res.json()) as T | ApiErrorBody
  if (!res.ok) {
    const message =
      (body as ApiErrorBody).detail ||
      (body as ApiErrorBody).details ||
      (body as ApiErrorBody).error ||
      `Request failed for ${path}`
    throw new Error(message)
  }

  return body as T
}

export async function routePost(post_content: string, threshold: number): Promise<RoutingResult> {
  return postViaProxy<RoutingResult>('/api/phase1/route', { post_content, threshold })
}

export async function generatePost(bot_id: string): Promise<PostOutput> {
  return postViaProxy<PostOutput>('/api/phase2/generate', { bot_id })
}

export async function defendThread(params: {
  bot_id: string
  parent_post: string
  comment_history: ThreadMessage[]
  human_reply: string
}): Promise<CombatResult> {
  return postViaProxy<CombatResult>('/api/phase3/defend', params)
}
