import { Minus, Plus } from 'lucide-react'

function QuantitySelector({ value, onChange }) {
  return (
    <div className="inline-flex items-center rounded-lg border border-white/10 bg-white/5">
      <button
        aria-label="Kurangi jumlah"
        className="p-3 text-slate-200 disabled:opacity-40"
        disabled={value <= 1}
        onClick={() => onChange(value - 1)}
        type="button"
      >
        <Minus size={18} />
      </button>
      <span className="w-12 text-center font-semibold text-white">{value}</span>
      <button
        aria-label="Tambah jumlah"
        className="p-3 text-slate-200"
        onClick={() => onChange(value + 1)}
        type="button"
      >
        <Plus size={18} />
      </button>
    </div>
  )
}

export default QuantitySelector
