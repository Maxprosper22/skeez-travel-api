import { createFileRoute } from '@tanstack/react-router'

import { IoPerson } from 'react-icons/io5'
import { AuthBtn } from '@/components/AuthBtn'

import { useAuth } from '@/auth'
import { useTripCtx } from '@/trips'

export const Route = createFileRoute('/_app/account')({
  component: RouteComponent,
})

function RouteComponent() {
  const auth = useAuth()
  const tripCtx = useTripCtx()

  return (
    <div className="col-span-6 row-span-11 flex flex-col justify-start items-center w-full h-full p-4 gap-4 ">
      <div className="flex justify-start items-center w-full p-4 gap-4 bg-slate-800 rounded-2xl">
        <div className="flex justify-center items-center w-16 h-16 rounded-full overflow-hidden bg-slate-900">
          <IoPerson size={32} />
        </div>
        <div className="flex flex-wrap justify-start items-center min-h-4 w-[80%] gap-x-2">
        { auth.isAuthenticated ? <>
          <span className="font-bold text-lg">{auth.user?.lastname}</span>
          <span className="font-bold text-lg">{auth.user?.firstname}</span>
          {auth.user?.othername ? <span className="font-bold text-lg">{auth.user?.othername}</span> : ""}
        </> : <span className="font-bold text-lg">Lovely Guest</span>
        }
        </div>
      </div>  
      {/* Auth actions */}
      {!auth.isAuthenticated ? 
      <div className="flex flex-col justify-between items-center w-[80%] gap-4">
        <AuthBtn value="signin" />
        <AuthBtn value="signup" />
      </div>
      : 
      <AuthBtn value="signout" />
      }
    </div>
  )
}
