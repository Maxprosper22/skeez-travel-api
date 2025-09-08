import { useAuth } from '@/auth'

export const AuthBtn = ({value}: {value:string}) => {
  const { toggleAuthForm, login, logout } = useAuth()
  // console.log(value)
  return (
    <>
    {
      value == 'signin' ? (<button className="flex justify-center items-center w-full h-10 text-lg font-bold rounded-xl bg-blue-500" onClick={()=> toggleAuthForm('signin')}>Sign in</button>)
    : value == 'signup' ? (<button className="flex justify-center items-center w-full h-10 text-lg font-bold rounded-lg bg-blue-500/20 border border-blue-500 text-blue-500" onClick={()=> toggleAuthForm('signup')}>Sign up</button>)
    :
      <div className="flex justify-center items-center w-[80%] h-10 rounded-lg border border-red-500 text-red-500 text-lg font-bold" onClick={()=> logout()}>Sign out</div>
    }
    </>
  )
}
