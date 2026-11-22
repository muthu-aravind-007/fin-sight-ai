import { supabase } from './supabase'
import type { CompanyAnalysisResponse } from '../types/analysis'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

interface SaveReportResponse {
  id: string
  ticker: string
  company_name: string | null
  created_at: string
}

export async function saveResearchReport(
  ticker: string,
  report: CompanyAnalysisResponse,
): Promise<SaveReportResponse> {
  if (!API_BASE_URL) {
    throw new Error('API base URL is not configured.')
  }

  const {
    data: { session },
    error: sessionError,
  } = await supabase.auth.getSession()

  if (sessionError || !session?.access_token) {
    throw new Error('Your session has expired. Please sign in again.')
  }

  const response = await fetch(
    `${API_BASE_URL.replace(/\/$/, '')}/reports`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${session.access_token}`,
      },
      body: JSON.stringify({
        ticker: ticker.trim().toUpperCase(),
        company_name: report.company_data.name,
        report_data: report,
      }),
    },
  )

  if (!response.ok) {
    let message = `Unable to save report (${response.status}).`

    try {
      const errorData = await response.json()
      message = errorData.detail || message
    } catch {
      // Keep the default error message.
    }

    throw new Error(message)
  }

  const data = await response.json()

  return Array.isArray(data) ? data[0] : data
}