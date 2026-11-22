
import {
  Activity,
  BarChart3,
  BookOpen,
  BriefcaseBusiness,
  ChevronDown,
  Clock3,
  FileText,
  LayoutDashboard,
  Search,
  Settings2,
  Sparkles,
} from 'lucide-react'

type SidebarProps = {
  activePage: string
  onNavigate: (page: string) => void
}

const Sidebar = ({ activePage, onNavigate }: SidebarProps) => {
  const researchItems = [
    { label: 'Research Reports', icon: FileText },
    { label: 'Market Overview', icon: LayoutDashboard },
  ]

  const agentItems = [
    { label: 'Company Analyst', icon: Search },
    { label: 'Comparison Agent', icon: BarChart3 },
    { label: 'Earnings Analyst', icon: Activity },
    { label: 'Portfolio Agent', icon: BriefcaseBusiness },
    { label: 'Earnings Q&A', icon: Sparkles },
    { label: 'Multi-Document RAG', icon: BookOpen },
  ]

  const workspaceItems = [
    { label: 'Saved Reports', icon: FileText },
    { label: 'Research History', icon: Clock3 },
  ]

  const renderItems = (
    items: { label: string; icon: typeof FileText }[],
  ) =>
    items.map(({ label, icon: Icon }) => (
      <button
        key={label}
        onClick={() => onNavigate(label)}
        className={`sidebar-link ${
          activePage === label ? 'active' : ''
        }`}
      >
        <Icon size={17} strokeWidth={1.8} />
        <span>{label}</span>
      </button>
    ))

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-icon">F</div>
        <div>
          <h2>FinSight</h2>
          <span>FINANCIAL INTELLIGENCE</span>
        </div>
      </div>

      <button className="workspace-selector">
        <div className="workspace-avatar">M</div>
        <div className="workspace-info">
          <strong>My Workspace</strong>
          <span>Personal workspace</span>
        </div>
        <ChevronDown size={15} />
      </button>

      <div className="sidebar-section">
        <p className="sidebar-heading">RESEARCH</p>
        {renderItems(researchItems)}
      </div>

      <div className="sidebar-section">
        <p className="sidebar-heading">AI WORKSPACE</p>
        {renderItems(agentItems)}
      </div>

      <div className="sidebar-section">
        <p className="sidebar-heading">PERSONAL</p>
        {renderItems(workspaceItems)}
      </div>

      <div className="sidebar-bottom">
        <button
          className={`sidebar-link ${
            activePage === 'Settings' ? 'active' : ''
          }`}
          onClick={() => onNavigate('Settings')}
        >
          <Settings2 size={17} strokeWidth={1.8} />
          <span>Settings</span>
        </button>

        <div className="sidebar-user">
          <div className="user-avatar">MA</div>
          <div>
            <strong>My Account</strong>
            <span>Personal plan</span>
          </div>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
