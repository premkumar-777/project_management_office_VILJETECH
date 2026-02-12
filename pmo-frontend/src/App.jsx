import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import MFA from "./pages/MFA";
import Dashboard from "./pages/Dashboard";
import AddUser from "./pages/AddUser";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/mfa" element={<MFA />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/add-user" element={<AddUser />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
