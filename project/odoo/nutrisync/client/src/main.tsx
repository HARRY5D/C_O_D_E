import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { ErrorBoundary } from './components/ErrorBoundary.tsx'
import { FlutterApp } from 'flutter'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ErrorBoundary>
      <FlutterApp>
        <App />
      </FlutterApp>
    </ErrorBoundary>
  </StrictMode>,
)
