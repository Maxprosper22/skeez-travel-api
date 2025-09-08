import { createFileRoute } from '@tanstack/react-router'
import { useEffect, useRef, useState } from 'react'

import { useTripCtx } from '@/trips'
import { useAuth } from '@/auth';
import type { SlotType } from '@/auth'

import { ReservationCTA } from '@/components/Reservations'
import { IoMenu, IoPerson, IoChevronBack, IoCashOutline, IoPeopleOutline, IoCalendarOutline, IoFilterOutline } from 'react-icons/io5'

const fetchTrip = async (tripid: string) => {
  try {
    const req = await fetch(`http://127.0.0.1:8080/trip/${tripid}`)
    const resp = await req.json()
    if (resp.data) {
      return resp.data
    } else {
    alert(resp.info)
    }
  } catch (error) {
    console.error(error)
  }
}

export const Route = createFileRoute('/trips/$tripid')({
  loader: ({ params, context }) => fetchTrip(params.tripid),
  component: RouteComponent,
})

function RouteComponent() {
  const auth = useAuth()
  const tripCtx = useTripCtx()

  const [slotState, setSlotState] = useState<Array<SlotType> | []>([])

  const { tripid } = Route.useParams()

  // const data = Route.useLoaderData()
  let data = tripCtx.trips.get(tripid) 
  data!.date = new Date(data!.date)

  useEffect(()=>{
    data = tripCtx.trips.get(tripid)
  }, [data])
  
  return (
    <div className="grid grid-rows-12 grid-cols-5 justify-start items-center w-full h-dvh divide-y divide-slate-800 relative">
      <div className="row-span-1 col-span-5 flex justify-between items-center w-full h-full border">
        <div className="flex justify-start items-center h-full p-2 gap-2">
          <IoChevronBack size={24} />
          <span className="flex justify-center items-center h-full text-sm font-bold">Back</span>
        </div>
      </div>
      <div className="row-span-10 col-span-5 flex flex-col justify-start items-center w-full h-full p-4 gap-8">
        <div className="flex justify-start items-center w-full">
          <span className="px-4 py-2 font-bold text-sm rounded-full bg-slate-800"># {tripid}</span>
        </div>
        <div className="flex flex-col justify-start items-center w-full divide-y divide-slate-800">
          <span className="flex justify-start items-center w-full h-20 p-2 font-bold text-4xl">{data!.destination.name}</span>
          <div className="flex justify-start items-center w-full h-16 gap-4">
            <div className="flex justify-center items-center py-2 px-4 gap-2 text-gray text-sm font-bold bg-slate-800 rounded-full">
              <IoCalendarOutline size={24} />
              <span>{data!.date.toLocaleString("en-GB")}</span>
            </div>
          </div>
          <div className="flex justify-start items-center w-full h-16 gap-4">
            <div className="flex justify-center items-center py-2 px-4 gap-2 text-gray text-sm font-bold bg-slate-800 rounded-full">
              <IoCashOutline size={24} />
              <span>{data!.destination.price}</span>
            </div>
            <div className="flex justify-center items-center py-2 px-4 gap-2 text-gray text-sm font-bold bg-slate-800 rounded-full">
              <IoPeopleOutline size={24} />
              <span>{data!.slots?.length}/{data!.capacity}</span>
            </div>
          </div>
        </div>
        
        <div className="flex flex-col justify-start items-center w-full p-4 gap-4 bg-slate-800 rounded-lg">
          <div className="flex flex-col justify-start items-center w-full">
            {/* <span className="flex justify-start items-center w-full text-sm font-bold">Capacity - {data.capacity}</span>*/}
            <span className="flex justify-start items-center w-full text-lg font-bold">Reservations</span>
          </div>

          <div className="flrx flex-col justify-center items-center w-full rounded-lg bg-slate-900 divide-y divide-slate-800">
          {data!.slots? data!.slots?.map((slot)=>
            <div key={slot?.account_id} className="flex justify-center items-center w-full h-14 px-4">
              <div className="flex justify-center items-center w-full gap-x-4">
                <div className="flex justify-center items-center p-2 rounded-full bg-slate-800">
                  <IoPerson size={24} />
                </div>
                <span className="flex justify-start items-center w-full text-lg font-bold">{slot?.firstname} {slot?.lastname}</span>
              </div>
              <div className="flex ">
                <IoMenu size={24} />
              </div>
            </div>
          )
          : <div className="flex flex-col justify-center items-center w-full h-16 p-8">
              <span className=" font-bold italic text-center text-slate-500">There are no reservations yet. This is your chance to be the trail blazer</span>
            </div>}
          </div>
        </div>
      </div>
      <div className="row-span-1 col-span-5 flex justify-center items-center h-full w-full">
        <ReservationCTA tripid={tripid} slots={data!.slots} />
      </div>
    </div>
  )
}
