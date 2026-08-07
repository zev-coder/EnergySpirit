import { Menu, Search, X } from 'lucide-react'
import { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'

const menu = [
  ['Home', '/'],
  ['Drinks', '/produk'],
  ['Apparel', '/produk'],
  ['Vehicles', '/produk'],
  ['Events', '/produk'],
]

function Navbar() {
  const [open, setOpen] = useState(false)

  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-[#0d0616]/90 backdrop-blur">
      <nav className="mx-auto flex max-w-6xl items-center gap-4 px-4 py-3 md:px-6">
        <Link className="flex items-center gap-2 text-lg font-semibold" to="/">
          <img className="h-10 w-10" src="/favicon.svg" alt="" />
          <span className="leading-none">
            <span className="block text-sm font-black tracking-wide text-emerald-400">ENERGY</span>
            <span className="block text-sm font-black tracking-wide text-purple-400">SPIRIT</span>
          </span>
        </Link>

        <div className="hidden flex-1 items-center justify-center gap-1 md:flex">
          {menu.map(([label, path]) => (
            <NavLink
              className={({ isActive }) =>
                `rounded-lg px-3 py-2 text-sm transition ${
                  isActive ? 'bg-white/10 text-white' : 'text-slate-300 hover:bg-white/5'
                }`
              }
              key={label}
              to={path}
            >
              {label}
            </NavLink>
          ))}
        </div>

        <form className="hidden w-72 items-center gap-2 rounded-lg border border-white/10 bg-white/5 px-3 py-2 md:flex">
          <Search size={16} className="text-slate-400" />
          <input
            className="min-w-0 flex-1 bg-transparent text-sm text-white outline-none placeholder:text-slate-500"
            placeholder="Cari produk"
            type="search"
          />
          <button className="rounded-md bg-emerald-400 px-3 py-1 text-sm font-medium text-purple-950" type="button">
            Search
          </button>
        </form>

        <button
          aria-label="Toggle menu"
          className="ml-auto rounded-lg border border-white/10 p-2 md:hidden"
          onClick={() => setOpen((value) => !value)}
          type="button"
        >
          {open ? <X size={20} /> : <Menu size={20} />}
        </button>
      </nav>

      {open && (
        <div className="border-t border-white/10 px-4 pb-4 md:hidden">
          <div className="flex flex-col gap-1 py-3">
            {menu.map(([label, path]) => (
              <Link className="rounded-lg px-3 py-2 text-slate-200 hover:bg-white/5" key={label} to={path}>
                {label}
              </Link>
            ))}
          </div>
          <div className="flex items-center gap-2 rounded-lg border border-white/10 bg-white/5 px-3 py-2">
            <Search size={16} className="text-slate-400" />
            <input className="min-w-0 flex-1 bg-transparent text-sm outline-none" placeholder="Cari produk" />
          </div>
        </div>
      )}
    </header>
  )
}

export default Navbar
