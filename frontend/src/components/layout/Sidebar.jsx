import { useNavigate } from "react-router-dom";
import "./Sidebar.css";

const Sidebar = ({ selectedMenu, setSelectedMenu }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    sessionStorage.clear();
    navigate("/");
  };

  return (
    <div className="sidebar">
      <h2 className="sidebar-title">PMO Tool</h2>

      <div className="sidebar-menu">
        <div
          className={`menu-item ${
            selectedMenu === "users" ? "active" : ""
          }`}
          onClick={() => setSelectedMenu("users")}
        >
          All Users
        </div>

        <div
          className={`menu-item ${
            selectedMenu === "projects" ? "active" : ""
          }`}
          onClick={() => setSelectedMenu("projects")}
        >
          Projects
        </div>
      </div>

      <button className="logout-btn" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
};

export default Sidebar;