import { Link } from '@tanstack/react-router'
import { IoCashOutline, IoPeopleOutline, IoCalendarOutline, IoFilterOutline } from "react-icons/io5";
// import { HiOutlineHashtag } from "react-icons/hi2";
//
import type { TripType } from '@/trips'

export interface TripProps {
  tripid: string;
  destination: string;
  date: Date;
  price: number;
  status: string;
  slots: [string];
  capacity: number;
}

export const TripCard = ({trip}: TripType) => {
  // console.log(trip.destination)
  // console.log(typeof(trip))
  // trip.date = new Date(trip.date)
  return (
    <Link to="/trips/$tripid" params={{tripid: `${trip.trip_id}`}} className="flex flex-col justify-evenly items-center w-full py-2 px-4 gap-2 active:bg-slate-900 bg-slate-800 text-sm font-bold">
      <div className="flex justify-between items-center w-full h-12">
        <div className="flex justify-start items-center">
          <span className="flex justify-center rounded-lg p-1 bg-slate-800">{trip.trip_id}</span>
        </div>
        <span className={trip.status == 'pending' ? "text-yellow-600 text-sm rounded-lg py-1 px-2 border border-yellow-600" : trip.status == 'active' ? "text-green-500 border border-green-500 text-sm rounded-lg py-1 px-2" : trip.status == 'complete' ? "text-blue-500 text-sm border border-blue-500 rounded-lg py-1 px-2" : "text-red-500 text-sm border border-red-500 rounded-lg py-1px-2"}>{trip.status}</span>
      </div>

      <span className="flex justify-start items-center w-full font-bold text-xl">{trip.destination.name}</span>

      <div className="flex justify-between items-center w-full h-12 gap-5">
        <span className="flex justify-start items-center gap-2 text-gray text-sm">
          <IoCalendarOutline size={24} />
          <span className="">{new Date(trip.date).toLocaleString()}</span>
        </span>
        <div className="flex justify-evenly items-center gap-2">
          <div className="flex justify-center items-center py-1 px-2 gap-2 text-gray text-sm bg-slate-800 rounded-full">
            <IoCashOutline size={24} />
            <span>{trip.destination.price}</span>
          </div>
          <div className="flex justify-center items-center py-1 px-2 gap-2 text-gray text-sm bg-slate-800 rounded-full">
            <IoPeopleOutline size={24} />
            <span>{trip.slots.length}/{trip.capacity}</span>
          </div>
        </div>
      </div>
    </Link>
  )
}
