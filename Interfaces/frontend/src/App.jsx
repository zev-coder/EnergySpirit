import { Route, Routes } from 'react-router-dom'
import Footer from './components/Footer'
import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import ProductDetailPage from './pages/ProductDetailPage'
import SearchProductPage from './pages/SearchProductPage'

function App() {
  return (
    <div className="min-h-screen bg-[#0d0616] text-slate-50">
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/produk" element={<SearchProductPage />} />
        <Route path="/produk/:id" element={<ProductDetailPage />} />
      </Routes>
      <Footer />
    </div>
  )
}

export default App
