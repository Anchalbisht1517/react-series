import React from 'react'
import { Bookmark } from 'lucide-react'

const Card = (props) => {
  return (
    
      <div className='card'>
      <div>
        <div className='top'>
            <img src={props.img} alt="" />
            <button>Save <Bookmark size={10}/> </button>
        </div>
        <div className='center'>
            <h3>{props.user} <span>{props.pan}</span></h3>
            <h2>{props.designation}</h2>
            <div className='tag'>
                <h4>{props.type}</h4>
                <h4>{props.level}</h4>
            </div>
        </div>
        </div>
        <div className="bottom">
                <div>
                  <h3>{props.price}</h3> 
                  <p>{props.places}</p> 
                </div>
                <button>Apply Now</button>
        </div>   
      </div>
    
  )
}

export default Card
