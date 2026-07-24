import React from 'react'
import { ArrowRight } from 'lucide-react';

const RightCardContent = () => {
  return (
     <div className='absolute top-0 left-0 h-full w-full p-8 flex flex-col justify-between '>
                    <h2 className='bg-white rounded-full text-2xl font-semibold h-14 w-14 flex justify-center items-center'>1</h2>
                    <div>
                        <p className='text-xl leading-relaxed font-semibold text-white mb-10 text-xl'>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Eveniet perferendis error temporibus.</p>
                        <div className='flex justify-between'>
                        <button className=" font-semibold bg-blue-600 text-white font-medium px-8 py-2 rounded-full">
                            Satisfied
                        </button>
                        <button className='font-semibold bg-blue-600 text-white font-medium px-3 py-2 rounded-full'><ArrowRight size={18} /></button>
                    </div>
    
                </div>
            </div>
  )
}

export default RightCardContent

