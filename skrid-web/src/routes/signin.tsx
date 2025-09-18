import { createFileRoute, redirect, Link, useNavigate } from '@tanstack/react-router'
import { useState, useRef, useEffect } from 'react';
import type { ChangeEvent, MouseEvent } from 'react'

import { useAuth } from '@/auth';

import { IoBus } from 'react-icons/io5'

export const Route = createFileRoute('/signin')({
  component: SignIn,
})

function SignIn() {
  const auth = useAuth()
  const navigate = useNavigate()

  const [email, setEmail] = useState<string>('')
  const [password, setPassword] = useState<string>('')

  const modal = useRef<HTMLDivElement>(null)

  const populateEmail = async (e: ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target?.value)
  }
  const populatePassword = async (e: ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target?.value)
  }

  const doLogin = async () => {
    if (!email) {
      alert('Email is required!')
      return
    } else if (!password) {
      alert('Password is required!')
      return
    }
    await auth.login(email, password)
  }

  const handleModal = (e: MouseEvent<HTMLDivElement>) => {
    if (e.target == modal.current) {
      auth.toggleAuthForm('signin')
    }
  }

  useEffect(()=>{
    if (auth.isAuthenticated) {
      navigate({
        to: '/'
      })
    }
  }, [auth.isAuthenticated])

  return (
    <div ref={modal} className="flex flex-col justify-start items-center w-screen h-screen bg-slate-900" onClick={(e)=> handleModal(e)}>
      <div className="flex flex-col justify-center items-center w-[80%] py-4 px-4 gap-6">

        <div className="flex flex-col justify-center items-center w-full py-4 gap-y-4 rounded-lg">
          <div className="flex flex-col justify-center items-center w-16 h-16 bg-slate-800 rounded-full">
            <IoBus size={36} />
          </div>
          {/* <span className="font-bold text-lg">Welcome, traveler</span>*/}
          <span className="font-bold text-lg">Sign in to <Link to='/' className="text-blue-500">Skeez Travel</Link></span>
        </div>
        <div className="flex flex-col justify-center items-center w-full">
          <div className="flex flex-col justify-center items-center w-full p-2 gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Email</span>
            <input
              type="email"
              className="flex w-full h-10 bg-slate-900 outline-2 outline-slate-800 focus:border-blue-500 focus:outline-blue-500 p-4 rounded-lg text-white"
              onChange={(e)=> populateEmail(e)}
            />
          </div>
          <div className="flex flex-col justify-center items-center w-full p-2 gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Password</span>
            <input
              type="password"
              className="flex w-full h-10 bg-slate-900 outline-2 outline-slate-800 focus:outline-blue-500 focus:border-blue-500 p-4 rounded-lg text-white"
              onChange={(e)=> populatePassword(e)}
            />
          </div>
        </div>
        <button
          onClick={(e)=> doLogin()}
          className="flex justify-center items-center w-full h-10 rounded-lg bg-blue-500 font-bold text-sm text-white">Sign in</button>
        <div className="flex flex-col justify-cebter items-center w-full text-sm gap-y-3 px-2">
          <span>New to Skeez Travel? <Link to='/signup' className="text-blue-500">Sign up</Link></span>
          <Link to="/recovery" className="text-blue-500">Recover account</Link>
        </div>
      </div>
    </div>
  )
}
