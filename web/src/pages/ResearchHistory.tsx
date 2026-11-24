
import { useEffect, useState } from 'react'
import {
  ArrowLeft,
  Clock3,
  FileText,
  LoaderCircle,
  AlertCircle,
  Trash2,
} from 'lucide-react'

import {
  getSavedReports,
  getSavedReport,
  deleteSavedReport,
} from '../services/reports'

import type {
  SavedResearchReport,
  SavedResearchReportDetail,
} from '../services/reports'

import type { CompanyAnalysisResponse } from '../types/analysis'

interface ResearchHistoryProps {
  onBack: () => void
}

function ResearchHistory({ onBack }: ResearchHistoryProps) {
  const [reports, setReports] = useState<SavedResearchReport[]>([])
  const [selectedReport, setSelectedReport] =
    useState<SavedResearchReportDetail | null>(null)

  const [loading, setLoading] = useState(true)
  const [detailLoading, setDetailLoading] = useState(false)
  const [error, setError] = useState('')
  const [deletingId, setDeletingId] = useState<string | null>(null)

  async function loadReports() {
    setLoading(true)
    setError('')

    try {
      const result = await getSavedReports()
      setReports(result)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Unable to load research history.',
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void loadReports()
  }, [])

  async function handleOpenReport(reportId: string) {
    setDetailLoading(true)
    setError('')

    try {
      const result = await getSavedReport(reportId)
      setSelectedReport(result)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Unable to open this report.',
      )
    } finally {
      setDetailLoading(false)
    }
  }

  async function handleDeleteReport(reportId: string) {
    const confirmed = window.confirm(
      'Are you sure you want to delete this research report?',
    )

    if (!confirmed) return

    setDeletingId(reportId)
    setError('')

    try {
      await deleteSavedReport(reportId)
      setReports((current) =>
        current.filter((report) => report.id !== reportId),
      )

      if (selectedReport?.id === reportId) {
        setSelectedReport(null)
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Unable to delete this report.',
      )
    } finally {
      setDeletingId(null)
    }
  }

  function formatDate(date: string) {
    return new Date(date).toLocaleString()
  }

  if (
    selectedReport &&
    'report_type' in selectedReport.report_data &&
    selectedReport.report_data.report_type === 'comparison'
  ) {
    const report = selectedReport.report_data

    return (
      <div className="analyst-page">
        <button
          className="secondary-button"
          onClick={() => setSelectedReport(null)}
        >
          <ArrowLeft size={16} />
          Back to history
        </button>

        <div className="page-heading">
          <div>
            <p className="eyebrow">SAVED COMPARISON</p>
            <h1>{report.ticker1} vs {report.ticker2}</h1>
            <p className="page-description">
              Saved {formatDate(selectedReport.created_at)}
            </p>
          </div>
        </div>

        <div className="comparison-company-grid">
          {[ 
            { ticker: report.ticker1, company: report.company1, metrics: report.metrics1 },
            { ticker: report.ticker2, company: report.company2, metrics: report.metrics2 },
          ].map(({ ticker, company, metrics }) => (
            <div className="comparison-company-card" key={ticker}>
              <div className="company-identity">
                <div className="company-icon">
                  <FileText size={22} />
                </div>
                <div>
                  <p className="eyebrow">{ticker}</p>
                  <h2>{company.name || ticker}</h2>
                  <p className="company-description">
                    {[company.sector, company.industry]
                      .filter(Boolean)
                      .join(' · ') || 'Company information unavailable'}
                  </p>
                </div>
              </div>

              <div className="comparison-financials">
                <div className="comparison-financial-item">
                  <span>Market Capitalization</span>
                  <strong>
                    {company.market_cap != null
                      ? `$${(company.market_cap / 1_000_000_000_000).toFixed(2)} T`
                      : 'N/A'}
                  </strong>
                </div>

                <div className="comparison-financial-item">
                  <span>P/E Ratio</span>
                  <strong>{company.pe_ratio?.toFixed(2) ?? 'N/A'}</strong>
                </div>

                <div className="comparison-financial-item">
                  <span>Revenue</span>
                  <strong>
                    {company.revenue != null
                      ? `$${(company.revenue / 1_000_000_000).toFixed(2)} B`
                      : 'N/A'}
                  </strong>
                </div>
              </div>

              <div className="comparison-metrics">
                <p className="eyebrow">FINANCIAL INDICATORS</p>

                {[
                  ['Analysis Score', metrics.score ?? 'Not Scored'],
                  ['Valuation', metrics.valuation],
                  ['Growth', metrics.growth],
                  ['Revenue Scale', metrics.revenue_scale],
                  ['Risk Indicator', metrics.risk],
                ].map(([label, value]) => (
                  <div className="comparison-metric-row" key={label}>
                    <span>{label}</span>
                    <strong>{value}</strong>
                  </div>
                ))}

                {metrics.insights.length > 0 && (
                  <ul className="insights-list">
                    {metrics.insights.map((insight, index) => (
                      <li key={index}>{insight}</li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          ))}
        </div>

        <section className="report-section">
          <p className="eyebrow">AI-GENERATED COMPARISON</p>
          <h2>Comparative Analysis &amp; Recommendation</h2>
          <div className="report-text">{report.analysis}</div>
        </section>
      </div>
    )
  }

  if (selectedReport) {
    const report = selectedReport.report_data as CompanyAnalysisResponse
    const company = report.company_data

    return (
      <div className="analyst-page">
        <button
          className="secondary-button"
          onClick={() => setSelectedReport(null)}
        >
          <ArrowLeft size={16} />
          Back to history
        </button>

        <div className="page-heading">
          <div>
            <p className="eyebrow">SAVED RESEARCH REPORT</p>
            <h1>{company.name || selectedReport.ticker}</h1>
            <p className="page-description">
              {selectedReport.ticker} · Saved {formatDate(selectedReport.created_at)}
            </p>
          </div>
        </div>

        <div className="financial-snapshot">
          <div className="financial-card">
            <span>Market Capitalization</span>
            <strong>
              {company.market_cap != null
                ? `$${(company.market_cap / 1_000_000_000_000).toFixed(2)} T`
                : 'N/A'}
            </strong>
          </div>

          <div className="financial-card">
            <span>P/E Ratio</span>
            <strong>{company.pe_ratio?.toFixed(2) ?? 'N/A'}</strong>
          </div>

          <div className="financial-card">
            <span>Revenue</span>
            <strong>
              {company.revenue != null
                ? `$${(company.revenue / 1_000_000_000).toFixed(2)} B`
                : 'N/A'}
            </strong>
          </div>
        </div>

        <section className="report-section">
          <p className="eyebrow">GENERATED ANALYSIS</p>
          <h2>Executive Research Report</h2>
          <div className="report-text">{report.analysis}</div>
        </section>

        <section className="report-section">
          <p className="eyebrow">SPECIALIST AGENT OUTPUTS</p>
          <h2>Financial Indicators</h2>

          <div className="metrics-grid">
            <div className="metric-card">
              <span>Analysis Score</span>
              <strong>{report.metrics.score ?? 'Not Scored'}</strong>
            </div>

            <div className="metric-card">
              <span>Valuation</span>
              <strong>{report.metrics.valuation}</strong>
            </div>

            <div className="metric-card">
              <span>Revenue Scale</span>
              <strong>{report.metrics.revenue_scale}</strong>
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
    )
  }

  return (
    <div className="reports-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">YOUR WORKSPACE</p>
          <h1>Research History</h1>
          <p className="page-description">
            Access and manage your previously saved research reports.
          </p>
        </div>

        <button className="secondary-button" onClick={onBack}>
          <ArrowLeft size={16} />
          Back to Research
        </button>
      </div>

      {error && (
        <div className="analysis-error">
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {loading || detailLoading ? (
        <div className="analysis-status">
          <LoaderCircle size={22} className="spin" />
          <div>
            <strong>
              {loading ? 'Loading research history' : 'Opening research report'}
            </strong>
          </div>
        </div>
      ) : reports.length === 0 ? (
        <div className="recent-empty-state">
          <div className="recent-empty-icon">
            <Clock3 size={21} />
          </div>
          <h3>No saved reports yet</h3>
          <p>Your saved company research reports will appear here.</p>
        </div>
      ) : (
        <div className="research-history-list">
          {reports.map((report) => (
            <div className="research-history-card" key={report.id}>
              <div className="research-history-icon">
                <FileText size={21} />
              </div>

              <div className="research-history-info">
                <h3>{report.company_name || report.ticker}</h3>
                <p>{report.ticker}</p>
                <span>{formatDate(report.created_at)}</span>
              </div>

              <div className="research-history-actions">
                <button
                  className="secondary-button"
                  onClick={() => handleOpenReport(report.id)}
                >
                  Open report
                </button>

                <button
                  className="icon-button"
                  aria-label={`Delete ${report.ticker} report`}
                  title="Delete report"
                  disabled={deletingId === report.id}
                  onClick={() => handleDeleteReport(report.id)}
                >
                  {deletingId === report.id ? (
                    <LoaderCircle size={17} className="spin" />
                  ) : (
                    <Trash2 size={17} />
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default ResearchHistory
