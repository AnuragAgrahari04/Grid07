export type BotMatch = {
  bot_id: string
  bot_name: string
  similarity_score: number
  will_respond: boolean
}

export type RoutingResult = {
  post_content: string
  threshold_used: number
  all_scores: BotMatch[]
  matched_bots: BotMatch[]
  total_matched: number
}

export type PostOutput = {
  bot_id: string
  topic: string
  post_content: string
}

export type ThreadMessage = {
  author: string
  content: string
  is_bot: boolean
}

export type CombatResult = {
  bot_id: string
  bot_name: string
  reply: string
  injection_detected: boolean
  thread_depth: number
}
