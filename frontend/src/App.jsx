import { Routes, Route } from "react-router-dom";
import Login from "./pages/auth/Login";
import MFAOtp from "./pages/auth/MFAOtp";
import SuperAdminDashboard from "./pages/dashboards/SuperAdminDashboard";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/mfa" element={<MFAOtp />} />
      <Route path="/super-admin/dashboard" element={<SuperAdminDashboard />} />
    </Routes>
  );
}

export default App;