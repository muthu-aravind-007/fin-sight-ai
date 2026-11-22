import { useState, type FormEvent } from 'react'
import { ArrowRight, LockKeyhole, Mail } from 'lucide-react'
import { supabase } from '../services/supabase'

const Auth = () => {
  const [isSignUp, setIsSignUp] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    setLoading(true)
    setMessage('')
    setError('')

    try {
      if (isSignUp) {
        const { data, error } = await supabase.auth.signUp({
          email: email.trim(),
          password,
        })

        if (error) throw error

        if (data.session) {
          setMessage('Account created successfully.')
        } else {
          setMessage(
            'Account created. Check your email to confirm your address before signing in.',
          )
        }
      } else {
        const { error } = await supabase.auth.signInWithPassword({
          email: email.trim(),
          password,
        })

        if (error) throw error
      }
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Something went wrong. Please try again.',
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
        <div className="auth-brand">
          <div className="brand-icon">F</div>
          <span>FINSIGHT</span>
        </div>

        <div className="auth-heading">
          <p className="eyebrow">FINANCIAL INTELLIGENCE</p>
          <h1>{isSignUp ? 'Create your account' : 'Welcome back'}</h1>
          <p>
            {isSignUp
              ? 'Create an account to save and manage your research.'
              : 'Sign in to continue to your financial workspace.'}
          </p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label htmlFor="auth-email">Email address</label>

          <div className="auth-input-wrapper">
            <Mail size={17} />
            <input
              id="auth-email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              autoComplete="email"
              required
            />
          </div>

          <label htmlFor="auth-password">Password</label>

          <div className="auth-input-wrapper">
            <LockKeyhole size={17} />
            <input
              id="auth-password"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              autoComplete={isSignUp ? 'new-password' : 'current-password'}
              minLength={6}
              required
            />
          </div>

          {error && <p className="auth-error">{error}</p>}
          {message && <p className="auth-message">{message}</p>}

          <button
            className="auth-submit"
            type="submit"
            disabled={loading}
          >
            {loading
              ? 'Please wait...'
              : isSignUp
                ? 'Create account'
                : 'Sign in'}

            {!loading && <ArrowRight size={17} />}
          </button>
        </form>

        <div className="auth-switch">
          <span>
            {isSignUp
              ? 'Already have an account?'
              : "Don't have an account?"}
          </span>

          <button
            type="button"
            onClick={() => {
              setIsSignUp(!isSignUp)
              setMessage('')
              setError('')
            }}
          >
            {isSignUp ? 'Sign in' : 'Create account'}
          </button>
        </div>

        <p className="auth-footer">
          Your financial research workspace, in one place.
        </p>
      </section>
    </main>
  )
}

export default Auth
