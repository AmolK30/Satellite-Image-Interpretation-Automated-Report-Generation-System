import { useId } from 'react'
import { FiImage, FiUploadCloud } from 'react-icons/fi'

interface Props {
  label: string
  file: File | null
  previewUrl: string | null
  onChange: (file: File | null) => void
  accept?: string
}

export default function ImageUploader({ label, file, previewUrl, onChange, accept = '.jpg,.jpeg,.png,.tif,.tiff,.bmp,.webp' }: Props) {
  const inputId = useId()

  return (
    <label htmlFor={inputId} className="group block cursor-pointer">
      <input
        id={inputId}
        type="file"
        accept={accept}
        className="sr-only"
        onChange={(event) => onChange(event.target.files?.[0] ?? null)}
      />
      <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/6 p-5 transition duration-300 group-hover:border-cyan-300/30 group-hover:bg-white/8">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.3em] text-cyan-200/60">{label}</p>
            <h3 className="text-lg font-semibold text-white">{file?.name ?? 'Upload a satellite scene'}</h3>
          </div>
          <div className="rounded-2xl border border-cyan-300/20 bg-cyan-300/10 p-3 text-cyan-200">
            <FiUploadCloud className="h-5 w-5" />
          </div>
        </div>
        <div className="flex min-h-56 items-center justify-center overflow-hidden rounded-2xl border border-dashed border-white/10 bg-slate-950/40 text-center text-slate-400">
          {previewUrl ? (
            <img src={previewUrl} alt={label} className="max-h-56 w-full object-contain p-2" />
          ) : (
            <div className="space-y-3 px-6 py-8">
              <FiImage className="mx-auto h-9 w-9 text-cyan-300/70" />
              <p>Drag and drop or click to upload JPG, PNG, TIFF, or GeoTIFF imagery.</p>
            </div>
          )}
        </div>
      </div>
    </label>
  )
}
