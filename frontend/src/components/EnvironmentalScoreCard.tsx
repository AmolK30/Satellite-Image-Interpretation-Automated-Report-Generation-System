import { motion } from 'framer-motion'

interface Props {
  score: number
  interpretation?: string
}

export default function EnvironmentalScoreCard({ score, interpretation }: Props) {
  const stroke = Math.max(0, Math.min(score, 100))

  return (
    <motion.div whileHover={{ scale: 1.01 }} className="rounded-3xl border border-white/10 bg-slate-950/70 p-5 shadow-2xl shadow-cyan-950/10 backdrop-blur-xl">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.35em] text-cyan-200/60">Environmental Score</p>
          <h3 className="mt-2 text-2xl font-semibold text-white">{score}/100</h3>
        </div>
        <div
          className="flex h-24 w-24 items-center justify-center rounded-full border border-cyan-300/20 text-lg font-semibold text-cyan-100"
          style={{ background: `conic-gradient(#22d3ee ${stroke * 3.6}deg, rgba(255,255,255,0.08) 0deg)` }}
        >
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-slate-950 text-white">{score}</div>
        </div>
      </div>
      {interpretation ? <p className="mt-4 text-sm leading-6 text-slate-300">{interpretation}</p> : null}
    </motion.div>
  )
}
