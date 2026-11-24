import { supabase } from './supabase'
import type { CompanyAnalysisResponse } from '../types/analysis'
import type { CompanyComparisonResponse } from './ComparisonAnalysis'

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

export async function saveComparisonReport(
  ticker1: string,
  ticker2: string,
  report: CompanyComparisonResponse,
): Promise<SaveReportResponse> {
  if (!API_BASE_URL) {
    throw new Error('API base URL is not configured.')
  }

  const headers = await getAuthenticatedHeaders()

  const firstTicker = ticker1.trim().toUpperCase()
  const secondTicker = ticker2.trim().toUpperCase()

  const response = await fetch(
    `${API_BASE_URL.replace(/\/$/, '')}/reports`,
    {
      method: 'POST',
      headers,
      body: JSON.stringify({
        ticker: `${firstTicker} vs ${secondTicker}`,
        company_name: `${report.company1.name || firstTicker} vs ${report.company2.name || secondTicker}`,
        report_data: {
          report_type: 'comparison',
          ticker1: firstTicker,
          ticker2: secondTicker,
          ...report,
        },
      }),
    },
  )

  if (!response.ok) {
    let message = `Unable to save comparison (${response.status}).`

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


export interface SavedResearchReport {
  id: string
  ticker: string
  company_name: string | null
  created_at: string
  updated_at?: string | null
}

export interface SavedComparisonReportData
  extends CompanyComparisonResponse {
  report_type: 'comparison'
  ticker1: string
  ticker2: string
}

export interface SavedResearchReportDetail
  extends SavedResearchReport {
  report_data: CompanyAnalysisResponse | SavedComparisonReportData
}

async function getAuthenticatedHeaders() {
  const {
    data: { session },
    error,
  } = await supabase.auth.getSession()

  if (error || !session?.access_token) {
    throw new Error('Your session has expired. Please sign in again.')
  }

  return {
    Authorization: `Bearer ${session.access_token}`,
    'Content-Type': 'application/json',
  }
}

export async function getSavedReports(): Promise<SavedResearchReport[]> {
  if (!API_BASE_URL) {
    throw new Error('API base URL is not configured.')
  }

  const headers = await getAuthenticatedHeaders()

  const response = await fetch(
    `${API_BASE_URL.replace(/\/$/, '')}/reports`,
    { headers },
  )

  if (!response.ok) {
    throw new Error(`Unable to load reports (${response.status}).`)
  }

  return response.json()
}

export async function getSavedReport(
  reportId: string,
): Promise<SavedResearchReportDetail> {
  if (!API_BASE_URL) {
    throw new Error('API base URL is not configured.')
  }

  const headers = await getAuthenticatedHeaders()

  const response = await fetch(
    `${API_BASE_URL.replace(/\/$/, '')}/reports/${reportId}`,
    { headers },
  )

  if (!response.ok) {
    throw new Error(`Unable to load report (${response.status}).`)
  }

  return response.json()
}

export async function deleteSavedReport(
  reportId: string,
): Promise<void> {
  if (!API_BASE_URL) {
    throw new Error('API base URL is not configured.')
  }

  const headers = await getAuthenticatedHeaders()

  const response = await fetch(
    `${API_BASE_URL.replace(/\/$/, '')}/reports/${reportId}`,
    {
      method: 'DELETE',
      headers,
    },
  )

  if (!response.ok) {
    throw new Error(`Unable to delete report (${response.status}).`)
  }
}
