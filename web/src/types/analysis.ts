
export interface CompanyData {
  name: string | null
  sector: string | null
  industry: string | null
  market_cap: number | null
  pe_ratio: number | null
  revenue: number | null
}

export interface FinancialMetrics {
  score: number
  valuation: string
  growth: string
  risk: string
  insights: string[]
}

export interface NewsArticle {
  title?: string
  publisher?: string
  link?: string
  published?: string
  [key: string]: unknown
}

export interface CompanyAnalysisResponse {
  company_data: CompanyData
  metrics: FinancialMetrics
  news: NewsArticle[]
  news_sentiment: string
  risk_analysis: string
  investment_analysis: string
  analysis: string
}

export interface CompanyAnalysisRequest {
  ticker: string
}
