import { Link } from '@tanstack/react-router'
import { useAuth } from '@/auth';

export default function Header() {

  return (
    <div className="flex justify-between items-center w-full h-[4em] gap p-2 rounded-2xl">
      <div className="flex justify-start items-center h-full px-2 font-bold">
        <Link to="/" className="flex justify-start items-center w-full font-bold text-2xl">Skrid Travel</Link>
      </div>
    </div>
  )
}
