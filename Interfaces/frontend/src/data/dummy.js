export const products = [
  {
    id: 'volt-rush-can',
    name: 'Volt Rush Can',
    category: 'Drinks',
    price: 'Rp 24.000',
    stock: 24,
    image:
      'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=900&q=80',
    description:
      'Minuman energi citrus dummy dengan karakter tajam untuk sesi latihan, malam kreatif, dan perjalanan panjang.',
  },
  {
    id: 'phantom-grape',
    name: 'Phantom Grape Zero',
    category: 'Drinks',
    price: 'Rp 26.000',
    stock: 16,
    image:
      'https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=900&q=80',
    description:
      'Varian anggur tanpa gula dengan finish ringan, dibuat untuk vibe malam kota dan event musik.',
  },
  {
    id: 'spirit-racing-hoodie',
    name: 'Spirit Racing Hoodie',
    category: 'Apparel',
    price: 'Rp 429.000',
    stock: 38,
    image:
      'https://images.unsplash.com/photo-1523398002811-999ca8dec234?auto=format&fit=crop&w=900&q=80',
    description:
      'Hoodie streetwear dummy dengan potongan clean, aksen hijau elektrik, dan feel paddock malam.',
  },
  {
    id: 'night-circuit-jersey',
    name: 'Night Circuit Jersey',
    category: 'Apparel',
    price: 'Rp 279.000',
    stock: 42,
    image:
      'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=900&q=80',
    description:
      'Jersey dummy bergaya racing untuk drop komunitas, nyaman dipakai harian tanpa terlihat berlebihan.',
  },
  {
    id: 'urban-volt-ebike',
    name: 'Urban Volt E-Bike',
    category: 'Vehicles',
    price: 'Rp 18.900.000',
    stock: 51,
    image:
      'https://images.unsplash.com/photo-1571068316344-75bc76f77890?auto=format&fit=crop&w=900&q=80',
    description:
      'Konsep e-bike dummy untuk campaign urban ride, ringan, agresif, dan cocok untuk showcase brand.',
  },
  {
    id: 'drift-concept',
    name: 'EnergySpirit Drift Concept',
    category: 'Vehicles',
    price: 'Rp 345.000.000',
    stock: 67,
    image:
      'https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?auto=format&fit=crop&w=900&q=80',
    description:
      'Kendaraan konsep dummy untuk event drift dan activation, bukan unit penjualan nyata.',
  },
]

export const slides = products.slice(0, 4).map((product) => ({
  title: product.name,
  text: product.description,
  image: product.image,
}))

export const comments = [
  {
    name: 'Raka Pratama',
    date: '12 Jul 2026',
    text: 'Vibe produknya cocok buat katalog brand lifestyle yang energik.',
  },
  {
    name: 'Maya Lestari',
    date: '18 Jul 2026',
    text: 'Kategori minuman, apparel, dan vehicle showcase gampang dibaca.',
  },
]

export const markers = [
  ['Balikpapan', 116.85, -1.24],
  ['Samarinda', 117.14, -0.5],
  ['Jambi', 103.61, -1.61],
  ['Makassar', 119.43, -5.15],
  ['Jakarta', 106.85, -6.2],
]
