import { useState, useRef } from 'react';
import type { MouseEvent } from 'react'

import { useAuth } from '@/auth';

import { TripCard } from '@/components/TripCard'

interface HistoryProps {
  showHistoryModal: boolean;
  toggleHistoryModal: (e: MouseEvent<HTMLDivElement>) => void;
}

export const MyTravelHistory = ({ showHistoryModal, toggleHistoryModal } : HistoryProps) => {

  if (!showHistoryModal) {
    return null
  }
  const auth = useAuth()

  const historyModal = useRef<HTMLDivElement>(null)

  const handleModal = (e: MouseEvent<HTMLDivElement>) => {
    if (e.target == historyModal.current) {
      toggleHistoryModal(e)
    }
  }
  console.log(historyModal)
  return (
    <div ref={historyModal} className="flex flex-col justify-end items-center w-screen h-dvh absolute z-10 bg-slate-900/80" onClick={(e)=> handleModal(e)}>
      <div className="flex flex-col justify-center items-center w-full max-h-[70%] h-[50%] bg-slate-800 py-4 px-4 gap-6 rounded-t-4xl">
      {
        auth.user?.trips ? auth.user?.trips.map((trip)=> <TripCard key={trip?.trip_id} trip={trip} />) 
      :
        <div className="flex flex-col justify-center items-center w-full h-full font-bold italic tex-gray-500">No Entry found</div>
      }
      </div>
    </div>
  )
}
