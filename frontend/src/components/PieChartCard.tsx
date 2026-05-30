import { Chart as ChartJS, ArcElement, Tooltip, Legend, type ChartData } from 'chart.js'
import { Pie } from 'react-chartjs-2'

ChartJS.register(ArcElement, Tooltip, Legend)

interface Props {
  distribution: Record<string, number>
}

const palette = ['#38bdf8', '#34d399', '#f59e0b', '#f97316', '#a78bfa', '#22c55e', '#e879f9', '#64748b']

export default function PieChartCard({ distribution }: Props) {
  const labels = Object.keys(distribution)
  const values = Object.values(distribution)

  const data: ChartData<'pie'> = {
    labels: labels.map((label) => label.replace('_', ' ').toUpperCase()),
    datasets: [{ data: values, backgroundColor: palette.slice(0, values.length), borderColor: '#08111f', borderWidth: 2 }],
  }

  return (
    <div className="rounded-3xl border border-white/10 bg-slate-950/70 p-5 shadow-2xl shadow-slate-950/25 backdrop-blur-xl">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.35em] text-cyan-200/60">Land Distribution</p>
          <h3 className="mt-2 text-xl font-semibold text-white">Area composition</h3>
        </div>
      </div>
      <div className="mx-auto max-w-sm">
        <Pie data={data} />
      </div>
    </div>
  )
}
