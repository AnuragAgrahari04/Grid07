type Props = {
  value: number
}

export function SimilarityBar({ value }: Props) {
  const pct = Math.max(0, Math.min(100, Math.round(value * 100)))
  return (
    <div className="h-1.5 bg-zinc-800 rounded-full overflow-hidden">
      <div className="h-full bg-white rounded-full" style={{ width: `${pct}%` }} />
    </div>
  )
}
