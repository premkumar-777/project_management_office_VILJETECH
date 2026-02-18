import DashboardLayout from "../../../components/layout/DashboardLayout";

const AdminLayout = () => {
  const adminMenu = [
    { label: "Dashboard", path: "/admin/dashboard" },
    { label: "Projects", path: "/admin/projects" },
    { label: "Users", path: "/admin/users" },
    { label: "Approvals", path: "/admin/approvals" },
  ];

  return <DashboardLayout menuItems={adminMenu} />;
};

export default AdminLayout;