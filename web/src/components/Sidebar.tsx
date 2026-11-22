
import {
  BriefcaseBusiness,
  ChevronDown,
  House,
  LogOut,
  Search,
  Settings2,
} from 'lucide-react'

type SidebarProps = {
  activePage: string
  onNavigate: (page: string) => void
  userEmail: string
  onLogout: () => void
}

const Sidebar = ({
  activePage,
  onNavigate,
  userEmail,
  onLogout,
}: SidebarProps) => {
  const navigationItems = [
    { label: 'Home', page: 'Home', icon: House },
    { label: 'Research', page: 'Research Reports', icon: Search },
    { label: 'Portfolio', page: 'Portfolio', icon: BriefcaseBusiness },
  ]

  const initials = userEmail
    .split('@')[0]
    .slice(0, 2)
    .toUpperCase()

  const isActive = (page: string) => {
    if (page === 'Research Reports') {
      return (
        activePage === 'Research Reports' ||
        activePage === 'Company Analyst'
      )
    }

    return activePage === page
  }

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
        <div className="workspace-avatar">{initials}</div>

        <div className="workspace-info">
          <strong>My Workspace</strong>
          <span>Personal workspace</span>
        </div>

        <ChevronDown size={15} />
      </button>

      <div className="sidebar-section">
        <p className="sidebar-heading">WORKSPACE</p>

        {navigationItems.map(({ label, page, icon: Icon }) => (
          <button
            key={page}
            onClick={() => onNavigate(page)}
            className={`sidebar-link ${isActive(page) ? 'active' : ''}`}
          >
            <Icon size={17} strokeWidth={1.8} />
            <span>{label}</span>
          </button>
        ))}
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
          <div className="user-avatar">{initials}</div>
          <div className="sidebar-user-info">
            <strong>My Account</strong>
            <span title={userEmail}>{userEmail}</span>
          </div>

          <button
            className="icon-button sidebar-logout"
            onClick={onLogout}
            aria-label="Sign out"
            title="Sign out"
          >
            <LogOut size={16} />
          </button>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
