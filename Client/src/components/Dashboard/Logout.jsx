import React from 'react'
import './Logout.css'
import { useNavigate } from 'react-router'
import axios from 'axios'

const Logout = () => {
    const navigate = useNavigate()
    
    const handleLogout = async (logoutFromAll = false) => {
        const accessToken = localStorage.getItem("accessToken");
        if (!accessToken) {
            navigate("/login");
            return;
        }

        try {
            const response = await axios.post(
                "http://localhost:8000/users/logout",
                {
                    logoutFromAllOtherDevices: logoutFromAll,
                    logout: !logoutFromAll // If we're logging out from all, this is false, and vice versa
                },
                {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                        "Content-Type": "application/json",
                    },
                }
            )

            if (response.status === 200) {
                alert(logoutFromAll 
                    ? "Logged out from all other devices successfully" 
                    : "Logout successful");
                
                // If it's a normal logout (not logout from all), clear local storage
                if (!logoutFromAll) {
                    localStorage.removeItem("accessToken")
                    navigate("/login")
                }
            }
        } catch (error) {
            console.error("Logout failed:", error);
            alert("Logout failed. Please try again.");
        }
    }

    const handleSubmit = () => {
        handleLogout(false); // Normal logout
    }

    const handleSubmitToLogoutFromAll = () => {
        handleLogout(true); // Logout from all devices
    }

    return (
        <div>
            <button className='LObtn' onClick={handleSubmit}>Logout</button>
            <br /><br />
            <button className='LObtn' onClick={handleSubmitToLogoutFromAll}>
                Logout from other devices
            </button>
        </div>
    )
}

export default Logout