import { Link } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'

function Hero() {
  return (
    <section className="mx-auto grid max-w-6xl gap-10 px-4 py-16 md:grid-cols-[1.05fr_.95fr] md:px-6 md:py-20">
      <div className="flex flex-col justify-center">
        <p className="mb-4 text-sm font-medium text-emerald-300">Energy drink and street lifestyle</p>
        <h1 className="max-w-3xl text-5xl font-semibold leading-tight text-white md:text-6xl">
          EnergySpirit
        </h1>
        <p className="mt-5 max-w-xl text-lg leading-8 text-slate-300">
          Katalog dummy untuk minuman energi, apparel racing, dan vehicle showcase dengan rasa brand yang tajam.
        </p>
        <div className="mt-8">
          <Link
            className="inline-flex items-center gap-2 rounded-lg bg-emerald-400 px-5 py-3 font-semibold text-purple-950 transition hover:bg-emerald-300"
            to="/produk"
          >
            Lihat Drop Terbaru <ArrowRight size={18} />
          </Link>
        </div>
      </div>
      <div className="min-h-80 overflow-hidden rounded-lg border border-white/10 bg-white/[0.04]">
        <img
          className="h-full min-h-80 w-full object-cover"
          src="https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=1100&q=80"
          alt="Rider dengan vibe lifestyle energy drink"
        />
      </div>
    </section>
  )
}

export default Hero
