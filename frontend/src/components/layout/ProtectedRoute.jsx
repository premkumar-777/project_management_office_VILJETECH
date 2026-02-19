import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children, allowedRoles }) => {
  const token = localStorage.getItem("access_token");
  const role = localStorage.getItem("role");

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && role) {
    const normalizedRole = role.toLowerCase();
    const normalizedAllowedRoles = allowedRoles.map((r) => r.toLowerCase());
    
    if (!normalizedAllowedRoles.includes(normalizedRole)) {
      return <Navigate to="/login" replace />;
    }
  }

  return children;
};

export default ProtectedRoute;