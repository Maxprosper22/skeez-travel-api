import { createContext, useContext, useState, useEffect, useRef } from 'react';
import type { ReactNode } from 'react'

export interface EventContext {
  event: SSEvent | null;
}
export interface SSEvent {
  id: string | null;
  event: string;
  data: {} | string;
}

const eventUrlKey = "skrid.event.url"
const eventUrl = "https://127.0.0.1:8080/trip/sse"

const getEventUrl = async (): string | null => {
  const url = localStorage.getItem(eventUrlKey)
  if (!url) return null;
  try{
    return url
  } catch(error) {
    console.error('Error reading event url')
    return null
  }
}
const setEventUrl = async (url: string) => {
  if (url) {
    localStorage.setItem(eventUrlKey, url)
  } else {
    localStorage.removeItem(eventUrlkey)
  }
}

const EventContext = createContext<EventContext | null>(null)

export const EventProvider = ({children} : {children: ReactNode}) => {
  // const [url, setUrl] = useState<string>(null)
  const [data, setData] = useState<object>(null);
  const [error, setError] = useState<any>(null);
  const eventSourceRef = useRef<EventSource>(null);
  const retryTimeoutRef = useRef<number>(null);

  useEffect(() => {
    
    // setUrl(getEventUrl)
    const eventSource = new EventSource(eventUrl);
    eventSourceRef.current = eventSource;

    // Listen for default 'message' events
    eventSource.onmessage = (event) => {
      const parsedData = JSON.parse(event.data);
      setData(parsedData);
    };

    // Handle connection open
    eventSource.onopen = () => {
      console.log('SSE connection opened');
      setError(null);
    };

    // Handle errors and auto-reconnect
    eventSource.onerror = (err) => {
      console.error('SSE error:', err);
      setError(err);

      // Auto-reconnect with exponential backoff (built-in, but customizable)
      if (retryTimeoutRef.current) clearTimeout(retryTimeoutRef.current);
      retryTimeoutRef.current = setTimeout(() => {
        // Reopen connection logic here if needed
      }, Math.min(1000 * Math.pow(2, eventSource.lastEventId || 0), 30000)); // Cap at 30s
    };

    // Cleanup on unmount
    return () => {
      if (eventSource) {
        eventSource.close();
      }
      if (retryTimeoutRef.current) {
        clearTimeout(retryTimeoutRef.current);
      }
    };
  }, [eventUrl]);

  return (
    <EventContext.Provider value={{ data, error }} >
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
