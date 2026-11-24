const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export interface EarningsAnalysisRequest {
  transcript: string
}

export interface EarningsAnalysisResponse {
  analysis: string
}

export async function analyzeEarnings(
  request: EarningsAnalysisRequest,
): Promise<EarningsAnalysisResponse> {
  if (!API_BASE_URL) {
    throw new Error('API base URL is not configured.')
  }

  if (!request.transcript.trim()) {
    throw new Error('Please provide an earnings-call transcript.')
  }

  const response = await fetch(
    `${API_BASE_URL.replace(/\/$/, '')}/earnings`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        transcript: request.transcript.trim(),
      }),
    },
  )

  if (!response.ok) {
    let message = `Earnings analysis failed (${response.status}).`

    try {
      const errorData = await response.json()
      message = errorData.detail || message
    } catch {
      // Keep the default error message.
    }

    throw new Error(message)
  }

  return response.json() as Promise<EarningsAnalysisResponse>
}