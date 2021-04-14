import React from 'react'
import "../styles/login.css"
import { Link } from "react-router-dom";
import { ReactComponent as Email } from "../svg/email.svg"
import { ReactComponent as Password } from "../svg/padlock.svg"

function Login() {
    return (
        <div>
            <div className="flex-centre page">
                <div className="loginLogo"></div>
                <form className="flex-centre login-centre">
                    <div className="login">
                        <div className="input-container">
                            <Email className="input-svg"></Email>
                            <div className="input-label-container">
                                <label className="input-label">Email</label>
                                <input placeholder="Enter Email"></input>
                            </div>
                            
                        </div>
                        <div className="input-container">
                            <Password className="input-svg"></Password>
                            <div className="input-label-container">
                                <label className="input-label">Password</label>
                                <input placeholder="Enter Password"></input>
                            </div> 
                        </div> 
                    </div>
                    
                    <Link to="/main" className="button">LOGIN</Link>
                </form>  
            </div>
        </div>
    )
}

export default Login