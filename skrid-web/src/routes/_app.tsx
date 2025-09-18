import { createFileRoute, Outlet, Link } from '@tanstack/react-router'
import { useAuth } from '@/auth'
import { useTripCtx} from '@/trips'

import { IoHome, IoCreateOutline, IoPerson } from 'react-icons/io5'
import { MdOutlineAdminPanelSettings, MdPeople, MdLocationPin, MdOutlineHistory, MdOutlinePayment } from 'react-icons/md'

export const Route = createFileRoute('/_app')({
  component: RouteComponent,
})

function RouteComponent() {
  const auth = useAuth()
  const tripCtx = useTripCtx()
  return (
    <div className="grid grid-rows-12 grid-cols-6 items-center h-full w-full text-center relative divide-y divide-slate-800">
      <div className="row-span-11 col-span-6 flex flex-col justify-start items-center w-full h-full">
        <Outlet />
      </div>
      <div className="col-span-6 flex justify-evenly items-center h-full w-full">
        <Link to="/home" className="flex flex-col justify-center items-center w-20 h-20 py-2 gap-y-2">
            {({ isActive })=>{
              return (
                <div className={isActive ? "flex flex-col justify-evenly items-center w-full h-full text-blue-500": "flex flex-col justify-evenly items-center w-full h-full"}>
                  <IoHome size={28} />
                  <span className="flex justify-center items-center w-full font-bold text-sm">Home</span>
                </div>
              )
            }}
        </Link>
        {auth.isAuthenticated && auth.user.is_admin ?
          <Link to="/destinations" className="flex flex-col justify-center items-center w-20 h-20 py-2 gap-y-2">
            {({ isActive })=>{
              return (
                <div className={isActive ? "flex flex-col justify-evenly items-center w-full h-full text-blue-500": "flex flex-col justify-evenly items-center w-full h-full"}>
                  <MdLocationPin size={28} />
                  <span className="flex justify-center items-center w-full font-bold text-sm">Destinations</span>
                </div>
              )
            }}
          </Link>
        : null}
        {auth.isAuthenticated && auth.user?.is_admin ?
          <Link to="/admin" className="flex flex-col justify-center items-center w-20 h-20 py-2 gap-y-2">
            {({ isActive })=>{
              return (
                <div className={isActive ? "flex flex-col justify-evenly items-center w-full h-full text-blue-500": "flex flex-col justify-evenly items-center w-full h-full"}>
                  <MdOutlineAdminPanelSettings size={28} />
                  <span className="flex justify-center items-center w-full font-bold text-sm">Admin</span>
                </div>
              )
            }}
          </Link>
          : null}
        {/*auth.isAuthenticated ?
          <div onClick={(e)=> toggleHistoryModal(e)} className="flex flex-col justify-center items-center w-20 h-20 py-2 gap-y-2">
            <MdOutlineHistory size={28} />
            <span className="flex justify-center items-center w-full font-bold text-sm">History</span>
          </div>
        : null*/}
        {/*auth.isAuthenticated && auth.user?.is_admin ?
          <div className="flex flex-col justify-center items-center w-20 h-20 py-2 gap-y-2">
            <MdPeople size={28} />
            <span className="flex justify-center items-center w-full font-bold text-sm">Users</span>
          </div>
        : ""*/}
        {auth.isAuthenticated ?
          <Link to="/account" className="flex flex-col justify-center items-center w-20 h-20 py-2 gap-y-2">
            {({ isActive })=>{
              return (
                <div className={isActive ? "flex flex-col justify-evenly items-center w-full h-full text-blue-500": "flex flex-col justify-evenly items-center w-full h-full"}>
                  <IoPerson size={28} />
                  <span className="flex justify-center items-center w-full font-bold text-sm">Account</span>
                </div>
              )
            }}
          </Link>
        : null}
      </div>
    </div>
  )
}
