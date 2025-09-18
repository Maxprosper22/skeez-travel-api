import { useState } from 'react'
import type { ChangeEvent, MouseEvent } from 'react'
import { createFileRoute, Link } from '@tanstack/react-router'

import { useAuth } from '@/auth'
import { useTripCtx } from '@/trips'

import Header from '@/components/Header'
import { MyTravelHistory } from '@/components/History'
// import { Destinations } from '@/components/Destinations'
import { TripCard } from '@/components/TripCard'

import { IoCashOutline, IoPerson, IoPeopleOutline, IoCalendarOutline, IoFilterOutline, IoFilter, IoCreateOutline, IoMenu, IoHome } from "react-icons/io5";
import { HiOutlineHashtag, HiClock, HiOutlineClock } from "react-icons/hi2";
import { MdOutlineHistory, MdOutlineAddLocationAlt, MdLocationPin, MdPeople, MdOutlinePayment } from 'react-icons/md'

export const Route = createFileRoute('/_app/home')({
  component: App,
})

function App() {
  const auth = useAuth()
  const tripCtx = useTripCtx()

  const [showHistoryModal, setHistoryModal] = useState<boolean>(false)
  const [showCreateTripModal, setCreateTripModal] = useState<boolean>(false)
  const [showDestinationModal, setDestinationModal] = useState<boolean>(false)
  
  const toggleHistoryModal = (e: MouseEvent<HTMLDivElement>) => {
    setHistoryModal(!showHistoryModal)
  }

  const toggleCreateTripModal = (e: MouseEvent<HTMLDivElement>) => {
    setCreateTripModal(!showCreateTripModal)
  }

  const toggleDestinationModal = (e: MouseEvent<HTMLDivElement>) => {
    setDestinationModal(!showDestinationModal)
  }

  // console.log(auth)
  // console.log(tripCtx)

  return (
    <div className="flex flex-col justify-start items-center w-full h-full divide-y divide-slate-800">
      <div className="flex justify-between items-center w-full h-[4em] gap p-2">
        <div className="flex justify-start items-center h-full px-2 font-bold">
          <Link to="/" className="flex justify-start items-center w-full font-bold text-2xl">Home</Link>
        </div>
            <div className="flex justify-center items-center w-full">
              {auth.isAuthenticated ? 
              <div className="flex flex-row justify-end items-center w-full rounded-2xl">
                <div onClick={(e)=> toggleHistoryModal(e)} className="flex flex-col justify-center items-center w-15 h-15">
                  <MdOutlineHistory size={28} />
                  {/*<span className="flex justify-center items-center w-full font-bold text-sm">History</span>*/}
                </div>
                {auth.user?.is_admin ?
                <div onClick={(e)=>toggleCreateTripModal(e)} className="flex flex-col justify-center items-center w-15 h-15">
                  <IoCreateOutline size={28} />
                  {/*<span className="flex justify-center items-center w-full font-bold text-sm">New Trip</span>*/}
                </div>
                : ""}
              </div> 
              : ""}
              {/*<div className="flex justify-center items-center w-24 h-10 rounded-lg bg-blue-500">
                <IoFilterOutline size={28} />
              </div>*/}
            </div>

        {/*<div className="flex flex-col justify-center items-center w-20 h-20 py-2 gap-y-2">
          <IoMenu size={28} />
          <span className="flex justify-center items-center w-full font-bold text-sm">Menu</span>
        </div>*/}
      </div>
      <div className="flex flex-col justify-start items-center w-full h-full p-2 gap-6 overflow-y-auto">
        <div className="flex flex-col justify-start items-center w-full p-4 gap-2">
        {/* <h1 className="flex justify-start items-center w-full font-bold text-2xl">Travel Port</h1>*/}
          <div className="flex justify-between items-center w-full h-12">
            <div className="flex justify-start items-center min-w-[40%] gap-2">
              <h4 className="font-bold text-xl">Available trips:</h4>
              <span className="text-gray">{tripCtx.trips?.size}</span>
            </div>

          </div>

          {/*<div className="flex justify-evenly items-center w-full">
            <input name="trip-search" placeholder="Search" className="flex justify-start items-center w-full h-14 px-4 text-gray-500 italic bg-slate-900 rounded-lg" />
          </div>*/}

          <div className="flex flex-col justify-start items-center w-full divide-y divide-slate-900 rounded-lg overflow-hidden">
            {tripCtx.trips.size != 0 ? 
              Array.from(tripCtx.trips, ([key, value])=>
                <TripCard key={key} trip={value} />
              )
            :
              <div className="flex flex-col justify-center items-center w-full px-2 py-4 gap-8 bg-slate-900 rounded-lg">
                <span className="flex justify-center items-center w-full h-10 font-bold italic text-gray-500">No trip available</span>
                <div className="flex justify-center items-center w-[50%] h-10 bg-blue-500 active:bg-blue-500/50 rounded-lg" onClick={(e)=> tripCtx.fetchTrips()}>Refresh</div>
              </div>
            }
          </div>

        </div>
      </div>
      <MyTravelHistory showHistoryModal={showHistoryModal} toggleHistoryModal={toggleHistoryModal} />
    </div>
  )
}
