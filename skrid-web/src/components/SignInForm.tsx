import { useState, useRef } from 'react';
import type { ChangeEvent, MouseEvent } from 'react'

import { useAuth } from '@/auth';

export const SignInForm = () => {
  const auth = useAuth()

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
  return (
    <div ref={modal} className="flex flex-col justify-end items-center w-screen h-dvh absolute z-10 bg-slate-900/80" onClick={(e)=> handleModal(e)}>
      <div className="flex flex-col justify-center items-center w-full bg-slate-800 py-4 px-4 gap-6 rounded-t-4xl">
        <div className="flex flex-col justify-center items-center w-full">
          <span className="font-bold text-lg">Welcome, traveler</span>
          <span className="font-bold text-lg">Sign In</span>
        </div>
        <div className="flex flex-col justify-center items-center w-full">
          <div className="flex flex-col justify-center items-center w-full p-2 gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-lg">Email</span>
            <input
              type="email"
              className="flex w-full h-12 outline p-4 rounded-full"
              onChange={(e)=> populateEmail(e)}
            />
          </div>
          <div className="flex flex-col justify-center items-center w-full p-2 gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-lg">Password</span>
            <input
              type="password"
              className="flex w-full h-12 outline p-4 rounded-full"
              onChange={(e)=> populatePassword(e)}
            />
          </div>
        </div>
        <button
          onClick={(e)=> doLogin()}
          className="flex justify-center items-center w-full h-12 rounded-full bg-blue-800 font-bold text-lg text-white">Sign in</button>
      </div>
    </div>
  )
}
