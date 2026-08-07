import { Link } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'

function ProductCard({ product }) {
  return (
    <article className="overflow-hidden rounded-lg border border-white/10 bg-white/[0.04] shadow-sm transition hover:-translate-y-1 hover:border-emerald-300/40">
      <img className="h-48 w-full object-cover" src={product.image} alt={product.name} />
      <div className="space-y-3 p-5">
        <div className="flex items-center justify-between gap-3">
          <span className="rounded-full border border-emerald-300/30 px-3 py-1 text-xs text-emerald-200">
            {product.category}
          </span>
          <span className="text-sm text-slate-300">{product.price}</span>
        </div>
        <h3 className="text-xl font-semibold text-white">{product.name}</h3>
        <p className="line-clamp-2 text-sm text-slate-300">{product.description}</p>
        <Link
          className="inline-flex items-center gap-2 text-sm font-medium text-emerald-300 hover:text-emerald-200"
          to={`/produk/${product.id}`}
        >
          Lihat detail <ArrowRight size={16} />
        </Link>
      </div>
    </article>
  )
}

export default ProductCard
