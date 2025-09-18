import { useState, useEffect, useRef } from 'react'
import { useNavigate } from '@tanstack/react-router'

import { useAuth } from '@/auth'
import type { AccountType } from '@/auth'
import { useTripCtx } from '@/trips'

export const ReservationCTA = ({ tripid, slots }: {tripid: string, slots?: Array<AccountType | null>}) => {
  const [isBooked, setIsBooked] = useState<boolean>(false)
  const auth = useAuth()
  const tripCtx = useTripCtx()

  const navigate = useNavigate()

  console.log(auth.user)

  const bookBtn = useRef<HTMLButtonElement>(null)
  const unBookBtn = useRef<HTMLButtonElement>(null)

  useEffect(()=>{
    slots?.forEach(element => {
      console.log(element)
      if (element?.account_id == auth.user?.account_id) {
        setIsBooked(true)
        // bookBtn.current.disabled = true
      }
    });
  }, [])

  const handleBooking = async () => {
    if (!auth.isAuthenticated) {
      // auth.toggleAuthForm('signin')
      navigate({
        to: '/signin'
      })
    } else {
      const req = await fetch(`http://127.0.0.1:8080/trip/${tripid}/book`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${auth.token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({'tripid': tripid, 'accountid': auth.user?.account_id})
      })
      console.log(req)
      const resp = await req.json()
      if (req.status != 201) {
        console.log(resp.info)
        alert(resp.info)
        return
      }
      // if (resp.data.access_code) {
      const trip = tripCtx.trips.get(tripid)
      const tripSlots = trip!.slots
      tripSlots?.push(auth.user)
      tripCtx.updateTrip(tripid, 'slots', tripSlots)
      setIsBooked(true)
      // }
    }
  }

  const cancelBooking = async () => {
    if (!auth.isAuthenticated) {
      return null
    } else {
      const req = await fetch(`http://127.0.0.1:8080/trip/${tripid}/unbook`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${auth.token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({'tripid': tripid, 'accountid': auth.user?.account_id})
      })
      console.log(req)
      const resp = await req.json()
      console.log(resp.status)
      if (req.status == 200) {
        console.log(slots)
        const newSlots = slots!
        newSlots?.forEach(element => {
          if (element?.account_id == auth.user?.account_id) {
            const indexValue = newSlots?.indexOf(element)
            newSlots.splice(indexValue,1)
          }
        });
        tripCtx.updateTrip(tripid, 'slots', newSlots)
        setIsBooked(false)
      } else {
        console.log(resp.info)
        alert(resp.info)
      }
    }
  }
  return (
    <>
    {isBooked ? <button ref={unBookBtn} onClick={(e)=> cancelBooking()} className="flex justify-center items-center w-[70%] h-10 bg-red-500 border border-red-500 active:bg-red-500/70 disabled:bg-slate-500/40 text-sm font-bold rounded-lg">Cancel Reservation</button>
    : <button ref={bookBtn} onClick={(e)=> handleBooking()} className="flex justify-center items-center w-[70%] h-10 bg-blue-500 active:bg-blue-500/70 disabled:bg-slate-500/40 text-sm font-bold rounded-lg">Reserve</button>}
    </>
  )
}
