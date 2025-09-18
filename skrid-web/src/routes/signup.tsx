import { createFileRoute, redirect, Link, useNavigate } from '@tanstack/react-router'
import { useState, useRef, useEffect } from 'react';
import type { ChangeEvent, MouseEvent } from 'react'

import { useAuth } from '@/auth';

import { IoBus } from 'react-icons/io5'

export const Route = createFileRoute('/signup')({
  component: SignUp,
})
function SignUp() {
  const auth = useAuth()
  
  const navigate = useNavigate()

  const [email, setEmail] = useState<string>(null)
  const [password, setPassword] = useState<string>(null)
  const [password2, setPassword2] = useState<string>(null)
  const [firstname, setFirstName] = useState<string>(null)
  const [lastname, setLastName] = useState<string>(null)
  const [othername, setOtherName] = useState<string>(null)
  const [phone, setPhoneNumber] = useState<string>(null)

  const modal = useRef<HTMLDivElement>(null)
  const phonePrefixRef = useRef<string>(null)

  const populateEmail = async (e: ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target?.value)
  }
  const populatePassword = async (e: ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target?.value)
  }

  const populateConfirmPassword = async (e: ChangeEvent<HTMLInputElement>) => {
    setPassword2(e.target?.value)
  }
  const populateFirstName = async (e: ChangeEvent<HTMLInputElement>) => {
    setFirstName(e.target?.value)
  }
  const populateLastName = async (e: ChangeEvent<HTMLInputElement>) => {
    setLastName(e.target?.value)
  }
  const populateOtherName = async (e: ChangeEvent<HTMLInputElement>) => {
    setOtherName(e.target?.value)
  }
  const populatePhoneNumber = async (e: ChangeEvent<HTMLInputElement>) => {
    setPhoneNumber(phonePrefixRef.current.value + e.target?.value)
  }

  const doSignup = async () => {
    if (!email) {
      alert('Email is required!')
    } else if (!password) {
      alert('Password is required!')
    } else if (!password2) {
      alert('Password2 is required!')
    } else if (!firstname) {
      alert('First name is required!')
    } else if (!lastname) {
      alert('Last name is required!')
    } else if (!phone) {
      alert('Phone number is required!')
    } else {
      await auth.signup({email, password, password2, firstname, lastname, othername, phone})
    }
  }

  const handleModal = (e: MouseEvent<HTMLDivElement>) => {
    if (e.target == modal.current) {
      auth.toggleAuthForm('signup')
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
    <div ref={modal} className="flex flex-col justify-center items-center w-screen h-screen bg-slate-900" onClick={(e)=> handleModal(e)} >
      <div className="flex flex-col justify-start items-center w-[80%] py-4 px-4 gap-6 rounded-2xl">
        <div className="flex flex-col justify-center items-center w-full py-4 gap-y-2 rounded-lg">
          <div className="flex flex-col justify-center items-center w-16 h-16 bg-slate-800 rounded-full">
            <IoBus size={36} />
          </div>
          {/* <span className="font-bold text-lg">Welcome, traveler</span>*/}
          <span className="font-bold text-lg">Sign up for <Link to='/' className="text-blue-500">Skeez Travel</Link></span>
        </div>
        <div className="flex flex-col justify-center items-center w-full">
          <div className="flex flex-col justify-center items-center w-full p-2 gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Email</span>
            <input
              type="email"
              className="flex w-full h-10 bg-slate-900 outline-2 outline-slate-800 focus:border-blue-500 focus:outline-blue-500 p-4 rounded-lg"
              onChange={(e)=> populateEmail(e)}
            />
          </div>
          <div className="flex flex-col justify-center items-center w-full p-2 gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">First Name</span>
            <input
              type="text"
              className="flex w-full h-10 bg-slate-900 outline-2 outline-slate-800 focus:border-blue-500 focus:outline-blue-500 p-4 rounded-lg"
              onChange={(e)=> populateFirstName(e)}
            />
          </div>
          <div className="flex flex-col justify-center items-center w-full p-2 gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Last Name</span>
            <input
              type="text"
              className="flex w-full h-10 bg-slate-900 outline-2 outline-slate-800 focus:border-blue-500 focus:outline-blue-500 p-4 rounded-lg"
              onChange={(e)=> populateLastName(e)}
            />
          </div>
          <div className="flex flex-col justify-center items-center w-full p-2 gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Other Name</span>
            <input
              type="text"
              className="flex w-full h-10 bg-slate-900 outline-2 outline-slate-800 focus:border-blue-500 focus:outline-blue-500 p-4 rounded-lg"
              onChange={(e)=> populateOtherName(e)}
            />
          </div>
          <div className="flex flex-col justify-center items-center w-full p-2 gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Phone</span>
            <div className="flex justify-center items-center w-full h-10">
              <input
                ref={phonePrefixRef}
                type="text"
                disabled
                value="+234"
                className="flex justify-center items-center w-[20%] h-full bg-slate-900 outline-2 outline-slate-800 focus:border-blue-500 focus:outline-blue-500 p-4 rounded-l-lg" />
              <input
                type="number"
                maxlength="10"
                className="flex w-[80%] h-full bg-slate-900 outline-2 outline-slate-800 focus:border-blue-500 focus:outline-blue-500 p-4 rounded-r-lg"
                onChange={(e)=> populatePhoneNumber(e)} />
            </div>
          </div>
          <div className="flex flex-col justify-center items-center w-full p-2 gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Password</span>
            <input
              type="password"
              className="flex w-full h-10 bg-slate-900 outline-2 outline-slate-800 focus:border-blue-500 focus:outline-blue-500 p-4 rounded-lg"
              onChange={(e)=> populatePassword(e)}
            />
          </div>
          <div className="flex flex-col justify-center items-center w-full p-2 gap-y-2">
            <span className="flex justify-start items-center w-full font-bold text-sm">Confirm Password</span>
            <input
              type="password"
              className="flex w-full h-10 bg-slate-900 outline-2 outline-slate-800 focus:border-blue-500 focus:outline-blue-500 p-4 rounded-lg"
              onChange={(e)=> populateConfirmPassword(e)}
            />
          </div>
        </div>
        <button
          onClick={(e)=> doSignup()}
          className="flex justify-center items-center w-full h-10 rounded-lg bg-blue-500 font-bold text-sm text-white">Create</button>
        <div className="flex justify-center items-center w-full h-12 text-sm px-2">
          <span>Already have an account? <Link to='/signin' className="text-blue-500">Sign in</Link></span>
        </div>
      </div>
    </div>
  )
}
