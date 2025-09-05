import { usetate, useEffect } from 'react'
import { Outlet, createRootRouteWithContext } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'

import type { AuthContext } from '@/auth'
import type { EventContext } from '@/event';
import type { TripContext } from '@/trips'

import { useAuth } from '@/auth'
import { useTripCtx } from '@/trips'

import { SignInForm } from '@/components/SignInForm'
// import { Signup } from '@/components/Signup'

interface RouterContext {
  auth: AuthContext;
  event: EventContext;
  tripCtx: TripContext;
}
export const Route = createRootRouteWithContext<RouterContext>()({
  component: Root,
})

function Root() {
  const auth = useAuth()
  const tripCtx = useTripCtx()

  useEffect(()=>{
    tripCtx.fetchTrips()
    tripCtx.fetchDestinations()
  }, [])
  return (
    <div className="flex flex-col justify-center items-center w-screen h-dvh relative text-white bg-slate-900">
      {!auth.isAuthenticated && auth.showSignInForm ? <SignInForm /> : ""}
      {/*context.auth.showSignUpForm ? <Signup /> : ""*/}
      <Outlet />
      <TanStackRouterDevtools />
    </div>
  )
}
