import { FiDownload } from 'react-icons/fi'

interface Props {
  pdfUrl: string | null
}

export default function ReportDownloadButton({ pdfUrl }: Props) {
  return (
    <a
      href={pdfUrl ?? '#'}
      target="_blank"
      rel="noreferrer"
      aria-disabled={!pdfUrl}
      className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium transition ${pdfUrl ? 'bg-cyan-400 text-slate-950 hover:bg-cyan-300' : 'cursor-not-allowed bg-white/10 text-slate-400'}`}
      onClick={(event) => {
        if (!pdfUrl) event.preventDefault()
      }}
    >
      <FiDownload />
      Download PDF
    </a>
  )
}
