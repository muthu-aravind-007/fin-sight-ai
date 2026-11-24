
import {
  ArrowRight,
  BarChart3,
  Building2,
  Clock3,
  FileSearch,
  FileText,
  LockKeyhole,
} from 'lucide-react'

interface ResearchReportsProps {
  onNewResearch: () => void
  onViewHistory: () => void
  onCompanyComparison: () => void
}

const ResearchReports = ({
  onNewResearch,
  onViewHistory,
  onCompanyComparison,
}: ResearchReportsProps) => {
  const researchTasks = [
    {
      title: 'Company Research',
      description:
        'Explore a company’s financial performance, valuation, business outlook and risks.',
      icon: Building2,
      status: 'Available',
      active: true,
      action: onNewResearch,
    },
    {
      title: 'Company Comparison',
      description:
        'Compare companies across financial performance, valuation and fundamentals.',
      icon: BarChart3,
      status: 'Available',
      active: true,
      action: onCompanyComparison,
    },
    {
      title: 'Earnings Analysis',
      description:
        'Understand earnings results, management commentary and financial guidance.',
      icon: FileSearch,
      status: 'Coming soon',
      active: false,
    },
    {
      title: 'Document Research',
      description:
        'Explore financial documents and ask questions using their contents.',
      icon: FileText,
      status: 'Coming soon',
      active: false,
    },
  ]

  return (
    <div className="reports-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">FINANCIAL INTELLIGENCE</p>
          <h1>Research</h1>
          <p className="page-description">
            Research companies, evaluate opportunities and understand financial information.
          </p>
        </div>
      </div>

      <section className="research-workspace">
        <div className="research-section-heading">
          <div>
            <h2>What would you like to research?</h2>
            <p>Choose a financial research task to get started.</p>
          </div>
        </div>

        <div className="research-task-grid">
          {researchTasks.map((task) => {
            const Icon = task.icon

            return (
              <button
                key={task.title}
                className={`research-task-card ${
                  task.active ? 'task-available' : 'task-disabled'
                }`}
                onClick={task.action}
                disabled={!task.active}
              >
                <div className="research-task-top">
                  <div className="research-task-icon">
                    <Icon size={21} strokeWidth={1.7} />
                  </div>

                  <span
                    className={`task-status ${
                      task.active ? 'status-available' : ''
                    }`}
                  >
                    {task.status}
                  </span>
                </div>

                <div className="research-task-content">
                  <h3>{task.title}</h3>
                  <p>{task.description}</p>
                </div>

                <div className="research-task-footer">
                  {task.active ? (
                    <>
                      <span>Start research</span>
                      <ArrowRight size={16} />
                    </>
                  ) : (
                    <>
                      <span>In development</span>
                      <LockKeyhole size={14} />
                    </>
                  )}
                </div>
              </button>
            )
          })}
        </div>
      </section>

      <section className="recent-research">
        <div className="research-section-heading">
          <div>
            <h2>Recent research</h2>
            <p>Continue exploring your previous research.</p>
          </div>

                    <button
                      className="recent-count"
                      onClick={onViewHistory}
                    >
                      View all <ArrowRight size={14} />
          </button>
        </div>

        <div className="recent-empty-state">
          <div className="recent-empty-icon">
            <Clock3 size={21} />
          </div>
          <h3>No research yet</h3>
          <p>
            Your generated research reports will appear here.
          </p>
        </div>
      </section>
    </div>
  )
}

export default ResearchReports
