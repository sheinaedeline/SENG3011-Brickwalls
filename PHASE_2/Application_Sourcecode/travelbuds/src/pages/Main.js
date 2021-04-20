import React from 'react'
import "../styles/main.css"
import Sidebar from "../components/Sidebar.js"
import Countryprofile from "../components/Countryprofile.js"

function Main() {
    return (
        <div>
            <Sidebar></Sidebar>
            <Countryprofile></Countryprofile>
        </div>
    )
}

export default Main