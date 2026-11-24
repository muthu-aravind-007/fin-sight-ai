import { useState, type FormEvent } from 'react'
import {
  FileText,
  LoaderCircle,
  AlertCircle,
  Search,
  RotateCcw,
} from 'lucide-react'

import { analyzeEarnings } from '../services/EarningsAnalysis'

function EarningsAnalysis() {
  const [transcript, setTranscript] = useState('')
  const [analysis, setAnalysis] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleAnalyze(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    if (!transcript.trim()) {
      setError('Please paste an earnings-call transcript.')
      return
    }

    setLoading(true)
    setError('')
    setAnalysis('')

    try {
      const result = await analyzeEarnings({ transcript })
      setAnalysis(result.analysis)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to analyze this earnings transcript.',
      )
    } finally {
      setLoading(false)
    }
  }

  function handleReset() {
    setTranscript('')
    setAnalysis('')
    setError('')
  }

  return (
    <div className="analyst-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">AI RESEARCH WORKSPACE</p>
          <h1>Earnings Analysis</h1>
          <p className="page-description">
            Analyze earnings-call transcripts to explore company performance,
            management commentary and financial outlook.
          </p>
        </div>
      </div>

      <form className="comparison-search" onSubmit={handleAnalyze}>
        <div className="comparison-input-group" style={{ width: '100%' }}>
          <label htmlFor="earnings-transcript">
            Earnings-call transcript
          </label>

          <textarea
            id="earnings-transcript"
            value={transcript}
            onChange={(event) => setTranscript(event.target.value)}
            placeholder="Paste the earnings-call transcript here..."
            rows={12}
            disabled={loading}
            style={{
              width: '100%',
              resize: 'vertical',
              padding: '16px',
              background: '#141414',
              color: '#F5F5F5',
              border: '1px solid #292929',
              borderRadius: '10px',
              font: 'inherit',
            }}
          />
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            className="primary-button"
            type="submit"
            disabled={loading || !transcript.trim()}
          >
            {loading ? (
              <>
                <LoaderCircle size={17} className="spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Search size={17} />
                Analyze Earnings
              </>
            )}
          </button>

          <button
            className="secondary-button"
            type="button"
            onClick={handleReset}
            disabled={loading}
          >
            <RotateCcw size={16} />
            Reset
          </button>
        </div>
      </form>

      {loading && (
        <div className="analysis-status">
          <LoaderCircle size={22} className="spin" />
          <div>
            <strong>Analyzing earnings transcript</strong>
            <p>
              Processing the transcript and generating your analysis.
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

      {analysis && (
        <section className="report-section">
          <p className="eyebrow">EARNINGS REPORT</p>
          <h2>Generated Earnings Analysis</h2>

          <div className="report-text">{analysis}</div>
        </section>
      )}

      {!analysis && !loading && !error && (
        <div className="comparison-empty-state">
          <div className="recent-empty-icon">
            <FileText size={22} />
          </div>
          <h3>Analyze an earnings call</h3>
          <p>
            Paste an earnings-call transcript to generate your analysis.
          </p>
        </div>
      )}
    </div>
  )
}

export default EarningsAnalysis