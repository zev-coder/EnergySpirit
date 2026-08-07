import { Camera, Mail, MessageCircle } from 'lucide-react'
import SectionTitle from './SectionTitle'

const contacts = [
  [MessageCircle, 'WhatsApp', '+62 812 0000 0000'],
  [Camera, 'Instagram', '@energyspirit.id'],
  [Mail, 'Gmail', 'hello@energyspirit.test'],
]

function ContactSection() {
  return (
    <section className="mx-auto max-w-6xl px-4 py-16 md:px-6">
      <SectionTitle eyebrow="Contact" title="Hubungi EnergySpirit">
        Kontak dummy untuk menjaga tampilan tetap siap tanpa menyentuh backend.
      </SectionTitle>
      <img className="mx-auto mb-8 h-28 w-auto" src="/energy-spirit-logo.svg" alt="Energy Spirit" />
      <div className="grid gap-4 md:grid-cols-3">
        {contacts.map(([Icon, label, value]) => (
          <div className="rounded-lg border border-white/10 bg-white/[0.04] p-5" key={label}>
            <Icon className="mb-4 text-emerald-300" size={24} />
            <h3 className="font-semibold text-white">{label}</h3>
            <p className="mt-1 text-sm text-slate-300">{value}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

export default ContactSection
