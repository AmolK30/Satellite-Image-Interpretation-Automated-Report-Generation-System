import { motion } from 'framer-motion'
import { FiGlobe } from 'react-icons/fi'

export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-slate-950/70 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <motion.div initial={{ opacity: 0, x: -12 }} animate={{ opacity: 1, x: 0 }} className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-cyan-400/15 text-cyan-300 shadow-glow ring-1 ring-cyan-300/30">
            <FiGlobe className="h-5 w-5" />
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-cyan-200/70">Orbital Intelligence</p>
            <h1 className="text-lg font-semibold text-white">Satellite Analysis System</h1>
          </div>
        </motion.div>
        <div className="hidden items-center gap-3 md:flex">
          <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs font-medium text-emerald-200">Live analysis</span>
          <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs font-medium text-slate-300">Geo-ready dashboard</span>
        </div>
      </div>
    </header>
  )
}
