import DashboardLayout from "../../../components/layout/DashboardLayout";

const PMLayout = () => {
  const pmMenu = [
    { label: "Dashboard", path: "/pm/dashboard" },
    { label: "Projects", path: "/pm/projects" },
    { label: "Approvals", path: "/pm/approvals" },
    { label: "My Requests", path: "/pm/requests" },
  ];

  return <DashboardLayout menuItems={pmMenu} />;
};

export default PMLayout;