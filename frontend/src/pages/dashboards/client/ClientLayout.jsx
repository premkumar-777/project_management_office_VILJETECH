import DashboardLayout from "../../../components/layout/DashboardLayout";

const ClientLayout = () => {
  const clientMenu = [
    { label: "Dashboard", path: "/client/dashboard" },
    { label: "Projects", path: "/client/projects" },
  ];

  return <DashboardLayout menuItems={clientMenu} />;
};

export default ClientLayout;