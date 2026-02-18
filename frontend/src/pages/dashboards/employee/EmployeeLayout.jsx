import DashboardLayout from "../../../components/layout/DashboardLayout";

const EmployeeLayout = () => {
  const employeeMenu = [
    { label: "Dashboard", path: "/employee/dashboard" },
    { label: "My Projects", path: "/employee/projects" },
    { label: "My Requests", path: "/employee/requests" },
  ];

  return <DashboardLayout menuItems={employeeMenu} />;
};

export default EmployeeLayout;