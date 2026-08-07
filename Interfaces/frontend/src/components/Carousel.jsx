import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useEffect, useState } from 'react'

function Carousel({ slides }) {
  const [active, setActive] = useState(0)
  const current = slides[active]
  const move = (step) => setActive((value) => (value + step + slides.length) % slides.length)

  useEffect(() => {
    const timer = setInterval(() => {
      setActive((value) => (value + 1) % slides.length)
    }, 4000)
    return () => clearInterval(timer)
  }, [slides.length])

  return (
    <section className="mx-auto max-w-6xl px-4 md:px-6">
      <div className="relative overflow-hidden rounded-lg border border-white/10 bg-white/[0.04]">
        <img className="h-[360px] w-full object-cover opacity-75" src={current.image} alt={current.title} />
        <div className="absolute inset-0 bg-gradient-to-r from-[#0d0616]/90 via-[#0d0616]/50 to-transparent" />
        <div className="absolute inset-y-0 left-0 flex max-w-xl flex-col justify-center p-6 md:p-10">
          <p className="text-sm font-medium text-emerald-300">Featured slide</p>
          <h2 className="mt-2 text-3xl font-semibold text-white">{current.title}</h2>
          <p className="mt-3 text-slate-300">{current.text}</p>
        </div>
        <button
          aria-label="Previous slide"
          className="absolute left-3 top-1/2 rounded-lg border border-white/10 bg-black/30 p-2"
          onClick={() => move(-1)}
          type="button"
        >
          <ChevronLeft size={20} />
        </button>
        <button
          aria-label="Next slide"
          className="absolute right-3 top-1/2 rounded-lg border border-white/10 bg-black/30 p-2"
          onClick={() => move(1)}
          type="button"
        >
          <ChevronRight size={20} />
        </button>
        <div className="absolute bottom-4 left-0 right-0 flex justify-center gap-2">
          {slides.map((slide, index) => (
            <button
              aria-label={`Slide ${index + 1}: ${slide.title}`}
              className={`h-2 rounded-full transition-all ${index === active ? 'w-8 bg-emerald-300' : 'w-2 bg-white/50'}`}
              key={slide.title}
              onClick={() => setActive(index)}
              type="button"
            />
          ))}
        </div>
      </div>
    </section>
  )
}

export default Carousel
