import { Link } from '@tanstack/react-router'
import { useAuth } from '@/auth';

export default function Header() {

  return (
    <div className="grid grid-cols-3 w-full h-full px-2">
    {/*<div className="flex justify-start items-center h-full font-bold">*/}
        <Link to="/" className="col-start-2 flex justify-center items-center w-full h-full">
          <img src="/src/skrid.png" className="w-20 h-20 aspect-1/1 object-cover"/>
        </Link>
        {/*</div>*/}
    </div>
  )
}
