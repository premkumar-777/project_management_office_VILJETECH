import { Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/layout/ProtectedRoute";

import Login from "./pages/auth/Login";
import MFAOtp from "./pages/auth/MFAOtp";

import SuperAdminDashboard from "./pages/dashboards/SuperAdminDashboard";
import AdminLayout from "./pages/dashboards/admin/AdminLayout";
import PMLayout from "./pages/dashboards/projectManager/PMLayout";
import EmployeeLayout from "./pages/dashboards/employee/EmployeeLayout";
import ClientLayout from "./pages/dashboards/client/ClientLayout";
import Home from "./pages/Home";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/mfa" element={<MFAOtp />} />

      <Route
        path="/super-admin/dashboard"
        element={
          <ProtectedRoute allowedRoles={["super admin"]}>
            <SuperAdminDashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin/*"
        element={
          <ProtectedRoute allowedRoles={["admin"]}>
            <AdminLayout />
          </ProtectedRoute>
        }
      />

      <Route
        path="/pm/*"
        element={
          <ProtectedRoute allowedRoles={["project manager"]}>
            <PMLayout />
          </ProtectedRoute>
        }
      />

      <Route
        path="/employee/*"
        element={
          <ProtectedRoute allowedRoles={["employee"]}>
            <EmployeeLayout />
          </ProtectedRoute>
        }
      />

      <Route
        path="/client/*"
        element={
          <ProtectedRoute allowedRoles={["client"]}>
            <ClientLayout />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

export default App;