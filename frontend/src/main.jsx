// React's StrictMode feature identifies potential problems in the application during development, no effect on production build
import { StrictMode } from 'react'
// createRoot creates the React root where app will be rendered in HTML document
import { createRoot } from 'react-dom/client'
// CSS file with global styles for  React app
import './index.css'
//  main App component with frontend
import App from './App.jsx'

// Finds HTML element with id="root" in index.html, creates a React root inside it, and renders the App component.
// StrictMode wraps App to enable additional development-time checks.
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
