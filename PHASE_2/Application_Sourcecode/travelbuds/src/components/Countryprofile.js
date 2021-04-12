import React from "react"
import "../styles/countryprofile.css"
import Sydney from "../images/Sydney.jpg"

function Countryprofile() {
    return (
        <div className="country-profile">
            <div className="img-container">
                <img src={Sydney} alt="sydney"></img>
                <div className="destination-name">
                    <h1>City Name</h1>
                    <h2>Country Name</h2>
                </div>
            </div>
            
        </div>
    )
}

export default Countryprofile