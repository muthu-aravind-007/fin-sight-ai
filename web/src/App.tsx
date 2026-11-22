import { useState } from 'react'
import { Bell, Plus, Search } from 'lucide-react'
import Sidebar from './components/Sidebar'
import './App.css'

import CompanyAnalyst from './pages/companyAnalyst'

function App() {
  const [activePage, setActivePage] = useState('Research Reports')

  return (
    <div className="app-layout">
      <Sidebar
        activePage={activePage}
        onNavigate={setActivePage}
      />

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">
            <span>FinSight</span>
            <span className="breadcrumb-separator">/</span>
            <strong>{activePage}</strong>
          </div>

          <div className="topbar-actions">
            <button className="icon-button" aria-label="Search">
              <Search size={18} />
            </button>
            <button className="icon-button" aria-label="Notifications">
              <Bell size={18} />
            </button>
            <div className="topbar-avatar">MA</div>
          </div>
        </header>

        <section className="page-container">
          {activePage === 'Company Analyst' ? (
            <CompanyAnalyst />
          ) : activePage === 'Research Reports' ? (
            <>
              <div className="page-heading">
                <div>
                  <p className="eyebrow">FINANCIAL INTELLIGENCE</p>
                  <h1>Research Reports</h1>
                  <p className="page-description">
                    AI-powered financial research and company insights.
                  </p>
                </div>

                <button
                  className="primary-button"
                  onClick={() => setActivePage('Company Analyst')}
                >
                  <Plus size={17} />
                  Generate New Research
                </button>
              </div>

              <div className="empty-state">
                <div className="empty-state-icon">
                  <Search size={24} />
                </div>
                <h2>Your research starts here</h2>
                <p>Generate your first AI-powered company research report.</p>
              </div>
            </>
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
