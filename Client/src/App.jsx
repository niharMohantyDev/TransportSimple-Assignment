import './App.css'
import Register from './components/User/Register'
import Login from './components/User/Login'
import { BrowserRouter as Router, Routes, Route} from "react-router";
import Dashboard from './components/Dashboard/Dashboard'
import Logout from './components/Dashboard/Logout'

function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path = "/register" element={<Register/>}/>
          <Route path = "/login" element={<Login/>}/>
          <Route path="/dashboard" element={<Dashboard />} /> 
          <Route path="/logout" element={<Logout />} /> 
        </Routes>
      </Router>
    </>
  )
}

export default App
