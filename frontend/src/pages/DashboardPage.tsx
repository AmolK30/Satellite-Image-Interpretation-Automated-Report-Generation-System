import { useEffect, useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import Navbar from '@/components/Navbar'
import Sidebar from '@/components/Sidebar'
import ImageUploader from '@/components/ImageUploader'
import AnalysisCard from '@/components/AnalysisCard'
import EnvironmentalScoreCard from '@/components/EnvironmentalScoreCard'
import PieChartCard from '@/components/PieChartCard'
import GrowthChart from '@/components/GrowthChart'
import MapViewer from '@/components/MapViewer'
import ReportViewer from '@/components/ReportViewer'
import ReportDownloadButton from '@/components/ReportDownloadButton'
import Footer from '@/components/Footer'
import { analyzeImage, compareImages, fetchHistory } from '@/services/api'
import type { AnalysisResponse, ComparisonResponse, HistoryRecord } from '@/types'

type Mode = 'single' | 'compare'

export default function DashboardPage() {
  const [mode, setMode] = useState<Mode>('single')
  const [singleImage, setSingleImage] = useState<File | null>(null)
  const [compareOldImage, setCompareOldImage] = useState<File | null>(null)
  const [compareNewImage, setCompareNewImage] = useState<File | null>(null)
  const [singlePreview, setSinglePreview] = useState<string | null>(null)
  const [oldPreview, setOldPreview] = useState<string | null>(null)
  const [newPreview, setNewPreview] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null)
  const [comparison, setComparison] = useState<ComparisonResponse | null>(null)
  const [history, setHistory] = useState<HistoryRecord[]>([])

  useEffect(() => {
    void fetchHistory()
      .then(setHistory)
      .catch(() => setHistory([]))
  }, [])

  useEffect(() => {
    if (!singleImage) return setSinglePreview(null)
    const url = URL.createObjectURL(singleImage)
    setSinglePreview(url)
    return () => URL.revokeObjectURL(url)
  }, [singleImage])

  useEffect(() => {
    if (!compareOldImage) return setOldPreview(null)
    const url = URL.createObjectURL(compareOldImage)
    setOldPreview(url)
    return () => URL.revokeObjectURL(url)
  }, [compareOldImage])

  useEffect(() => {
    if (!compareNewImage) return setNewPreview(null)
    const url = URL.createObjectURL(compareNewImage)
    setNewPreview(url)
    return () => URL.revokeObjectURL(url)
  }, [compareNewImage])

  const pdfUrl = useMemo(() => {
    if (!analysis?.pdf_path) return null
    return `${import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:5000/api'}/reports/${analysis.id}/pdf`
  }, [analysis])

  const handleAnalyze = async () => {
    if (!singleImage) {
      setError('Select a satellite image before running the analysis.')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const result = await analyzeImage(singleImage)
      setAnalysis(result)
      setComparison(null)
      setHistory((previous) => [result, ...previous.filter((record) => record.id !== result.id)])
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Analysis failed.')
    } finally {
      setLoading(false)
    }
  }

  const handleCompare = async () => {
    if (!compareOldImage || !compareNewImage) {
      setError('Select both the older and newer satellite images before comparing.')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const result = await compareImages(compareOldImage, compareNewImage)
      setComparison(result)
      setAnalysis(result.new_image)
      setHistory((previous) => [result.new_image, result.old_image, ...previous.filter((record) => record.id !== result.new_image.id && record.id !== result.old_image.id)])
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Comparison failed.')
    } finally {
      setLoading(false)
    }
  }

  const distribution = analysis?.land_distribution ?? {}
  const environmentalSummary = analysis?.environmental_summary
  const disasterSummary = analysis?.disaster_summary

  return (
    <div className="min-h-screen bg-cosmic-grid text-white">
      <Navbar />
      <div className="mx-auto flex max-w-[1700px] gap-6 px-4 py-6 sm:px-6 lg:px-8">
        <Sidebar />
        <main className="flex-1 space-y-6">
          <section className="grid gap-6 xl:grid-cols-[1.7fr_1fr]">
            <div className="rounded-[2rem] border border-white/10 bg-white/5 p-6 shadow-2xl shadow-slate-950/30 backdrop-blur-xl">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
                <div className="space-y-3">
                  <p className="text-xs uppercase tracking-[0.35em] text-cyan-200/60">Satellite Intelligence Dashboard</p>
                  <h2 className="max-w-2xl text-4xl font-semibold leading-tight text-white">Generate land-use, environmental, and disaster assessment reports from a single upload.</h2>
                  <p className="max-w-3xl text-sm leading-7 text-slate-300">This workspace combines classical remote-sensing heuristics with a production-ready API layer and a visual interface designed for planning teams, researchers, and portfolio demos.</p>
                </div>
                <div className="grid gap-3 sm:grid-cols-3">
                  <AnalysisCard title="Mode" value={mode === 'single' ? 'Single' : 'Compare'} subtitle="Switch between one-image analysis and change detection." />
                  <AnalysisCard title="History" value={history.length} subtitle="Analyses stored in SQLAlchemy history." accent="from-emerald-400/25 to-emerald-500/5" />
                  <AnalysisCard title="Status" value={loading ? 'Running' : 'Ready'} subtitle="Backend analysis pipeline is available." accent="from-amber-400/25 to-amber-500/5" />
                </div>
              </div>

              <div className="mt-6 flex flex-wrap gap-3">
                <button onClick={() => setMode('single')} className={`rounded-full px-4 py-2 text-sm font-medium transition ${mode === 'single' ? 'bg-cyan-400 text-slate-950' : 'bg-white/8 text-slate-200 hover:bg-white/12'}`}>Single Image</button>
                <button onClick={() => setMode('compare')} className={`rounded-full px-4 py-2 text-sm font-medium transition ${mode === 'compare' ? 'bg-cyan-400 text-slate-950' : 'bg-white/8 text-slate-200 hover:bg-white/12'}`}>Compare Images</button>
              </div>

              <div className="mt-6 grid gap-6 xl:grid-cols-2">
                {mode === 'single' ? (
                  <ImageUploader label="Primary satellite image" file={singleImage} previewUrl={singlePreview} onChange={setSingleImage} />
                ) : (
                  <>
                    <ImageUploader label="Image A - earlier scene" file={compareOldImage} previewUrl={oldPreview} onChange={setCompareOldImage} />
                    <ImageUploader label="Image B - newer scene" file={compareNewImage} previewUrl={newPreview} onChange={setCompareNewImage} />
                  </>
                )}
              </div>

              <div className="mt-6 flex flex-wrap items-center gap-3">
                <button
                  onClick={mode === 'single' ? handleAnalyze : handleCompare}
                  className="rounded-full bg-cyan-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
                  disabled={loading}
                >
                  {loading ? 'Processing...' : mode === 'single' ? 'Analyze Image' : 'Compare Images'}
                </button>
                <ReportDownloadButton pdfUrl={pdfUrl} />
                {error ? <span className="text-sm text-rose-300">{error}</span> : null}
              </div>
            </div>

            <div className="space-y-6">
              <EnvironmentalScoreCard
                score={analysis?.environment_score ?? 0}
                interpretation={environmentalSummary?.interpretation}
              />
              <div className="grid gap-4 sm:grid-cols-2">
                <AnalysisCard title="Dominant class" value={analysis?.classification?.dominant_class?.replace('_', ' ') ?? 'N/A'} subtitle="Highest confidence land-cover category." />
                <AnalysisCard title="Confidence" value={analysis ? `${Math.round((analysis.classification.confidence ?? 0) * 100)}%` : '0%'} subtitle="Classifier confidence based on the current scene." />
              </div>
              <div className="rounded-3xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-xl">
                <p className="text-xs uppercase tracking-[0.35em] text-cyan-200/60">Risk Summary</p>
                <div className="mt-3 space-y-3">
                  <div className="text-xl font-semibold text-white">{disasterSummary?.risk_level ?? 'No assessment yet'}</div>
                  <ul className="space-y-2 text-sm leading-6 text-slate-300">
                    {(disasterSummary?.threats ?? ['Upload an image to detect flood, drought, deforestation, or wildfire signals.']).map((item) => (
                      <li key={item} className="rounded-2xl border border-white/5 bg-white/5 px-3 py-2">{item}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </section>

          {analysis ? (
            <motion.section initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
              <PieChartCard distribution={distribution} />
              <MapViewer />
            </motion.section>
          ) : null}

          {analysis ? (
            <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
              <ReportViewer report={analysis.report_text} />
              <div className="space-y-6">
                <div className="rounded-3xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-xl">
                  <p className="text-xs uppercase tracking-[0.35em] text-cyan-200/60">Recommendations</p>
                  <ul className="mt-4 space-y-3 text-sm leading-6 text-slate-300">
                    {(analysis.disaster_summary?.recommendations ?? []).map((item) => (
                      <li key={item} className="rounded-2xl border border-white/5 bg-white/5 px-3 py-2">{item}</li>
                    ))}
                  </ul>
                </div>
                {comparison ? (
                  <div className="rounded-3xl border border-white/10 bg-slate-950/70 p-5 backdrop-blur-xl">
                    <p className="text-xs uppercase tracking-[0.35em] text-cyan-200/60">Comparison Report</p>
                    <p className="mt-3 text-sm leading-7 text-slate-200">{comparison.report}</p>
                  </div>
                ) : null}
              </div>
            </section>
          ) : null}

          {comparison ? (
            <GrowthChart
              oldUrban={comparison.old_image.land_distribution.urban ?? 0}
              newUrban={comparison.new_image.land_distribution.urban ?? 0}
              oldForest={comparison.old_image.land_distribution.forest ?? 0}
              newForest={comparison.new_image.land_distribution.forest ?? 0}
            />
          ) : null}
        </main>
      </div>
      <Footer />
    </div>
  )
}
