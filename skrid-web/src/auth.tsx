import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { ReactNode } from 'react';

import type { TripType } from '@/trips'

export interface AuthContext {
  user: AccountType | null;
  isAuthenticated: boolean;
  token: string | null;
  login: (email: string, password: string) => void;
  logout: () => void;
  showSignInForm: boolean;
  showSignUpForm: boolean;
  toggleAuthForm: (formType: string) => void;
}

export interface AccountType {
  account_id: string;
  email: string;
  phone: string;
  firstname: string;
  lastname: string;
  othername: string;
  is_admin: boolean;
  join_date: Date;
  admin: object | null;
  trips: Array<TripType> | null;
}

export type SlotType = Omit<AccountType, 'admin' | 'trips'>

const AuthContext = createContext<AuthContext | undefined>(undefined)

const userKey = 'skrid.auth.user'
const tokenKey = 'skrid.auth.token' 

function getStoredUser(): AccountType | null {
  const user = localStorage.getItem(userKey)
  if (!user) return null;
  try {
    return JSON.parse(user)
  } catch (error) {
    console.error('Error parsing stored user: ', error)
    return null
  }
}

function setStoredUser(user: AccountType | null) {
  if (user) {
    localStorage.setItem(userKey, JSON.stringify(user))
  } else {
    localStorage.removeItem(userKey)
  }
}

function getStoredAuthToken(): string | null {
  const token = localStorage.getItem(tokenKey)
  if (!token) return null;
  try {
    return token
  } catch(error) {
    console.error('Error reading stored token: ', error)
    return null
  }
}

function setStoredAuthToken(token: string | null) {
  if (token) {
    localStorage.setItem(tokenKey, token)
  } else {
    localStorage.removeItem(tokenKey)
  }
}
export const AuthProvider = ({children}: {children: ReactNode}) => {
  const [user, setUser] = useState<AccountType | null>(getStoredUser());
  const [authToken, setAuthToken] = useState<string | null>(getStoredAuthToken());
  const [showSignInForm, setShowSigninForm] = useState<boolean>(false)
  const [showSignUpForm, setShowSignupForm] = useState<boolean>(false)

  const isAuthenticated = !!user
  
  const toggleAuthForm = async (formType: string) => {
    if (isAuthenticated) {
      return
    } else {
      if (formType=='signin') {
        setShowSigninForm(!showSignInForm)
      } else {
        setShowSignupForm(!showSignUpForm)
      }
    }
  }
  const login = useCallback(async (email:string, password:string) => {
    const req = await fetch('http://127.0.0.1:8080/account/signin', {
      method: 'POST',
      body: JSON.stringify({'email': email, 'password': password})
    })

    const resp = await req.json()
    if (resp.authenticated) {
      setStoredUser(resp.data)
      setUser(resp.data)

      setStoredAuthToken(resp.token)
      setAuthToken(resp.token)
      // alert(resp.info)
      // userData = await fetch('http://127.0.0.1:8080/account/signin', {method: "POST"})
    }
  }, [])

  const logout = useCallback(async () => {
    const req = await fetch('http://127.0.0.1:8080/account/signout', {
      method: 'GET',
      headers: {
        'Authorisation': `Bearer: ${authToken}`
      }
    })
    const resp = await req.json()
    // console.log(resp)
    if (req.status == 200) {
      setStoredUser(null)
      setUser(null)

      setStoredAuthToken(null)
      setAuthToken(null)
      // alert(resp.info)
    }
  }, [])

  useEffect(()=>{
    setStoredUser(getStoredUser())
  }, [])

  return (
    <AuthContext.Provider value={{ user, isAuthenticated,  token:authToken, login, logout, showSignInForm, showSignUpForm, toggleAuthForm }}>
      {children}
    </AuthContext.Provider>
  )
  
}
export const useAuth = () => {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
    
  }
  return context;
} 
