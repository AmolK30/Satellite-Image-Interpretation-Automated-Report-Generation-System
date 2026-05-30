import { motion } from 'framer-motion'

interface Props {
  title: string
  value: string | number
  subtitle?: string
  accent?: string
}

export default function AnalysisCard({ title, value, subtitle, accent = 'from-cyan-400/30 to-blue-400/10' }: Props) {
  return (
    <motion.div
      whileHover={{ y: -4 }}
      className={`rounded-3xl border border-white/10 bg-gradient-to-br ${accent} p-[1px] shadow-2xl shadow-slate-950/25`}
    >
      <div className="rounded-[23px] bg-slate-950/70 p-5 backdrop-blur-xl">
        <p className="text-xs uppercase tracking-[0.35em] text-slate-400">{title}</p>
        <div className="mt-2 text-3xl font-semibold text-white">{value}</div>
        {subtitle ? <p className="mt-2 text-sm leading-6 text-slate-300">{subtitle}</p> : null}
      </div>
    </motion.div>
  )
}
