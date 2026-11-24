
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export interface DocumentResearchFile {
  file: File
  company: string
  quarter: string
}

export interface DocumentResearchRequest {
  documents: DocumentResearchFile[]
  question: string
}

export interface DocumentResearchResponse {
  answer: string
  context: string
  sources: Array<Record<string, unknown>>
  companies_used: string[]
  retrieved_companies: string[]
  missing_companies: string[]
}

export async function analyzeDocuments(
  request: DocumentResearchRequest,
): Promise<DocumentResearchResponse> {
  if (!API_BASE_URL) {
    throw new Error('API base URL is not configured.')
  }

  if (!request.documents.length) {
    throw new Error('Please upload at least one PDF.')
  }

  if (!request.question.trim()) {
    throw new Error('Please enter a research question.')
  }

  const formData = new FormData()

  request.documents.forEach((document) => {
    formData.append('files', document.file)
  })

  formData.append(
    'documents',
    JSON.stringify(
      request.documents.map((document) => ({
        company: document.company.trim(),
        quarter: document.quarter.trim(),
      })),
    ),
  )

  formData.append('question', request.question.trim())

  const response = await fetch(
    `${API_BASE_URL.replace(/\/$/, '')}/multi-rag/upload`,
    {
      method: 'POST',
      body: formData,
    },
  )

  if (!response.ok) {
    let message = `Document research failed (${response.status}).`

    try {
      const errorData = await response.json()
      message = errorData.detail || message
    } catch {
      // Keep the default error message.
    }

    throw new Error(message)
  }

  return response.json() as Promise<DocumentResearchResponse>
}
