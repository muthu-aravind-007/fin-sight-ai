
import { useState } from 'react'
import {
  Search,
  LoaderCircle,
  AlertCircle,
  Building2,
  Save,
  CheckCircle2,
} from 'lucide-react'

import { analyzeCompany } from '../services/CompanyAnalysis'
import { saveResearchReport } from '../services/reports'
import type { CompanyAnalysisResponse } from '../types/analysis'

function formatCurrency(
  value: number | null,
  divisor: number,
  suffix: string,
) {
  if (value === null || !Number.isFinite(value)) return 'N/A'

  return `$${(value / divisor).toFixed(2)} ${suffix}`
}

function CompanyAnalyst() {
  const [ticker, setTicker] = useState('NVDA')
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [saveError, setSaveError] = useState('')
  const [saveMessage, setSaveMessage] = useState('')
  const [savedReportId, setSavedReportId] = useState<string | null>(null)
  const [report, setReport] = useState<CompanyAnalysisResponse | null>(null)

  async function handleAnalyze(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    if (!ticker.trim()) {
      setError('Please enter a company ticker.')
      return
    }

    setLoading(true)
    setError('')
    setSaveError('')
    setSaveMessage('')
    setSavedReportId(null)
    setReport(null)

    try {
      const result = await analyzeCompany({ ticker })
      setReport(result)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to generate the company analysis.',
      )
    } finally {
      setLoading(false)
    }
  }

  async function handleSaveReport() {
    if (!report || savedReportId) return

    setSaving(true)
    setSaveError('')
    setSaveMessage('')

    try {
      const result = await saveResearchReport(ticker, report)

      setSavedReportId(result.id)
      setSaveMessage('Research report saved successfully.')
    } catch (err) {
      setSaveError(
        err instanceof Error
          ? err.message
          : 'Unable to save the research report.',
      )
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="analyst-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">AI RESEARCH WORKSPACE</p>
          <h1>Company Analyst</h1>
          <p className="page-description">
            Generate an AI-powered financial research report for any supported company.
          </p>
        </div>
      </div>

      <form className="analysis-search" onSubmit={handleAnalyze}>
        <div className="search-input-wrapper">
          <Search size={19} />
          <input
            value={ticker}
            onChange={(event) => setTicker(event.target.value)}
            placeholder="Enter company ticker (e.g. NVDA)"
            aria-label="Company ticker"
            disabled={loading}
          />
        </div>

        <button className="primary-button" type="submit" disabled={loading}>
          {loading ? (
            <>
              <LoaderCircle size={17} className="spin" />
              Analyzing...
            </>
          ) : (
            <>
              <Search size={17} />
              Generate Research
            </>
          )}
        </button>
      </form>

      {loading && (
        <div className="analysis-status">
          <LoaderCircle size={22} className="spin" />
          <div>
            <strong>Generating company research</strong>
            <p>
              Retrieving financial data and running the AI analysis workflow.
              This may take a little while.
            </p>
          </div>
        </div>
      )}

      {error && (
        <div className="analysis-error">
          <AlertCircle size={19} />
          <span>{error}</span>
        </div>
      )}

      {report && (
        <div className="research-result">
          <div className="company-overview">
            <div className="company-identity">
              <div className="company-icon">
                <Building2 size={23} />
              </div>
              <div>
                <p className="eyebrow">COMPANY RESEARCH REPORT</p>
                <h2>{report.company_data.name || ticker.toUpperCase()}</h2>
                <p className="company-description">
                  {[report.company_data.sector, report.company_data.industry]
                    .filter(Boolean)
                    .join(' · ') || 'Company information unavailable'}
                </p>
              </div>
            </div>
          </div>

          <div className="report-save-actions">
            <button
              className="primary-button"
              type="button"
              onClick={handleSaveReport}
              disabled={saving || savedReportId !== null}
            >
              {saving ? (
                <>
                  <LoaderCircle size={17} className="spin" />
                  Saving...
                </>
              ) : savedReportId ? (
                <>
                  <CheckCircle2 size={17} />
                  Saved
                </>
              ) : (
                <>
                  <Save size={17} />
                  Save Report
                </>
              )}
            </button>

            {saveMessage && (
              <p className="save-success">
                <CheckCircle2 size={15} />
                {saveMessage}
              </p>
            )}

            {saveError && (
              <p className="save-error">
                <AlertCircle size={15} />
                {saveError}
              </p>
            )}
          </div>

          <div className="financial-snapshot">
            <div className="financial-card">
              <span>Market Capitalization</span>
              <strong>
                {formatCurrency(
                  report.company_data.market_cap,
                  1_000_000_000_000,
                  'T',
                )}
              </strong>
            </div>

            <div className="financial-card">
              <span>P/E Ratio</span>
              <strong>
                {report.company_data.pe_ratio != null
                  ? report.company_data.pe_ratio.toFixed(2)
                  : 'N/A'}
              </strong>
            </div>

            <div className="financial-card">
              <span>Revenue</span>
              <strong>
                {formatCurrency(
                  report.company_data.revenue,
                  1_000_000_000,
                  'B',
                )}
              </strong>
            </div>
          </div>

          <section className="report-section">
            <div className="report-section-heading">
              <div>
                <p className="eyebrow">GENERATED ANALYSIS</p>
                <h2>Executive Research Report</h2>
              </div>
            </div>
            <div className="report-text">{report.analysis}</div>
          </section>

          <section className="report-section">
            <p className="eyebrow">SPECIALIST AGENT OUTPUTS</p>
            <h2>Financial Indicators</h2>

            <div className="metrics-grid">
              <div className="metric-card">
                <span>Analysis Score</span>
                <strong>{report.metrics.score}/6</strong>
              </div>
              <div className="metric-card">
                <span>Valuation</span>
                <strong>{report.metrics.valuation}</strong>
              </div>
              <div className="metric-card">
                <span>Revenue Scale</span>
                <strong>{report.metrics.growth}</strong>
              </div>
              <div className="metric-card">
                <span>Metric Risk Indicator</span>
                <strong>{report.metrics.risk}</strong>
              </div>
            </div>

            {report.metrics.insights.length > 0 && (
              <ul className="insights-list">
                {report.metrics.insights.map((insight, index) => (
                  <li key={index}>{insight}</li>
                ))}
              </ul>
            )}
          </section>

          <section className="report-section">
            <p className="eyebrow">AI SPECIALIST FINDINGS</p>
            <h2>Risk Assessment</h2>
            <div className="report-text">{report.risk_analysis}</div>
          </section>

          <section className="report-section">
            <h2>Investment Perspective</h2>
            <div className="report-text">{report.investment_analysis}</div>
          </section>

          <section className="report-section">
            <h2>News &amp; Sentiment</h2>
            <div className="report-text">{report.news_sentiment}</div>
          </section>

          <section className="report-section">
            <h2>Recent News</h2>
            {report.news.length > 0 ? (
              <ul className="news-list">
                {report.news.map((article, index) => (
                  <li key={index}>
                    {article.link ? (
                      <a href={article.link} target="_blank" rel="noreferrer">
                        {article.title || 'Untitled article'}
                      </a>
                    ) : (
                      article.title || 'Untitled article'
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="muted-text">No news articles were returned.</p>
            )}
          </section>
        </div>
      )}
    </div>
  )
}

export default CompanyAnalyst
