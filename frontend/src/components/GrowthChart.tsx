import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Tooltip, Legend, type ChartData } from 'chart.js'
import { Bar, Line } from 'react-chartjs-2'

ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, LineElement, Tooltip, Legend)

interface Props {
  oldUrban: number
  newUrban: number
  oldForest: number
  newForest: number
}

export default function GrowthChart({ oldUrban, newUrban, oldForest, newForest }: Props) {
  const barData: ChartData<'bar'> = {
    labels: ['Urban', 'Forest'],
    datasets: [
      { label: '2020', data: [oldUrban, oldForest], backgroundColor: ['#38bdf8', '#34d399'] },
      { label: '2025', data: [newUrban, newForest], backgroundColor: ['#0f766e', '#1d4ed8'] },
    ],
  }

  const lineData: ChartData<'line'> = {
    labels: ['2020', '2021', '2022', '2023', '2024', '2025'],
    datasets: [
      {
        label: 'Urban expansion',
        data: [oldUrban, oldUrban + (newUrban - oldUrban) * 0.2, oldUrban + (newUrban - oldUrban) * 0.4, oldUrban + (newUrban - oldUrban) * 0.6, oldUrban + (newUrban - oldUrban) * 0.8, newUrban],
        borderColor: '#38bdf8',
        backgroundColor: 'rgba(56, 189, 248, 0.15)',
      },
    ],
  }

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <div className="rounded-3xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-xl">
        <p className="text-xs uppercase tracking-[0.35em] text-cyan-200/60">Comparison</p>
        <h3 className="mt-2 text-xl font-semibold text-white">Urban and forest change</h3>
        <Bar data={barData} />
      </div>
      <div className="rounded-3xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-xl">
        <p className="text-xs uppercase tracking-[0.35em] text-cyan-200/60">Trend graph</p>
        <h3 className="mt-2 text-xl font-semibold text-white">Urban growth trajectory</h3>
        <Line data={lineData} />
      </div>
    </div>
  )
}
