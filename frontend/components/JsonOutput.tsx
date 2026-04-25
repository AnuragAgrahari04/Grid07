type Props = {
  data: unknown
}

export function JsonOutput({ data }: Props) {
  return (
    <pre className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 text-xs text-zinc-200 overflow-auto">
      {JSON.stringify(data, null, 2)}
    </pre>
  )
}
