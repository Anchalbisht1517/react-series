import React from 'react'
import LeftContent from './LeftContent'
import RightContent from './RightContent'

const Page1Content = () => {
  return (
    <div className='py-10 flex items-center justify-between h-[90vh] px-18 gap-10'>
    <LeftContent/>
    <RightContent/>
    </div>
  )
}

export default Page1Content
