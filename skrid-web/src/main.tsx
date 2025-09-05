import { StrictMode } from 'react'
import ReactDOM from 'react-dom/client'
import { RouterProvider, createRouter } from '@tanstack/react-router'

// Import the generated route tree
import { routeTree } from './routeTree.gen'
import { AuthProvider, useAuth } from "@/auth"
import { EventProvider, useEvent } from '@/event'
import { TripProvider, useTripCtx } from '@/trips'

import './styles.css'
import reportWebVitals from './reportWebVitals.ts'


// Create a new router instance
const router = createRouter({
  routeTree,
  context: {
    auth: undefined!, // This will be set after we wrap the app in an AuthProvider
    event: undefined!,
    tripCtx: undefined!,
  },
  defaultPreload: 'intent',
  scrollRestoration: true,
  defaultStructuralSharing: true,
  defaultPreloadStaleTime: 0,
})

// Register the router instance for type safety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}

function InnerApp() {

  const auth = useAuth()
  const event = useEvent()
  const tripCtx = useTripCtx()

  return <RouterProvider router={router} context={{auth, event, tripCtx }} />
}

function App() {
  return (
    <AuthProvider>
      <EventProvider>
        <TripProvider>
          <InnerApp />
        </TripProvider>
      </EventProvider>
    </AuthProvider>
  )
}

// Render the app
const rootElement = document.getElementById('app')
if (rootElement && !rootElement.innerHTML) {
  const root = ReactDOM.createRoot(rootElement)
  root.render(
    <StrictMode>
      <App />
    </StrictMode>,
  )
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
