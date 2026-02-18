import { NavLink, useNavigate } from "react-router-dom";
import "../../App.css";

const Sidebar = ({ menuItems = [] }) => {   // ✅ default empty array
  const navigate = useNavigate();

  const role = localStorage.getItem("role");

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <div className="sidebar">
      <h2>PMO Tool</h2>
      <p className="sidebar-user">{role}</p>

      <nav>
        {menuItems.length > 0 &&
          menuItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                isActive ? "sidebar-link active" : "sidebar-link"
              }
            >
              {item.label}
            </NavLink>
          ))}
      </nav>

      <button onClick={handleLogout} className="logout-btn">
        Logout
      </button>
    </div>
  );
};

export default Sidebar;