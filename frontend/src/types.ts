export interface EnvironmentalSummary {
  score: number
  interpretation: string
  factors: Record<string, number>
}

export interface DisasterSummary {
  risk_level: 'Low' | 'Moderate' | 'High' | string
  threats: string[]
  recommendations: string[]
}

export interface AnalysisResponse {
  id: number
  analysis_type: string
  image_name: string
  image_path: string
  report: string
  report_text: string
  executive_summary: string
  environment_score: number
  land_distribution: Record<string, number>
  environmental_summary: EnvironmentalSummary
  disaster_summary: DisasterSummary
  classification: {
    confidence: number
    dominant_class: string
    raw_scores: Record<string, number>
  }
  features: Record<string, number | number[]>
  pdf_path?: string | null
  created_at?: string
}

export interface ComparisonResponse {
  urban_growth: number
  forest_loss: number
  report: string
  old_image: AnalysisResponse
  new_image: AnalysisResponse
}

export interface HistoryRecord extends AnalysisResponse {}
