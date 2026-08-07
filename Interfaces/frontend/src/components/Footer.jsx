import { Camera, Mail, MessageCircle } from 'lucide-react'

function Footer() {
  return (
    <footer className="border-t border-white/10">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 px-4 py-8 text-sm text-slate-400 md:flex-row md:items-center md:justify-between md:px-6">
        <div className="flex items-center gap-2 text-white">
          <img className="h-10 w-10" src="/favicon.svg" alt="" />
          <span className="leading-none">
            <span className="block text-sm font-black tracking-wide text-emerald-400">ENERGY</span>
            <span className="block text-sm font-black tracking-wide text-purple-400">SPIRIT</span>
          </span>
        </div>
        <p>Copyright 2026 EnergySpirit. Dummy content only.</p>
        <div className="flex gap-3 text-slate-300">
          <MessageCircle size={18} />
          <Camera size={18} />
          <Mail size={18} />
        </div>
      </div>
    </footer>
  )
}

export default Footer
