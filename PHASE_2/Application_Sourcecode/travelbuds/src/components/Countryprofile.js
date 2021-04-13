import React from "react"
import "../styles/countryprofile.css"
import Sydney from "../images/Sydney.jpg"
import beach from "../images/beach.PNG"
import bridgewalk from "../images/bridgewalk.jpeg"
import dining from "../images/dining.PNG"

function Countryprofile() {
    const info = "From stylish hotels to award-winning restaurants, buzzy small bars, captivating galleries and exhilarating adventures, there’s a new experience for every day in Sydney. Plan a holiday in one of the world’s greatest cities – you won’t even need your passport.\n Sydney. Love it like you mean it."
    return (
        <div className="country-profile gradient-background">
            <div className="img-container">
                <img src={Sydney} alt="sydney"></img>
                <div className="destination-name">
                    <h1>City Name</h1>
                    <h2>Country Name</h2>
                </div>
            </div>
            <ul className="tags-list">
                <li>Beaches</li>
                <li>Captital</li>
                <li>City</li>
                <li>Night-Life</li>
                <li>Nature</li>
                <li>Outdoor</li>
                <li>Landmarks</li>
                <li>Fashion</li>
            </ul>
            <div className="alt-image-container">
                <img src={beach} alt="beach" className="alt-img"></img>
                <img src={bridgewalk} alt="bridgewalk" className="alt-img"></img>
                <img src={dining} alt="dining" className="alt-img"></img>
            </div>
            <p className="country-info">{info}</p>
        </div>
    )
}

export default Countryprofile