type Props = {
  name: string
  description: string
}

export function BotCard({ name, description }: Props) {
  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4">
      <h4 className="font-semibold">{name}</h4>
      <p className="text-zinc-400 text-sm mt-1">{description}</p>
    </div>
  )
}
