import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  // Check if user is already logged in
  useEffect(() => {
    const accessToken = localStorage.getItem("accessToken");
    if (accessToken) {
      navigate("/dashboard");
    }
  }, [navigate]);

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleMessage = (message) => {
    setMessage(message);
  };

  const handleSubmit = () => {
    axios
      .post("http://127.0.0.1:8000/users/login", {
        username: username,
        password: password,
      })
      .then((response) => {
        console.log(response.data);

        const { accessToken } = response.data;
        localStorage.setItem("accessToken", accessToken);
        const responseMessage = "Login Successful";
        handleMessage(responseMessage);
        navigate("/dashboard"); 
      })
      .catch((error) => {
        console.error("Login failed:", error);
        handleMessage("Login failed. Please try again.");
      });
  };

  return (
    <div>
      <h2>Login</h2>
      <br />
      <input
        type="text"
        placeholder="Please enter your username"
        value={username}
        onChange={handleUsernameChange}
      />
      <br /><br />
      <input
        type="password"
        placeholder="Please enter your password"
        value={password}
        onChange={handlePasswordChange}
      />
      <br /><br />
      <button onClick={handleSubmit}>Submit</button>
      <br /><br />
      <div>{message}</div>
    </div>
  );
};

export default Login;
