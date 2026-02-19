import { useEffect, useState } from "react";

export default function DashboardPage() {
  const [roles, setRoles] = useState([]);

  useEffect(() => {
    const rolesFromStorage = JSON.parse(localStorage.getItem("roles")) || [];
    setRoles(rolesFromStorage);
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      {roles.includes("Super Admin") && <p>Welcome Super Admin! You can add users.</p>}
      {roles.includes("Admin") && <p>Welcome Admin! Limited management access.</p>}
      {roles.includes("Employee") && <p>Welcome Employee! Your projects will appear here.</p>}
      {roles.includes("Project Manager") && <p>Welcome PM! Manage your team.</p>}
    </div>
  );
}
