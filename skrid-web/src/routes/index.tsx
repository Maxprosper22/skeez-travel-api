import { createFileRoute, Link } from '@tanstack/react-router'
import Header from '@/components/Header'
import { MdBookmarkAdd, MdCopyright } from "react-icons/md";
import { FaLuggageCart } from "react-icons/fa";
import { IoPricetags } from "react-icons/io5";

export const Route = createFileRoute('/')({
  component: RouteComponent,
})

function RouteComponent() {
  return (
    <div className="/*grid grid-rows-12 grid-cols-5*/ flex flex-col justify-start items-center w-full h-full overflow-auto">
      <div className="/*row-span-1 col-span-5*/ flex justify-center items-center w-full h-20 fixed top-0 bg-slate-950">
        <Header />
      </div>
      {/*<div className="flex flex-col justify-start items-center w-full h-full overflow-auto">*/}
        {/* Banner */}
        <div className="flex flex-col justify-center items-center w-full min-h-full gap-y-12">
          <div className="flex justify-center items-center w-full h-[23em]">
            <img src="/src/banner.png" className="aspect-1/1" />
          </div>
          <div className="flex flex-col justify-evenly items-center w-full">
            <div className="flex flex-col justify-evenly items-center w-[80%] gap-y-4 text-center font-mono">
              <p>The one stop agency for all your transportation needs. From online trip booking to waybills, we've got you covered</p>

                {/*<p>Colors: Cool blues, silvers, or gradients that convey innovation and trustworthiness, or alternatively, bold neon accents for a cutting-edge look.</p>*/}
            </div>
          </div>
          {/*<div className="flex flex-col justify-evenly items-center w-[80%] gap-4 text-sm font-bold font-mono">*/}
          {/*<button className="flex justify-center items-center w-full h-12 bg-blue-500 outline-none outline-slate-800 active:outline-blue-500 focus:border-blue-500 p-4 rounded-lg text-white">Get Started</button>*/}
            {/*}<button className="flex justify-center items-center w-full h-12 bg-slate-900 outline-2 outline-slate-800 active:outline-blue-500 focus:border-blue-500 p-4 rounded-lg text-white">Book</button>*/}
          {/*</div>*/}
        </div>
        {/* Banner end */}

        {/* Banner */}
        <div className="flex flex-col justify-center items-center w-[90%] h-[32em] mx-auto my-4 px-4 py-12 gap-y-8 bg-slate-950 border border-slate-800 rounded-lg">
          <div className="flex justify-center items-center w-[6em] h-[6em] rounded-full">
            <MdBookmarkAdd color="white" size={52} />
          </div>
          <div className="flex flex-col justify-evenly items-center w-full">
            <div className="flex flex-col justify-evenly items-center w-[80%] gap-y-4 text-center font-mono">
              <p className="text-lg font-bold">Seamless Online Booking</p>
            </div>
          </div>
        </div>
        {/* Banner end */}

        {/* Banner */}
        <div className="flex flex-col justify-center items-center w-[90%] h-[32em] mx-auto my-4 px-4 py-12 gap-y-8 bg-slate-950 border border-slate-800 rounded-lg">
          <div className="flex justify-center items-center w-[6em] h-[6em] rounded-full">
            <IoPricetags color="white" size={52} />
          </div>
          <div className="flex flex-col justify-evenly items-center w-full">
            <div className="flex flex-col justify-evenly items-center w-[80%] gap-y-4 text-center font-mono">
              <p className="text-lg font-bold">Cheap And Affordable Prices</p>
              {/*<span className="text-sm">Cheap? Yes, and comfy too!</span>*/}
            </div>
          </div>
        </div>
        {/* Banner end */}

        {/* Banner */}
        <div className="flex flex-col justify-center items-center w-[90%] h-[32em] mx-auto my-4 px-4 py-12 gap-y-8 bg-slate-950 border border-slate-800 rounded-lg">
          <div className="flex justify-center items-center w-[6em] h-[6em] rounded-full">
            <FaLuggageCart color="white" size={52} />
          </div>
          <div className="flex flex-col justify-evenly items-center w-full">
            <div className="flex flex-col justify-evenly items-center w-[80%] gap-y-4 text-center font-mono">
              <p className="text-lg font-bold">Fast Parcel Delivery</p>
            </div>
          </div>
        </div>
        {/* Banner end */}

        {/* Banner */}
        <div className="flex flex-col justify-center items-center w-full my-8 p-4 gap-y-8">
        {/*<div className="flex justify-center items-center w-full">
            <MdBookmarkAdd color="white" size={62} />
          </div>*/}
          <div className="flex flex-col justify-evenly items-center w-full">
            <div className="flex flex-col justify-evenly items-center w-[80%] gap-y-4 text-center font-mono">
            {/*<p className="text-lg font-bold">Online Booking</p>*/}

              <p>Ready to travel?</p>
            </div>
          </div>
          <div className="flex flex-col justify-evenly items-center w-[80%] gap-4 text-sm font-bold font-mono">
            <Link to="/home" className="flex justify-center items-center w-full h-12 bg-blue-500 outline-none outline-slate-800 active:outline-blue-500 focus:border-blue-500 p-4 rounded-lg text-white">Get Started</Link>
          </div>
        </div>
        {/* Banner end */}

        {/* Footer */}
        <div className="flex flex-col justify-around items-center w-full h-[32em] p-4 gap-y-4 divide divide-y divide-slate-800">
          <Link to="/" className="col-start-2 flex justify-center items-center w-full h-[30%]">
            <img src="/src/skrid.png" className="w-20 h-20 aspect-1/1 object-cover"/>
          </Link>
          <div className="flex flex-col justify-evenly items-center w-full h-[40%] pb-4">
            <div className="flex flex-col justify-evenly items-center w-[80%] gap-y-4 text-center font-mono">
              <p className="text-sm font-bold">Trips</p>

              <p className="text-sm font-bold">Destinations</p>
              <p className="text-sm font-bold">Contact</p>
            </div>
          </div>
          <div className="flex justify-center items-center w-[80%] h-[30%] gap-4 text-sm font-bold font-mono">
            <MdCopyright size={24} />
            <span className="text-sm font-bold">Skeez Group</span>
          </div>
        </div>
        {/* Footer end */}
    </div>
  )
}
