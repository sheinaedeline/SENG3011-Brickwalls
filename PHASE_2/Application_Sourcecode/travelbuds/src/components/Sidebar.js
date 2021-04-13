import React from 'react'
import "../styles/sidebar.css"
import { Link } from "react-router-dom";
import { ReactComponent as Home} from "../svg/home.svg"
import { ReactComponent as Group} from "../svg/group.svg"
import { ReactComponent as Info} from "../svg/information.svg"
import { ReactComponent as Logout} from "../svg/logout.svg"
import { ReactComponent as Settings} from "../svg/settings.svg"
import { ReactComponent as Trip} from "../svg/tracking.svg"
import { ReactComponent as User } from "../svg/user.svg"

function Sidebar() {
    return (
        <div className="sidebar">
            <input type="checkbox" id="nav-toggle" className="nav-toggle"></input>
            <label htmlFor="nav-toggle" className="nav-toggle-label">
                <span></span>
            </label>
            <div className="sidebar-input">
                <input placeholder="Search Destinations"></input>
            </div>
            <nav className="sidebar-content">
                <ul>
                    <li className="profile-container">
                        <div className="sidebar-profile">
                            <User className="sidebar-profile-svg"></User>
                            <div className="profile-container">
                                <p className="sidebar-name">Name</p>
                                <p className="sidebar-group">Group Name</p>
                            </div> 
                        </div>
                    </li>
                    <li>
                        <Link to="/main" className="sidebar-link">
                            <Home className="sidebar-svg"></Home>
                            <div>Home</div>
                        </Link>
                    </li>
                    <li>
                        <Link to="/group" className="sidebar-link">
                            <Group className="sidebar-svg"></Group>
                            <div>Group</div>
                        </Link>
                    </li>
                    <li>
                        <Link to="/trips" className="sidebar-link">
                            <Trip className="sidebar-svg"></Trip>
                            <div>Trips</div>
                        </Link>
                    </li>
                    <li>
                        <Link to="/help" className="sidebar-link">
                            <Info className="sidebar-svg"></Info>
                            <div>Help</div>
                        </Link>
                    </li>
                    <li>
                        <Link to="/settings" className="sidebar-link">
                            <Settings className="sidebar-svg"></Settings>
                            Settings
                        </Link>
                    </li>
                    <li>
                        <Link to="/">
                            <Logout className="sidebar-svg"></Logout>
                            Logout
                        </Link>
                    </li>
                </ul>
            </nav>
        </div>
    )
}

export default Sidebar