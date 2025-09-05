import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/auth';
import { useTripCtx, StatusEnum } from '@/trips';
import type { DestinationType, newTripType } from '@/trips'

import { TripCard } from '@/components/TripCard'

import { IoInformationCircleOutline } from 'react-icons/io5'

interface CreateTripProps {
  showCreateTripModal: boolean;
  toggleCreateTripModal: () => void;
}

export const CreateTripModal = ({ showCreateTripModal, toggleCreateTripModal } : CreateTripProps) => {

  if (!showCreateTripModal) {
    return null
  }
  const auth = useAuth()
  const tripCtx = useTripCtx()

  const createTripModal = useRef('create-trip-modal')

  const handleModal = (e) => {
    if (e.target != createTripModal.current) {
      return
    } else {
      toggleCreateTripModal()
    }
  }

  const [destinationValue, setDestinationValue] = useState<DestinationType | null>(null)
  const [dateValue, setDateValue] = useState<Date | null>(null)
  const [statusValue, setStatusValue] = useState<StatusEnum | null>(null)
  const [capacityValue, setCapacityValue] = useState<number | null>(null)
  const [priceValue, setPriceValue] = useState<number | null>(null)

  const [showDestinationError, setDestinationError] = useState<boolean>(false)
  const [showDateError, setDateError] = useState<boolean>(false)
  const [showStatusError, setStatusError] = useState<boolean>(false)
  const [showCapacityError, setCapacityError] = useState<boolean>(false)
  const [showPriceError, setPriceError] = useState<boolean>(false)

  const destinationRef = useRef('destination-ref')
  const priceRef = useRef('price-ref')
  const statusRef = useRef('status-ref')

  useEffect(()=>{
    const defaultDestination = tripCtx.destinations.get(destinationRef.current.value)
    if (defaultDestination) {
      console.log(defaultDestination)
      setDestinationValue(defaultDestination)
      priceRef.current.value = defaultDestination.price
      setPriceValue(priceRef.current.value)
    }
    const defaultStatus = statusRef
    if (defaultStatus) {
      // console.log('Default status: ')
      // console.log(defaultStatus)
      setStatusValue(defaultStatus.current.value)
    }
  }, [])

  const handleDestinationField =(e)=> {
    const destValue = tripCtx.destinations.get(e.target.value)
    if (destValue) {
      setDestinationValue(destValue)
      priceRef.current.value = destValue.price
    }
    if (showDestinationError) {
      setDestinationError(!showDestinationError)
    }
  }
  const handleDateField = (e)=> {
    setDateValue(e.target.value)
    if (showDateError) {
      setDateError(!showDateError)
    }
  }
  const handleStatusField = (e) => {
    setStatusValue(e.target.value)
    if (showStatusError) {
      setStatusError(!showStatusError)
    }
  }
  const handleCapacityField = (e) => {
    setCapacityValue(e.target.value)
    if (showCapacityError) {
      setCapacityError(!showCapacityError)
    }
  }
  const handlePriceField = (e) => {
    setPriceValue(e.target.value)
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
        await tripCtx.createTrip({destination:destinationValue, capacity:capacityValue, status:statusValue, date:dateValue})
      }
    } catch (error) {
      console.log(error)
      alert('An error occurred during trip creation')
    }
  }
  return (
    <div ref={createTripModal} className="flex flex-col justify-end items-center w-screen h-dvh absolute z-10 bg-slate-900/80" onClick={(e)=> handleModal(e)}>
      <div className="flex flex-col justify-center items-center w-full bg-slate-800 py-6 px-4 gap-6 rounded-t-4xl divide-y divide-gray-500">
        <div className="flex justify-start items-center w-full">
          <span className="text-lg font-bold">New Trip</span>
        </div>

        <div className="grid grid-cols-2 flex flex-col w-full gap-6">
          <div className="col-span-2 flex flex-col items-center w-full gap-y-2">
            <span className="flex justify-start items-center text-lg font-bold w-full text-sm">Destination</span>
            <select ref={destinationRef} onChange={(e)=>handleDestinationField(e)} className="actve:outline w-full h-10 rounded-lg bg-slate-900 px-2 text-sm">
              {tripCtx.destinations ? Array.from(tripCtx.destinations, ([key, value])=><option key={key} value={value.destination_id} className="">{value.name}</option>) : <option></option>}
            </select>
            {showDestinationError ? <div className="flex justify-start items-center w-full font-bold text-sm text-red-500 gap-x-1">
              <IoInformationCircleOutline size={24} />
              <span> Destination required!</span>
            </div> : ""}
          </div>
          <div className="flex flex-col justify-center items-center w-full gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Date</span>
            <input type="datetime-local" onChange={(e)=> handleDateField(e)} className="flex justify-start items-center w-full h-10 px-2 rounded-lg bg-slate-900 text-sm active:outline placeholder:text-gray-500" placeholder="DD/MM/YY" />
            {showDateError ? <div className="flex justify-start items-center w-full font-bold text-sm text-red-500 gap-x-1">
              <IoInformationCircleOutline size={24} />
              <span> Date required!</span>
            </div> : ""}
          </div>
          <div className="flex flex-col justify-center items-center w-full gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Status</span>
            <select ref={statusRef} onChange={(e)=> handleStatusField(e)} className="w-full h-10 rounded-lg bg-slate-900 px-2 active:outline text-sm">
              <option value={StatusEnum.Pending}>Pending</option>
              <option value={StatusEnum.Active}>Active</option>
            </select>
            {showStatusError ? <div className="flex justify-start items-center w-full font-bold text-sm text-red-500 gap-x-1">
              <IoInformationCircleOutline size={24} />
              <span>Status required!</span>
            </div> : ""}
          </div>
          <div className="flex flex-col justify-center items-center w-full gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Capacity</span>
            <input type="number" onChange={(e)=> handleCapacityField(e)} className="flex justify-start items-center w-full h-10 px-2 bg-slate-900 rounded-lg active:outline placeholder:text-gray-500 text-sm" placeholder="10" />
            {showCapacityError ? <div className="flex justify-start items-center w-full font-bold text-sm text-red-500 gap-x-1">
              <IoInformationCircleOutline size={24} />
              <span>Capacity required!</span>
            </div> : ""}
          </div>
          <div className="flex flex-col justify-center items-center w-full gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Price (NGN)</span>
            <input type="number" ref={priceRef} disabled onChange={(e)=> handlePriceField(e)} className="flex justify-start items-center w-full h-10 px-2 rounded-lg bg-slate-900 active:outline placeholder:text-gray-500 text-sm" placeholder="5000" />
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
