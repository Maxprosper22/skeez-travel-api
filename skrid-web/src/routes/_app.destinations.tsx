import { createFileRoute } from '@tanstack/react-router'
import { useRef, useState, useEffect } from 'react';
import type { ChangeEvent, MouseEvent } from 'react'

import { useTripCtx } from '@/trips'
import type { DestinationType } from '@/trips'
import { useAuth } from '@/auth'

import { IoInformationCircleOutline } from 'react-icons/io5'
import { MdOutlineAddLocationAlt } from 'react-icons/md'

interface DestinationsProps {
  showDestinationModal: boolean;
  toggleDestinationModal: (e: MouseEvent<HTMLDivElement>) => void;
}
interface DestinationFormProps {
  showDestinationForm: boolean;
  toggleDestinationForm: () => void;
}

const DestinationForm = ({ showDestinationForm, toggleDestinationForm }: DestinationFormProps) => {
  if (!showDestinationForm) return null

  const tripCtx = useTripCtx()

  const formBackdrop = useRef<HTMLDivElement>(null)
  const nameRef = useRef<HTMLInputElement>(null)
  const priceRef = useRef<HTMLInputElement>(null)

  const [name, setDestinationName] = useState<string | null>(null)
  const [price, setPrice] = useState<number | null>(null)

  const [showDestinationError, setDestinationError] = useState<boolean>(false)
  const [showPriceError, setPriceError] = useState<boolean>(false)

  const handleDestInput = (e: ChangeEvent<HTMLInputElement>) => {
    setDestinationName(e.target?.value)
    if (showDestinationError) setDestinationError(false)
  }
  const handlePriceInput = async (e: ChangeEvent<HTMLInputElement>) => {
    setPrice(Number(e.target?.value))
    if (showPriceError) setPriceError(false)
  }
  const sendNewDestination = async () => {
    if (!name) {
      setDestinationError(!showDestinationError)
      return
    } else if (!price) {
      setPriceError(!showPriceError)
    } else {
      await tripCtx.createDestination({name, price})
    }
  }
  const handleFormDisplay = (e: MouseEvent<HTMLDivElement>) => {
    if (e.target == e.currentTarget) {
      toggleDestinationForm()
    }
  }
  return (
    <div ref={formBackdrop} className="flex flex-col justify-end items-center w-screen h-dvh absolute z-12 bg-slate-900/70" onClick={(e)=> handleFormDisplay(e)}>
      <div className="flex flex-col justify-center items-center w-full bg-slate-800 py-8 px-4 gap-4 rounded-t-4xl divide-y divide-gray-500 relative">
        <span className="flex justify-start items-center w-full font-bold text-xl">Add Destination</span>
        <div className="flex flex-col justify-center items-center w-full gap-4 py-4">
          <div className="flex flex-col justify-center items-center w-full gap-y-2">
            <span className="flex justify-start w-full font-bold text-sm">Destination</span>
            <input type="text" onChange={(e)=>handleDestInput(e)} className="flex justify-start items-center w-full h-10 px-4 rounded-lg active:outline bg-slate-900 text-sm" />
            {showDestinationError ? <div ref={nameRef} className="flex justify-start items-center w-full font-bold text-sm text-red-500 gap-x-1">
              <IoInformationCircleOutline size={24} />
              <span> Destination required!</span>
            </div> : ""}
          </div>

          <div className="flex flex-col justify-center items-center w-full gap-y-2">
            <span className="flex justify-start w-full font-bold text-sm">Price (NGN)</span>
            <input type="text" onChange={(e)=>handlePriceInput(e)} className="flex justify-start items-center w-full h-10 px-4 rounded-lg active:outline bg-slate-900 text-sm" />
            {showPriceError ?<div ref={priceRef} className="flex justify-start items-center w-full font-bold text-sm text-red-500 gap-x-1">
              <IoInformationCircleOutline size={20} />
              <span>Price required!</span>
            </div> : ""}
          </div>
          <div onClick={(e)=> sendNewDestination()} className="flex justify-center items-center w-full h-10 bg-blue-500 active:bg-blue-500/80 font-bold rounded-lg">Add</div>
        </div>
      </div>
    </div>
  )
}

const DestinationItem = ({destination}: {destination: DestinationType}) => {
  console.log(destination.destination_id)
  return (
    <div className="flex justify-center items-center w-full h-20 bg-slate-800">{destination.name}</div>
  )
}

export const Route = createFileRoute('/_app/destinations') ({
  component: Destinations
})

function Destinations() {
  
  const auth = useAuth()
  const tripCtx = useTripCtx()

  const [showDestinationForm, setDestinationForm] = useState<boolean>(false)

  const destinationsBackdrop = useRef<HTMLDivElement>(null)
  const historyList = useRef<HTMLDivElement>(null)


  const toggleDestinationForm = () => {
    setDestinationForm(!showDestinationForm)
  }

  return (
    <div ref={destinationsBackdrop} className="flex flex-col justify-start items-center w-full h-fullbg-slate-900/80">
      <div className="flex justify-between items-center w-full h-28">
        <span className="flex justify-start items-center font-bold text-lg">Destinations</span>
        <div onClick={(e)=> toggleDestinationForm()} className="flex justify-center items-center w-32 h-10 gap-x-1 bg-blue-500 rounded-lg">
          <MdOutlineAddLocationAlt size={24} />
          <span className="font-bold text-sm">Add</span>
        </div>
      </div>
      <div className="flex flex-col justify-center items-center w-full py-8 px-4 gap-6 relative">

        <div ref={historyList} className="flex flex-col justify-center items-center w-full max-h-140 min-h-36 bg-slate-900 rounded-lg overflow-hidden">
          {tripCtx.destinations ? <div className="flex flex-col justify-start items-center w-full h-full divide-y divide-slate-900 overflow-y-auto">
            {Array.from(tripCtx.destinations, ([key, value])=><DestinationItem key={key} destination={value} />)}
          </div> : <div className="flex justify-center items-center w-full h-full font-bold italic">No destination data</div>}
        </div>
      </div>
      <DestinationForm showDestinationForm={showDestinationForm} toggleDestinationForm={toggleDestinationForm} />
    </div>
  )
}
