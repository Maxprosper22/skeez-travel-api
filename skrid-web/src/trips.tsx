import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';

import { useAuth } from '@/auth'

export enum StatusEnum {
  Pending = "pending",
  Active = "active",
  Cancelled = "cancelled",
  Complete = "complete"
}

export interface TripContext {
  trips: Map<string, TripType>;
  destinations: Map<string, DestinationType>;
  createTrip: () => void;
  fetchTrips: () => void;
  updateTrip: <K extends keyof TripType>(key: string, property: K, value: TripType[K]) => void;
  createDestination: () => void;
  fetchDestinations: () => void;
}

export interface DestinationType {
  destination_id: string;
  name: string;
  price: number;
}
export type newDestinationType = Omit<DestinationType, "destination_id"> & {destination_id?: string}

export interface TripSlot {
  accountid: string;
  size: number;
}

export interface TripType {
  trip_id: string;
  destination: DestinationType;
  capacity: number;
  slots: Array<TripSlot> | null;
  status: StatusEnum;
  date: Date;
}

export type newTripType = Omit<TripType, "slots"> & {trip_id?: string, slots?: Array<TripSlot> | null}

const TripContext = createContext<TripContext | undefined>(undefined)

export const TripProvider = ({children}: {children: ReactNode}) => {
  const [trips, setTrips] = useState<Map<string, TripType>>(new Map())
  const [destinations, setDestinations] = useState<Map<string, DestinationType>>(new Map())

  const auth = useAuth
  
  const createTrip = async (trip: newTripType) => {
    console.log(trip)
    const req = await fetch('http://127.0.0.1:8080/admin/trip/create', {
      method: "POST",
      Authorization: `Bearer ${auth.token}`,
      body: JSON.stringify(trip)
    })
    const resp = await req.json()
    console.log(resp)
    if (resp.data) {
      setTrips((prevData)=>{
        const newMap = new Map(prevData)
        newMap.set(resp.data.destination_id, resp.data)
        return newMap
      })
    }
  }
  const fetchTrips = async () => {
    const req = await fetch('http://127.0.0.1:8080/api/trips')
    const resp: {info: string | null, data?: Array<TripType>} = await req.json()
    if (resp.data) {
      const data: Array<TripType> = resp.data
      setTrips((oldData)=>{
        const newTripMap = new Map(oldData)
        for (let i=0; i<data.length; i++) {
          newTripMap.set(data[i].trip_id, data[i])
        }
        return newTripMap
      })
    }
  }
  const fetchTrip = async (tripid: string) => {
    try {
      const req = await fetch(`http://127.0.0.1:8080/trip/${tripid}`)
      const resp = await req.json()
      if (resp.data) {
        return resp.data
      }
    } catch (error) {
      console.error(error)
    }
  }

  const updateTrip = <K extends keyof TripType> (key: string, property: K, value: TripType[K]) => {   
    // oldData = trips
    console.log("Key " + key)
    console.log("Property " + property)
    console.log("Value " + value)

    setTrips((prevTripsMap) => {
      console.log(prevTripsMap)
      const newUpdate = new Map(prevTripsMap)
      const tripData = newUpdate.get(key)
      if (tripData) {
        newUpdate.set(key, {...tripData, [property]: value})
      }
      return newUpdate
    })
  }
  
  const createDestination = async (newDest: newDestinationType) => {
    try {
      const req = await fetch('http://127.0.0.1:8080/admin/destinations/new', {
        method: "POST",
        Authorization: `Bearer ${auth.token}`,
        body: JSON.stringify(newDest)
      
      })
      const resp = await req.json()
      console.log(resp)
    } catch (error) {
      alert('An error occurred!')
      console.log(error)
    }
  }

  const fetchDestinations = async () => {
    const req = await  fetch('http://127.0.0.1:8080/destinations')
    const resp: {info: string | null, data?: Array<DestinationType>} = await req.json()
    if (resp.data) {
      const data: Array<DestinationType> = resp.data
      setDestinations((oldData)=>{
        const newDestinationsMap = new Map(oldData)
        data.forEach(elt => {
          // console.log(elt)
          newDestinationsMap.set(elt.destination_id, elt)
        })        
        return newDestinationsMap
      })
    }
  }

  useEffect(()=>{
    fetchTrips()
    fetchDestinations
  }, [])

  return (
    <TripContext.Provider value={{ trips, createTrip, fetchTrips, updateTrip, destinations, createDestination, fetchDestinations }}>
      {children}
    </TripContext.Provider>
  )
}

export const useTripCtx = () => {
  const context = useContext(TripContext)
  if (!context) {
    throw new Error("useTripCtx must be used in A TripContext Provider")
  }
  return context
}
