import axios from 'axios'
import type { AnalysisResponse, ComparisonResponse, HistoryRecord } from '@/types'

const baseURL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:5000/api'

export const api = axios.create({
  baseURL,
  timeout: 120000,
})

export async function analyzeImage(file: File): Promise<AnalysisResponse> {
  const formData = new FormData()
  formData.append('image', file)
  formData.append('generate_pdf', 'true')
  const response = await api.post<AnalysisResponse>('/analyze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

export async function compareImages(oldImage: File, newImage: File): Promise<ComparisonResponse> {
  const formData = new FormData()
  formData.append('old_image', oldImage)
  formData.append('new_image', newImage)
  const response = await api.post<ComparisonResponse>('/compare-images', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

export async function fetchHistory(): Promise<HistoryRecord[]> {
  const response = await api.get<HistoryRecord[]>('/history')
  return response.data
}

export async function deleteHistoryRecord(id: number): Promise<void> {
  await api.delete(`/history/${id}`)
}

export function getPdfUrl(recordId: number): string {
  return `${baseURL.replace(/\/api$/, '')}/api/reports/${recordId}/pdf`
}
