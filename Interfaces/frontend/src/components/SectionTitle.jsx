function SectionTitle({ eyebrow, title, children }) {
  return (
    <div className="mx-auto mb-8 max-w-2xl text-center">
      <p className="mb-2 text-sm font-medium text-emerald-300">{eyebrow}</p>
      <h2 className="text-3xl font-semibold text-white md:text-4xl">{title}</h2>
      {children && <p className="mt-3 text-slate-300">{children}</p>}
    </div>
  )
}

export default SectionTitle
