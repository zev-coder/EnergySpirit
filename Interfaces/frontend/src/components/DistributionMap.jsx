import { MapPin } from 'lucide-react'
import { markers } from '../data/dummy'

const bounds = { west: 89, east: 134, north: 6.5, south: -12 }
const markerStyle = (lng, lat) => ({
  left: `${((lng - bounds.west) / (bounds.east - bounds.west)) * 100}%`,
  top: `${((bounds.north - lat) / (bounds.north - bounds.south)) * 100}%`,
})

function DistributionMap() {
  return (
    <div className="relative mx-auto h-[420px] max-w-5xl overflow-hidden rounded-lg border border-white/10 bg-[#13091f]">
      <iframe
        className="pointer-events-none h-full w-full grayscale invert-[.88] hue-rotate-[55deg] saturate-150"
        loading="lazy"
        referrerPolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps?ll=-2.8,111.7&z=5&output=embed"
        title="Google Maps Indonesia"
      />
      <div className="pointer-events-none absolute inset-0 bg-[#0d0616]/25" />
      {markers.map(([name, lng, lat]) => (
        <div className="pointer-events-none absolute -translate-x-1/2 -translate-y-1/2" key={name} style={markerStyle(lng, lat)}>
          <div className="flex items-center gap-2 rounded-full border border-white/10 bg-black/45 px-3 py-1 text-xs text-white">
            <MapPin size={14} className="text-emerald-300" />
            {name}
          </div>
        </div>
      ))}
    </div>
  )
}

export default DistributionMap
