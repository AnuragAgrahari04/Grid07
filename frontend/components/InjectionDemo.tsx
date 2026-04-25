type Props = {
  onInject: () => void
}

export function InjectionDemo({ onInject }: Props) {
  return (
    <button
      onClick={onInject}
      className="px-4 py-2 rounded-lg border border-red-500/40 bg-red-500/10 text-red-300 text-sm hover:bg-red-500/20"
    >
      Try Injection Attack
    </button>
  )
}
