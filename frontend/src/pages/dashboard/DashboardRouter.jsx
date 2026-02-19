import { getAccessToken } from "../../api/storage";
import SuperAdminDashboard from "./SuperAdminDashboard";
import AdminDashboard from "./AdminDashboard";
import UserDashboard from "./UserDashboard";
import ClientDashboard from "./ClientDashboard";

export default function DashboardRouter() {
  const token = getAccessToken();
  let roles = [];

  if (token) {
    const payload = JSON.parse(atob(token.split(".")[1]));
    roles = payload.roles || [];
  }

  // Simple role-based rendering
  if (roles.includes("Super Admin")) return <SuperAdminDashboard />;
  if (roles.includes("Admin")) return <AdminDashboard />;
  if (roles.includes("User")) return <UserDashboard />;
  if (roles.includes("Client")) return <ClientDashboard />;

  return <p>No dashboard available for your role.</p>;
}
