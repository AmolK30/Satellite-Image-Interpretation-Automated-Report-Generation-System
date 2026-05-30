interface Props {
  report: string
}

export default function ReportViewer({ report }: Props) {
  return (
    <div className="rounded-3xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-xl">
      <p className="text-xs uppercase tracking-[0.35em] text-cyan-200/60">Generated Report</p>
      <pre className="mt-4 whitespace-pre-wrap rounded-2xl border border-white/10 bg-slate-900/80 p-4 text-sm leading-7 text-slate-200">
        {report}
      </pre>
    </div>
  )
}
