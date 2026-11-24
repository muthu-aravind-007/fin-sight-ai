
import { useEffect, useState } from 'react'
import { Bell, Search } from 'lucide-react'

import Sidebar from './components/Sidebar'
import Auth from './pages/Auth'
import CompanyAnalyst from './pages/CompanyAnalyst'
import ResearchReports from './pages/ResearchReports'
import ResearchHistory from './pages/ResearchHistory'
import ComparisonAgent from './pages/ComparisonAgent'
import EarningsAnalysis from './pages/EarningsAnalysis'
import DocumentResearch from './pages/DocumentResearch'
import { supabase } from './services/supabase'

import './App.css'

function App() {
  const [activePage, setActivePage] = useState('Research Reports')
  const [userEmail, setUserEmail] = useState<string | null>(null)
  const [checkingSession, setCheckingSession] = useState(true)

  useEffect(() => {
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUserEmail(session?.user.email ?? null)
      setCheckingSession(false)
    })

    supabase.auth.getSession().then(({ data, error }) => {
      if (error) {
        console.error('Session check failed:', error.message)
      }

      setUserEmail(data.session?.user.email ?? null)
      setCheckingSession(false)
    })

    return () => {
      subscription.unsubscribe()
    }
  }, [])

  const handleLogout = async () => {
    const { error } = await supabase.auth.signOut()

    if (error) {
      console.error('Sign out failed:', error.message)
    }
  }

  if (checkingSession) {
    return (
      <div className="auth-page">
        <p className="page-description">Loading your workspace...</p>
      </div>
    )
  }

  if (!userEmail) {
    return <Auth />
  }

  const initials = userEmail
    .split('@')[0]
    .slice(0, 2)
    .toUpperCase()

  return (
    <div className="app-layout">
      <Sidebar
        activePage={activePage}
        onNavigate={setActivePage}
        userEmail={userEmail}
        onLogout={handleLogout}
      />

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">
            <span>FinSight</span>
            <span className="breadcrumb-separator">/</span>
            <strong>
              {activePage === 'Research Reports' ? 'Research' : activePage}
            </strong>
          </div>

          <div className="topbar-actions">
            <button className="icon-button" aria-label="Search">
              <Search size={18} />
            </button>

            <button className="icon-button" aria-label="Notifications">
              <Bell size={18} />
            </button>

            <div className="topbar-avatar">{initials}</div>
          </div>
        </header>

        <section className="page-container">
          {activePage === 'Research Reports' ? (
            <ResearchReports
              onNewResearch={() => setActivePage('Company Analyst')}
              onViewHistory={() => setActivePage('Research History')}
              onCompanyComparison={() => setActivePage('Company Comparison')}
              onEarningsAnalysis={() => setActivePage('Earnings Analysis')}
              onDocumentResearch={() => setActivePage('Document Research')}
            />
          ) : activePage === 'Earnings Analysis' ? (
            <EarningsAnalysis />
            ) : activePage === 'Document Research' ? (
            <DocumentResearch />
          ) : activePage === 'Company Analyst' ? (
            <CompanyAnalyst />
          ) : activePage === 'Company Comparison' ? (
            <ComparisonAgent />
          ) : activePage === 'Research History' ? (
            <ResearchHistory
              onBack={() => setActivePage('Research Reports')}
            />
          ) : (
            <div className="page-heading">
              <div>
                <p className="eyebrow">FINSIGHT WORKSPACE</p>
                <h1>{activePage}</h1>
                <p className="page-description">
                  Explore financial intelligence with FinSight AI.
                </p>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
