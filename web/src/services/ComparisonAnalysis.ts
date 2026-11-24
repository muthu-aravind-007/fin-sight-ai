import type {
  CompanyData,
  FinancialMetrics,
} from '../types/analysis'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export interface CompanyComparisonRequest {
  ticker1: string
  ticker2: string
}

export interface CompanyComparisonResponse {
  company1: CompanyData
  company2: CompanyData
  metrics1: FinancialMetrics
  metrics2: FinancialMetrics
  analysis: string
}

export async function compareCompanies(
  request: CompanyComparisonRequest,
): Promise<CompanyComparisonResponse> {
  if (!API_BASE_URL) {
    throw new Error('API base URL is not configured.')
  }

  const response = await fetch(
    `${API_BASE_URL.replace(/\/$/, '')}/compare`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ticker1: request.ticker1.trim().toUpperCase(),
        ticker2: request.ticker2.trim().toUpperCase(),
      }),
    },
  )

  if (!response.ok) {
    let message = `Comparison failed (${response.status}).`

    try {
      const errorData = await response.json()
      message = errorData.detail || message
    } catch {
      // Keep the default error message.
    }

    throw new Error(message)
  }

  return response.json() as Promise<CompanyComparisonResponse>
}
