
import { useState, type FormEvent } from 'react'
import {
  FileText,
  Upload,
  LoaderCircle,
  AlertCircle,
  Search,
  RotateCcw,
  X,
} from 'lucide-react'

import {
  analyzeDocuments,
  type DocumentResearchFile,
  type DocumentResearchResponse,
} from '../services/DocumentResearch'

function DocumentResearch() {
  const [documents, setDocuments] = useState<DocumentResearchFile[]>([])
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState<DocumentResearchResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  function handleFileSelection(files: FileList | null) {
    if (!files) return

    const selectedFiles = Array.from(files)

    const invalidFile = selectedFiles.find(
      (file) => !file.name.toLowerCase().endsWith('.pdf'),
    )

    if (invalidFile) {
      setError('Only PDF files are supported.')
      return
    }

    setError('')

    setDocuments((current) => [
      ...current,
      ...selectedFiles.map((file) => ({
        file,
        company: '',
        quarter: '',
      })),
    ])

    setResult(null)
  }

  function updateDocument(
    index: number,
    field: 'company' | 'quarter',
    value: string,
  ) {
    setDocuments((current) =>
      current.map((document, documentIndex) =>
        documentIndex === index
          ? { ...document, [field]: value }
          : document,
      ),
    )
  }

  function removeDocument(index: number) {
    setDocuments((current) =>
      current.filter((_, documentIndex) => documentIndex !== index),
    )
    setResult(null)
  }

  async function handleAnalyze(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    if (!documents.length) {
      setError('Please upload at least one PDF.')
      return
    }

    if (
      documents.some(
        (document) => !document.company.trim() || !document.quarter.trim(),
      )
    ) {
      setError('Please provide a company and quarter for every document.')
      return
    }

    if (!question.trim()) {
      setError('Please enter a research question.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await analyzeDocuments({
        documents,
        question,
      })

      setResult(response)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to analyze the uploaded documents.',
      )
    } finally {
      setLoading(false)
    }
  }

  function handleReset() {
    setDocuments([])
    setQuestion('')
    setResult(null)
    setError('')
  }

  return (
    <div className="analyst-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">AI RESEARCH WORKSPACE</p>
          <h1>Document Research</h1>
          <p className="page-description">
            Upload financial documents and ask questions across their contents.
          </p>
        </div>
      </div>

      <form className="comparison-search" onSubmit={handleAnalyze}>
        <div className="comparison-input-group">
          <label htmlFor="document-upload">Financial documents (PDF)</label>

          <label
            htmlFor="document-upload"
            className="secondary-button"
            style={{
              display: 'inline-flex',
              width: 'fit-content',
              cursor: 'pointer',
              marginTop: '8px',
            }}
          >
            <Upload size={17} />
            Upload PDF files
          </label>

          <input
            id="document-upload"
            type="file"
            accept=".pdf,application/pdf"
            multiple
            onChange={(event) => {
              handleFileSelection(event.target.files)
              event.target.value = ''
            }}
            disabled={loading}
            style={{ display: 'none' }}
          />
        </div>

        {documents.length > 0 && (
          <div style={{ display: 'grid', gap: '14px', marginTop: '18px' }}>
            {documents.map((document, index) => (
              <div
                key={`${document.file.name}-${index}`}
                style={{
                  padding: '16px',
                  border: '1px solid #292929',
                  borderRadius: '10px',
                  background: '#141414',
                }}
              >
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    gap: '12px',
                    marginBottom: '14px',
                  }}
                >
                  <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                    <FileText size={19} />
                    <span>{document.file.name}</span>
                  </div>

                  <button
                    type="button"
                    className="secondary-button"
                    onClick={() => removeDocument(index)}
                    disabled={loading}
                    aria-label={`Remove ${document.file.name}`}
                  >
                    <X size={16} />
                  </button>
                </div>

                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                    gap: '12px',
                  }}
                >
                  <div className="comparison-input-group">
                    <label htmlFor={`company-${index}`}>Company / ticker</label>
                    <input
                      id={`company-${index}`}
                      type="text"
                      value={document.company}
                      onChange={(event) =>
                        updateDocument(index, 'company', event.target.value)
                      }
                      placeholder="e.g. NVDA"
                      disabled={loading}
                    />
                  </div>

                  <div className="comparison-input-group">
                    <label htmlFor={`quarter-${index}`}>Quarter / period</label>
                    <input
                      id={`quarter-${index}`}
                      type="text"
                      value={document.quarter}
                      onChange={(event) =>
                        updateDocument(index, 'quarter', event.target.value)
                      }
                      placeholder="e.g. Q3 2026"
                      disabled={loading}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        <div
          className="comparison-input-group"
          style={{ width: '100%', marginTop: '22px' }}
        >
          <label htmlFor="document-question">Research question</label>
          <textarea
            id="document-question"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask a question about the uploaded financial documents..."
            rows={5}
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

        <div style={{ display: 'flex', gap: '12px', marginTop: '18px' }}>
          <button
            className="primary-button"
            type="submit"
            disabled={loading || !documents.length || !question.trim()}
          >
            {loading ? (
              <>
                <LoaderCircle size={17} className="spin" />
                Analyzing documents...
              </>
            ) : (
              <>
                <Search size={17} />
                Analyze Documents
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
            <strong>Researching your documents</strong>
            <p>Extracting and analyzing document contents. This may take a while.</p>
          </div>
        </div>
      )}

      {error && (
        <div className="analysis-error">
          <AlertCircle size={19} />
          <span>{error}</span>
        </div>
      )}

      {result && (
        <section className="report-section">
          <p className="eyebrow">DOCUMENT RESEARCH REPORT</p>
          <h2>Research Results</h2>

          <div className="report-text">{result.answer}</div>

          {result.companies_used?.length > 0 && (
            <div style={{ marginTop: '20px' }}>
              <strong>Companies covered</strong>
              <p>{result.companies_used.join(', ')}</p>
            </div>
          )}

          {result.sources?.length > 0 && (
            <div style={{ marginTop: '20px' }}>
              <strong>Retrieved sources</strong>
              <div style={{ display: 'grid', gap: '10px', marginTop: '12px' }}>
                {result.sources.map((source, index) => (
                  <div
                    key={index}
                    style={{
                      padding: '12px',
                      background: '#141414',
                      border: '1px solid #292929',
                      borderRadius: '8px',
                    }}
                  >
                    <pre style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere' }}>
                      {JSON.stringify(source, null, 2)}
                    </pre>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>
      )}

      {!result && !loading && !error && (
        <div className="comparison-empty-state">
          <div className="recent-empty-icon">
            <FileText size={22} />
          </div>
          <h3>Research your financial documents</h3>
          <p>
            Upload one or more PDFs, identify their company and reporting period,
            then ask a question.
          </p>
        </div>
      )}
    </div>
  )
}

export default DocumentResearch
