import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { RouterProvider } from 'react-router/dom'
import { router } from './app/router'
import './shared/styles.css'

// Retire the previous SPA's host-only token cookie when users load the new app.
document.cookie = 'auth_token=; Max-Age=0; Path=/; SameSite=Lax'

createRoot(document.getElementById('root')!).render(
  <StrictMode><RouterProvider router={router} /></StrictMode>,
)
