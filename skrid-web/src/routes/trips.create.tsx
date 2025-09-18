import { createFileRoute, useNavigate, useRouter, useCanGoBack } from '@tanstack/react-router'

import { useState, useRef, useEffect } from 'react'
import type { ChangeEvent, MouseEvent } from 'react';
import { useAuth } from '@/auth';
import { useTripCtx, StatusEnum } from '@/trips';
import type { DestinationType, newTripType } from '@/trips'

import { TripCard } from '@/components/TripCard'

import { IoInformationCircleOutline, IoChevronBack } from 'react-icons/io5'

interface CreateTripProps {
  showCreateTripModal: boolean;
  toggleCreateTripModal: (e: MouseEvent<HTMLDivElement>) => void;
}

export const Route = createFileRoute('/trips/create')({
  component: CreateTrip,
})
function CreateTrip () {

  const auth = useAuth()
  const tripCtx = useTripCtx()
  const navigate = useNavigate()

  if (!auth.isAuthenticated) {
    navigate({
      to: '/'
    })
  }
  const createTripModal = useRef<HTMLDivElement>(null)

  // const handleModal = (e: MouseEvent<HTMLDivElement>) => {
  // if (e.target == createTripModal.current) {
  //     toggleCreateTripModal(e)
  //   }
  // }

  const router = useRouter()
  const canGoBack = useCanGoBack()

  const [destinationValue, setDestinationValue] = useState<DestinationType | null>(null)
  const [dateValue, setDateValue] = useState<Date | null>(null)
  const [statusValue, setStatusValue] = useState<keyof typeof StatusEnum>("PENDING")
  const [capacityValue, setCapacityValue] = useState<number | null>(null)
  const [priceValue, setPriceValue] = useState<number | null>(null)

  const [showDestinationError, setDestinationError] = useState<boolean>(false)
  const [showDateError, setDateError] = useState<boolean>(false)
  const [showStatusError, setStatusError] = useState<boolean>(false)
  const [showCapacityError, setCapacityError] = useState<boolean>(false)
  const [showPriceError, setPriceError] = useState<boolean>(false)

  const destinationRef = useRef<HTMLSelectElement>(null)
  const priceRef = useRef<HTMLInputElement>(null)
  const statusRef = useRef<HTMLSelectElement>(null)

  useEffect(()=>{
    // console.log(destinationRef)
    const defaultDestination = tripCtx.destinations.get(destinationRef.current.value)
    console.log(defaultDestination)
    if (defaultDestination) {
      console.log(defaultDestination)
      setDestinationValue(defaultDestination)
      // destinationRef.current.value()
      priceRef.current.value = defaultDestination.price
      console.log(priceRef.value)
      setPriceValue(priceRef.current.value)
    }
    // const defaultStatus = statusRef
    // if (defaultStatus) {
    //   // console.log('Default status: ')
    //   // console.log(defaultStatus)
    //   setStatusValue(defaultStatus.current.value)
    // }
  }, [tripCtx.destinations])

  const handleDestinationField =(e: ChangeEvent<HTMLSelectElement>)=> {
    console.log(e)
    const destValue = tripCtx.destinations.get(e.target?.value)
    console.log(destValue)
    if (destValue) {
      setDestinationValue(destValue.name)
      priceRef.current.value = destValue.price
      setPriceValue(destValue.price)
    }
    if (showDestinationError) {
      setDestinationError(!showDestinationError)
    }
  }
  const handleDateField = (e: ChangeEvent<HTMLInputElement>)=> {
    setDateValue(new Date(e.target.value))
    if (showDateError) {
      setDateError(!showDateError)
    }
  }
  const handleStatusField = (e: ChangeEvent<HTMLSelectElement>) => {
    setStatusValue(e.target.value as keyof typeof StatusEnum)
    if (showStatusError) {
      setStatusError(!showStatusError)
    }
  }
  const handleCapacityField = (e: ChangeEvent<HTMLInputElement>) => {
    setCapacityValue(Number(e.target.value))
    if (showCapacityError) {
      setCapacityError(!showCapacityError)
    }
  }
  const handlePriceField = (e: ChangeEvent<HTMLInputElement>) => {
    setPriceValue(Number(e.target.value))
    if (showPriceError) {
      setPriceError(!showPriceError)
    }
  }

  const handleSubmit = async () => {
    try {
      if (!destinationValue) {
        setDestinationError(!showDestinationError)
      } else if (!dateValue) {
        setDateError(!showDateError)
      } else if (!statusValue) {
        setStatusError(!showStatusError)
      } else if (!capacityValue) {
        setCapacityError(!showCapacityError)
      } else if (!priceValue) {
        setPriceError(!showPriceError)
      } else {
        console.log(destinationValue)
        await tripCtx.createTrip({destination:destinationValue, capacity:capacityValue, status:StatusEnum[statusValue], date:dateValue})
      }
    } catch (error) {
      console.log(error)
      alert('An error occurred during trip creation')
    }
  }
  return (
    <div ref={createTripModal} className="flex flex-col justify-start items-center w-screen h-screen bg-slate-900/80 divide-y divide-gray-500">
      <div className="row-span-1 col-span-5 flex justify-between items-center w-full h-16">
        {canGoBack ? <div onClick={()=> router.history.back()} className="flex justify-start items-center h-full p-2 gap-2">
          <IoChevronBack size={24} />
          <span className="flex justify-center items-center h-full text-sm font-bold">New Trip</span>
        </div> : null}
      </div>
      <div className="flex flex-col justify-center items-center w-[90%] py-6 px-4 gap-6 rounded-t-4xl divide-y divide-gray-500">
      {/*<div className="flex justify-start items-center w-full">
          <span className="text-lg font-bold">New Trip</span>
        </div>*/}

        <div className="grid grid-cols-2 flex flex-col w-full gap-6">
          <div className="col-span-2 flex flex-col items-center w-full gap-y-2">
            <span className="flex justify-start items-center text-lg font-bold w-full text-sm">Destination</span>
            <select ref={destinationRef} onChange={(e)=>handleDestinationField(e)} className="actve:outline w-full h-10 outline-2 outline-slate-800 focus:border-blue-500 focus:outline-blue-500 rounded-lg bg-slate-900 px-2 text-sm">
              {tripCtx.destinations ? Array.from(tripCtx.destinations, ([key, value])=><option key={key} value={value.destination_id} className="">{value.name}</option>) : <option></option>}
            </select>
            {showDestinationError ? <div className="flex justify-start items-center w-full font-bold text-sm text-red-500 gap-x-1">
              <IoInformationCircleOutline size={24} />
              <span> Destination required!</span>
            </div> : ""}
          </div>
          <div className="flex flex-col justify-center items-center w-full gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Date</span>
            <input type="datetime-local" onChange={(e)=> handleDateField(e)} className="flex justify-start items-center w-full h-10 px-2 outline-2 outline-slate-800 focus:border-blue-500 focus:outline-blue-500 rounded-lg bg-slate-900 text-sm active:outline placeholder:text-gray-500" placeholder="DD/MM/YY" />
            {showDateError ? <div className="flex justify-start items-center w-full font-bold text-sm text-red-500 gap-x-1">
              <IoInformationCircleOutline size={24} />
              <span> Date required!</span>
            </div> : ""}
          </div>
          <div className="flex flex-col justify-center items-center w-full gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Status</span>
            <select ref={statusRef} onChange={(e)=> handleStatusField(e)} className="w-full h-10 outline-2 outline-slate-800 focus:border-blue-500 focus:outline-blue-500 rounded-lg bg-slate-900 px-2 active:outline text-sm">
              <option value={StatusEnum.PENDING}>Pending</option>
              <option value={StatusEnum.ACTIVE}>Active</option>
            </select>
            {showStatusError ? <div className="flex justify-start items-center w-full font-bold text-sm text-red-500 gap-x-1">
              <IoInformationCircleOutline size={24} />
              <span>Status required!</span>
            </div> : ""}
          </div>
          <div className="flex flex-col justify-center items-center w-full gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Capacity</span>
            <input type="number" onChange={(e)=> handleCapacityField(e)} className="flex justify-start items-center w-full h-10 px-2 outline-2 outline-slate-800 focus:border-blue-500 focus:outline-blue-500 bg-slate-900 rounded-lg active:outline placeholder:text-gray-500 text-sm" placeholder="10" />
            {showCapacityError ? <div className="flex justify-start items-center w-full font-bold text-sm text-red-500 gap-x-1">
              <IoInformationCircleOutline size={24} />
              <span>Capacity required!</span>
            </div> : ""}
          </div>
          <div className="flex flex-col justify-center items-center w-full gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Price (NGN)</span>
            <input type="number" ref={priceRef} disabled onChange={(e)=> handlePriceField(e)} className="flex justify-start items-center w-full h-10 px-2 outline-2 outline-slate-800 focus:border-blue-500 focus:outline-blue-500 rounded-lg bg-slate-900 active:outline placeholder:text-gray-500 text-sm" placeholder="5000" />
            {showPriceError ? <div className="flex justify-start items-center w-full font-bold text-sm text-red-500 gap-x-1">
              <IoInformationCircleOutline size={24} />
              <span>Price required!</span>
            </div> : ""}
          </div>
          <div onClick={(e)=>handleSubmit()} className="col-span-2 flex justify-center items-center w-full h-10 rounded-lg font-bold text-sm bg-blue-500">Create</div>
        </div>
      </div>
    </div>
  )
}
