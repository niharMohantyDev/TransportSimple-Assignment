import React, { useState } from "react";
import axios from "axios";

const Register = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordeChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = () => {
    axios
      .post("http://127.0.0.1:8000/users/register", {
        username: username,
        password: password,
      })
      .then((data) => console.log(data.data))
      .catch((error) => console.log(error));
  };
  return (
    <div>
      Register <br /> <br />
      <input
        type="username"
        placeholder="please enter your username"
        value={username}
        onChange={handleUsernameChange}
      />{" "}
      <br /> <br />
      <input
        type="password"
        placeholder="please enter your password"
        value={password}
        onChange={handlePasswordeChange}
      />{" "}
      <br />
      <br />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default Register;
