
import { useState, type FormEvent } from 'react'
import {
  ArrowLeftRight,
  BarChart3,
  Building2,
  LoaderCircle,
  AlertCircle,
  Search,
} from 'lucide-react'

import { compareCompanies } from '../services/ComparisonAnalysis'
import type { CompanyComparisonResponse } from '../services/ComparisonAnalysis'

function formatCurrency(
  value: number | null,
  divisor: number,
  suffix: string,
) {
  if (value === null || !Number.isFinite(value)) return 'N/A'

  return `$${(value / divisor).toFixed(2)} ${suffix}`
}

function CompanySnapshot({
  company,
  metrics,
  ticker,
}: {
  company: CompanyComparisonResponse['company1']
  metrics: CompanyComparisonResponse['metrics1']
  ticker: string
}) {
  return (
    <div className="comparison-company-card">
      <div className="company-identity">
        <div className="company-icon">
          <Building2 size={22} />
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
            {formatCurrency(company.market_cap, 1_000_000_000_000, 'T')}
          </strong>
        </div>

        <div className="comparison-financial-item">
          <span>P/E Ratio</span>
          <strong>{company.pe_ratio?.toFixed(2) ?? 'N/A'}</strong>
        </div>

        <div className="comparison-financial-item">
          <span>Revenue</span>
          <strong>
            {formatCurrency(company.revenue, 1_000_000_000, 'B')}
          </strong>
        </div>
      </div>

      <div className="comparison-metrics">
        <p className="eyebrow">FINANCIAL INDICATORS</p>

        <div className="comparison-metric-row">
          <span>Analysis Score</span>
          <strong>{metrics.score ?? 'Not Scored'}</strong>
        </div>

        <div className="comparison-metric-row">
          <span>Valuation</span>
          <strong>{metrics.valuation}</strong>
        </div>

        <div className="comparison-metric-row">
          <span>Growth</span>
          <strong>{metrics.growth}</strong>
        </div>

        <div className="comparison-metric-row">
          <span>Revenue Scale</span>
          <strong>{metrics.revenue_scale}</strong>
        </div>

        <div className="comparison-metric-row">
          <span>Risk Indicator</span>
          <strong>{metrics.risk}</strong>
        </div>

        {metrics.insights.length > 0 && (
          <ul className="insights-list">
            {metrics.insights.map((insight, index) => (
              <li key={index}>{insight}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

function ComparisonAgent() {
  const [ticker1, setTicker1] = useState('NVDA')
  const [ticker2, setTicker2] = useState('AMD')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [comparison, setComparison] =
    useState<CompanyComparisonResponse | null>(null)

  async function handleCompare(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const first = ticker1.trim().toUpperCase()
    const second = ticker2.trim().toUpperCase()

    if (!first || !second) {
      setError('Please enter both company ticker symbols.')
      return
    }

    if (first === second) {
      setError('Please enter two different company tickers.')
      return
    }

    setLoading(true)
    setError('')
    setComparison(null)

    try {
      const result = await compareCompanies({
        ticker1: first,
        ticker2: second,
      })

      setComparison(result)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to compare these companies.',
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="analyst-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">AI RESEARCH WORKSPACE</p>
          <h1>Company Comparison</h1>
          <p className="page-description">
            Compare two companies across financial performance, valuation,
            growth and risk.
          </p>
        </div>
      </div>

      <form className="comparison-search" onSubmit={handleCompare}>
        <div className="comparison-input-group">
          <label htmlFor="ticker-one">First company</label>
          <div className="search-input-wrapper">
            <Search size={18} />
            <input
              id="ticker-one"
              value={ticker1}
              onChange={(event) => setTicker1(event.target.value)}
              placeholder="e.g. NVDA"
              disabled={loading}
            />
          </div>
        </div>

        <div className="comparison-vs">VS</div>

        <div className="comparison-input-group">
          <label htmlFor="ticker-two">Second company</label>
          <div className="search-input-wrapper">
            <Search size={18} />
            <input
              id="ticker-two"
              value={ticker2}
              onChange={(event) => setTicker2(event.target.value)}
              placeholder="e.g. AMD"
              disabled={loading}
            />
          </div>
        </div>

        <button
          className="primary-button"
          type="submit"
          disabled={loading}
        >
          {loading ? (
            <>
              <LoaderCircle size={17} className="spin" />
              Comparing...
            </>
          ) : (
            <>
              <ArrowLeftRight size={17} />
              Compare Companies
            </>
          )}
        </button>
      </form>

      {loading && (
        <div className="analysis-status">
          <LoaderCircle size={22} className="spin" />
          <div>
            <strong>Comparing companies</strong>
            <p>
              Retrieving financial data and generating the comparison.
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

      {comparison && (
        <div className="comparison-results">
          <div className="comparison-results-heading">
            <div>
              <p className="eyebrow">FINANCIAL COMPARISON</p>
              <h2>
                {ticker1.toUpperCase()} vs {ticker2.toUpperCase()}
              </h2>
            </div>
          </div>

          <div className="comparison-company-grid">
            <CompanySnapshot
              company={comparison.company1}
              metrics={comparison.metrics1}
              ticker={ticker1.trim().toUpperCase()}
            />

            <CompanySnapshot
              company={comparison.company2}
              metrics={comparison.metrics2}
              ticker={ticker2.trim().toUpperCase()}
            />
          </div>

          <section className="report-section">
            <p className="eyebrow">AI-GENERATED COMPARISON</p>
            <h2>Comparative Analysis &amp; Recommendation</h2>
            <div className="report-text">{comparison.analysis}</div>
          </section>
        </div>
      )}

      {!comparison && !loading && !error && (
        <div className="comparison-empty-state">
          <div className="recent-empty-icon">
            <BarChart3 size={22} />
          </div>
          <h3>Compare companies side by side</h3>
          <p>
            Enter two ticker symbols to explore their financial performance,
            valuation, growth and risk indicators.
          </p>
        </div>
      )}
    </div>
  )
}

export default ComparisonAgent
