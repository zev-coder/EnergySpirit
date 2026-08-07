import ProductCard from '../components/ProductCard'
import SectionTitle from '../components/SectionTitle'
import { products } from '../data/dummy'

function SearchProductPage() {
  return (
    <main className="mx-auto max-w-6xl px-4 py-12 md:px-6">
      <SectionTitle eyebrow="Search" title="Pencarian Produk">
        Data dummy diurutkan seolah berdasarkan drop terbaru.
      </SectionTitle>
      <div className="mb-6 flex flex-col gap-3 rounded-lg border border-white/10 bg-white/[0.04] p-4 md:flex-row">
        <input
          className="flex-1 rounded-lg border border-white/10 bg-black/20 px-4 py-3 text-white outline-none placeholder:text-slate-500"
          placeholder="Cari nama produk"
          type="search"
        />
        <select className="rounded-lg border border-white/10 bg-black/20 px-4 py-3 text-white outline-none">
          <option>Semua kategori</option>
          <option>Drinks</option>
          <option>Apparel</option>
          <option>Vehicles</option>
        </select>
      </div>
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
      <div className="mt-8 flex justify-center gap-2">
        {[1, 2, 3].map((page) => (
          <button
            className={`h-10 w-10 rounded-lg border border-white/10 ${page === 1 ? 'bg-emerald-400 text-purple-950' : 'bg-white/5 text-white'}`}
            key={page}
            type="button"
          >
            {page}
          </button>
        ))}
      </div>
    </main>
  )
}

export default SearchProductPage
