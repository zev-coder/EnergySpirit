import { Send } from 'lucide-react'
import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import QuantitySelector from '../components/QuantitySelector'
import { comments, products } from '../data/dummy'

function ProductDetailPage() {
  const { id } = useParams()
  const product = products.find((item) => item.id === id) || products[0]
  const [quantity, setQuantity] = useState(1)

  return (
    <main className="mx-auto max-w-6xl px-4 py-12 md:px-6">
      <Link className="text-sm text-emerald-300 hover:text-emerald-200" to="/produk">
        Kembali ke produk
      </Link>
      <section className="mt-6 grid gap-8 md:grid-cols-2">
        <div className="overflow-hidden rounded-lg border border-white/10 bg-white/[0.04]">
          <img className="h-full min-h-96 w-full object-cover" src={product.image} alt={product.name} />
        </div>
        <div className="rounded-lg border border-white/10 bg-white/[0.04] p-6">
          <span className="rounded-full border border-emerald-300/30 px-3 py-1 text-sm text-emerald-200">
            {product.category}
          </span>
          <h1 className="mt-5 text-4xl font-semibold text-white">{product.name}</h1>
          <p className="mt-4 leading-7 text-slate-300">{product.description}</p>
          <div className="mt-6 grid gap-4 text-sm text-slate-300 sm:grid-cols-2">
            <div className="rounded-lg border border-white/10 bg-black/20 p-4">
              <p>Harga</p>
              <strong className="mt-1 block text-xl text-white">{product.price}</strong>
            </div>
            <div className="rounded-lg border border-white/10 bg-black/20 p-4">
              <p>Stok dummy</p>
              <strong className="mt-1 block text-xl text-white">{product.stock}</strong>
            </div>
          </div>
          <div className="mt-6">
            <p className="mb-3 text-sm text-slate-300">Quantity</p>
            <QuantitySelector value={quantity} onChange={setQuantity} />
          </div>
          <button className="mt-8 w-full rounded-lg bg-emerald-400 px-5 py-3 font-semibold text-purple-950 hover:bg-emerald-300" type="button">
            Checkout
          </button>
        </div>
      </section>

      <section className="mt-12 rounded-lg border border-white/10 bg-white/[0.04] p-6">
        <h2 className="text-2xl font-semibold text-white">Komentar</h2>
        <div className="mt-5 space-y-4">
          {comments.map((comment) => (
            <article className="flex gap-4 rounded-lg border border-white/10 bg-black/20 p-4" key={comment.name}>
              <div className="grid h-11 w-11 shrink-0 place-items-center rounded-full bg-emerald-400 font-semibold text-purple-950">
                {comment.name.slice(0, 1)}
              </div>
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <h3 className="font-semibold text-white">{comment.name}</h3>
                  <span className="text-xs text-slate-400">{comment.date}</span>
                </div>
                <p className="mt-1 text-sm text-slate-300">{comment.text}</p>
              </div>
            </article>
          ))}
        </div>
        <form className="mt-6 grid gap-3">
          <textarea className="min-h-28 rounded-lg border border-white/10 bg-black/20 p-4 text-white outline-none placeholder:text-slate-500" placeholder="Tulis komentar dummy" />
          <button className="inline-flex w-fit items-center gap-2 rounded-lg bg-emerald-400 px-5 py-3 font-semibold text-purple-950" type="button">
            <Send size={18} /> Kirim komentar
          </button>
        </form>
      </section>
    </main>
  )
}

export default ProductDetailPage
