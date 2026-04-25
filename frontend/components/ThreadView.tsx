type Message = {
  author: string
  content: string
}

type Props = {
  parentPost: string
  messages: Message[]
}

export function ThreadView({ parentPost, messages }: Props) {
  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 space-y-2">
      <p className="text-sm text-zinc-300"><span className="font-semibold">Parent:</span> {parentPost}</p>
      {messages.map((m, idx) => (
        <p key={idx} className="text-sm text-zinc-400">
          <span className="text-zinc-200">{m.author}:</span> {m.content}
        </p>
      ))}
    </div>
  )
}
