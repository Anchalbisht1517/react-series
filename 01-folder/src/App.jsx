import React from 'react'
import Card from './component/card'

const App = () => {

  const jobs = [
    {
      img: "https://pngimg.com/uploads/meta/meta_PNG12.png",
      user: "Meta",
      pan: "5 days ago",
      designation: "Frontend Engineer",
      type: "Full Time",
      level: "Junior Level",
      price: "$65/hour",
      places: "Menlo Park, USA"
    },
    {
      img: "https://static.vecteezy.com/system/resources/previews/014/018/561/non_2x/amazon-logo-on-transparent-background-free-vector.jpg",
      user: "Amazon",
      pan: "2 weeks ago",
      designation: "Backend Developer",
      type: "Full Time",
      level: "Mid Level",
      price: "$70/hour",
      places: "Hyderabad, India"
    },
    {
      img: "https://substackcdn.com/image/fetch/$s_!G1lk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8ed3d547-94ff-48e1-9f20-8c14a7030a02_2000x2000.jpeg",
      user: "Apple",
      pan: "3 weeks ago",
      designation: "iOS Developer",
      type: "Part Time",
      level: "Senior Level",
      price: "$90/hour",
      places: "Cupertino, USA"
    },
    {
      img: "https://images.ctfassets.net/4cd45et68cgf/Rx83JoRDMkYNlMC9MKzcB/2b14d5a59fc3937afd3f03191e19502d/Netflix-Symbol.png?w=700&h=456",
      user: "Netflix",
      pan: "10 days ago",
      designation: "Machine Learning Engineer",
      type: "Full Time",
      level: "Senior Level",
      price: "$110/hour",
      places: "Los Gatos, USA"
    },
    {
      img: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/1200px-Google_%22G%22_logo.svg.png",
      user: "Google",
      pan: "1 week ago",
      designation: "Cloud Solutions Architect",
      type: "Full Time",
      level: "Mid Level",
      price: "$85/hour",
      places: "Bangalore, India"
    },
    {
      img: "https://download.logo.wine/logo/Microsoft_Store/Microsoft_Store-Logo.wine.png",
      user: "Microsoft",
      pan: "4 weeks ago",
      designation: "Data Scientist",
      type: "Full Time",
      level: "Junior Level",
      price: "$75/hour",
      places: "Redmond, USA"
    },
    {
      img: "https://blog.logomaster.ai/hs-fs/hubfs/ibm-logo-1967.jpg?width=672&height=454&name=ibm-logo-1967.jpg",
      user: "IBM",
      pan: "2 days ago",
      designation: "AI Research Engineer",
      type: "Full Time",
      level: "Senior Level",
      price: "$95/hour",
      places: "New York, USA"
    },
    {
      img: "https://www.pngplay.com/wp-content/uploads/13/Tesla-Logo-PNG-HD-Quality.png",
      user: "Tesla",
      pan: "6 days ago",
      designation: "Software Engineer",
      type: "Full Time",
      level: "Mid Level",
      price: "$80/hour",
      places: "Austin, USA"
    },
    {
      img: "https://www.nvidia.com/content/dam/en-zz/Solutions/about-nvidia/logo-and-brand/nvidia-og-image-white-bg-1200x630.jpg",
      user: "NVIDIA",
      pan: "3 weeks ago",
      designation: "GPU Programmer",
      type: "Full Time",
      level: "Senior Level",
      price: "$120/hour",
      places: "Santa Clara, USA"
    },
    {
      img: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnOVjTWaheo4E99cgYZ6y14tpsgHlm0VN8Hw&s",
      user: "Oracle",
      pan: "8 days ago",
      designation: "Database Administrator",
      type: "Full Time",
      level: "Mid Level",
      price: "$70/hour",
      places: "Mumbai, India"
    }
  ];

  return (
    <div className="parent">
      {jobs.map((job, index) => (
        <Card
          key={index}
          user={job.user}
          img={job.img}
          pan={job.pan}
          designation={job.designation}
          type={job.type}
          level={job.level}
          price={job.price}
          places={job.places}
        />
      ))}
    </div>
  );
};

export default App;