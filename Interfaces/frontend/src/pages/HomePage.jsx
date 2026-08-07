import Carousel from '../components/Carousel'
import ContactSection from '../components/ContactSection'
import DistributionMap from '../components/DistributionMap'
import Hero from '../components/Hero'
import ProductCard from '../components/ProductCard'
import SectionTitle from '../components/SectionTitle'
import { products, slides } from '../data/dummy'

function HomePage() {
  return (
    <main>
      <Hero />
      <Carousel slides={slides} />
      <section className="mx-auto max-w-6xl px-4 py-16 md:px-6">
        <SectionTitle eyebrow="New products" title="Produk Terbaru">
          Drop terbaru untuk drinks, apparel, dan vehicle showcase dummy.
        </SectionTitle>
        <div className="grid gap-5 md:grid-cols-3">
          {products.slice(0, 3).map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>
      <section className="px-4 py-16 md:px-6">
        <SectionTitle eyebrow="Distribution" title="Wilayah Distribusi Indonesia">
          Peta Google Maps Indonesia dengan marker dummy untuk kota distribusi dan event.
        </SectionTitle>
        <DistributionMap />
      </section>
      <ContactSection />
    </main>
  )
}

export default HomePage
