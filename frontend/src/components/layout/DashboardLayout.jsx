import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import "../../App.css";

const DashboardLayout = ({ menuItems }) => {
  return (
    <div className="layout">
      <Sidebar menuItems={menuItems} />
      <div className="main-content">
        <Outlet />
      </div>
    </div>
  );
};

export default DashboardLayout;