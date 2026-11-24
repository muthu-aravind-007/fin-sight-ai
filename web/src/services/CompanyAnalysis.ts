
import type {
  CompanyAnalysisRequest,
  CompanyAnalysisResponse,
} from '../types/analysis'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export async function analyzeCompany(
  request: CompanyAnalysisRequest,
): Promise<CompanyAnalysisResponse> {
  if (!API_BASE_URL) {
    throw new Error('API base URL is not configured.')
  }

  const response = await fetch(
    `${API_BASE_URL.replace(/\/$/, '')}/analyze`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ticker: request.ticker.trim().toUpperCase(),
      }),
    },
  )

  if (!response.ok) {
    let message = `Analysis failed (${response.status}).`

    try {
      const errorData = await response.json()
      message = errorData.detail || message
    } catch {
      // Keep the default error message.
    }

    throw new Error(message)
  }

  return response.json() as Promise<CompanyAnalysisResponse>
}
