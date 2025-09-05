import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react'

export interface EventContext {
  event: SSEvent | null;
}
export interface SSEvent {
  id: string | null;
  event: string;
  data: {} | string;
}

const EventContext = createContext<EventContext | null>(null)

export const EventProvider = ({children} : {children: ReactNode}) => {
  const [event, setEvent] = useState<SSEvent | null>(null)

  const sse_url = 'http://127.0.0.1:8080/trips/sse'
  // setEvent()

  useEffect(()=>{
    const eventSource = new EventSource(sse_url);

    eventSource.onmessage = (ev) => {
      console.log(ev)
      // const data = JSON.parse(ev)
      // setEvent(ev.data)
    }
    return () => {
      eventSource.close()
    }
  }, [])

  return (
    <EventContext.Provider value={{ event }} >
      {children}
    </EventContext.Provider>
  )
}

export const useEvent = () => {
  const context = useContext(EventContext)
  if (!context) {
    throw new Error('useEvent must be used within an EventProvider')
  }
  return context;
}
