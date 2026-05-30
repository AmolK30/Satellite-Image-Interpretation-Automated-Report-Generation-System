import { FiBarChart2, FiCloudLightning, FiDownload, FiLayers, FiMapPin } from 'react-icons/fi'

const items = [
  { label: 'Analysis', icon: FiBarChart2 },
  { label: 'Compare', icon: FiLayers },
  { label: 'Disaster', icon: FiCloudLightning },
  { label: 'Map', icon: FiMapPin },
  { label: 'Export', icon: FiDownload },
]

export default function Sidebar() {
  return (
    <aside className="hidden w-72 shrink-0 border-r border-white/10 bg-white/5 p-4 backdrop-blur-xl xl:block">
      <div className="space-y-4 rounded-3xl border border-white/10 bg-slate-900/55 p-5 shadow-2xl shadow-cyan-950/20">
        <p className="text-xs uppercase tracking-[0.3em] text-cyan-200/60">Mission Panel</p>
        <div className="space-y-2">
          <h2 className="text-2xl font-semibold text-white">Environmental intelligence for planning teams.</h2>
          <p className="text-sm leading-6 text-slate-300">Upload a satellite scene, inspect land-cover distribution, generate a professional report, and export it as a PDF package.</p>
        </div>
        <div className="space-y-2 pt-2">
          {items.map((item) => (
            <div key={item.label} className="flex items-center gap-3 rounded-2xl border border-white/5 bg-white/5 px-3 py-2 text-sm text-slate-200">
              <item.icon className="h-4 w-4 text-cyan-300" />
              <span>{item.label}</span>
            </div>
          ))}
        </div>
      </div>
    </aside>
  )
}
