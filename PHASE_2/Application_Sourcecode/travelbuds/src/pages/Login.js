import React from 'react'
import "../styles/login.css"
import { Link } from "react-router-dom";

function Login() {
    return (
        <div className="gradient-background">
            <div className="flex-centre">
                <div className="loginLogo"></div>
                <form className="flex-centre">
                    <div>
                        <label>Username</label>
                        <input className="login-input" placeholder="Enter Username"></input>
                        <label >Password</label>
                        <input className="login-input" placeholder="Enter Password"></input>
                    </div>
                    <Link to="/main" className="button">Login</Link>
                </form>  
            </div>
             
        </div>
    )
}

export default Login