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
    <div className="grid grid-cols-5 grid-rows-24 w-full h-full divide-y divide-slate-800 overflow-y-auto">
      
      <div className="row-span-2 col-span-5 flex justify-center items-center w-full h-full bg-slate-950">
        <Header />
      </div>

      <div className="row-span-20 col-span-5 flex flex-col justify-start items-center w-full h-full p-2 gap-6 overflow-y-auto">
        <div className="flex flex-col justify-start items-center w-full p-4 gap-2">
        {/* <h1 className="flex justify-start items-center w-full font-bold text-2xl">Travel Port</h1>*/}

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
      <div className="row-span-2 col-span-5 flex justify-between items-center w-full h-full">
        <div className="flex justify-start items-center min-w-[40%] gap-2 text-sm">
          <h4 className="font-bold text">Available trips:</h4>
          <span className="text-gray">{tripCtx.trips?.size}</span>
        </div>
      </div>
      {/*<MyTravelHistory showHistoryModal={showHistoryModal} toggleHistoryModal={toggleHistoryModal} />*/}
    </div>
  )
}
