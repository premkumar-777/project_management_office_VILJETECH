import { useState, useEffect } from "react";
import Sidebar from "../../components/layout/Sidebar";
import Modal from "../../components/ui/Modal";
import { createUser, getUsers } from "../../networking/userApi";
import "../../App.css";

const SuperAdminDashboard = () => {
  const [selectedMenu, setSelectedMenu] = useState("users");
  const [users, setUsers] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedRoleId, setSelectedRoleId] = useState(null);
  const [message, setMessage] = useState("");

  const [form, setForm] = useState({
    name: "",
    email: "",
    location: "",
  });

  // Role mapping
  const roleConfig = [
    { name: "Admin", id: 2 },
    { name: "Project Manager", id: 3 },
    { name: "Employee", id: 4 },
    { name: "Client", id: 5 },
  ];

  const fetchUsers = async () => {
    try {
      const data = await getUsers();
      setUsers(data);
    } catch (error) {
      console.error("Failed to fetch users", error);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleCardClick = (roleId) => {
    setSelectedRoleId(roleId);
    setIsOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const payload = {
        name: form.name,
        email: form.email,
        location: form.location,
        roles: [selectedRoleId],
        status_id: 1,
      };

      const res = await createUser(payload);

      setMessage(res.message);
      setIsOpen(false);
      setForm({ name: "", email: "", location: "" });
      fetchUsers();

    } catch (err) {
      alert(JSON.stringify(err.response?.data));
    }
  };

  const countByRoleId = (roleId) => {
    return users.filter((u) => u.roles?.[0] === roleId).length;
  };

  const totalUsers = users.length;

  return (
    <div className="dashboard-layout">
      <Sidebar
        selectedMenu={selectedMenu}
        setSelectedMenu={setSelectedMenu}
      />

      <div className="dashboard-content">
        <h1>Super Admin Dashboard</h1>

        {selectedMenu === "users" && (
          <>
            <div className="card-grid">

              {/* Total Users */}
              <div className="card total-card">
                <h3>Total Users</h3>
                <p>{totalUsers}</p>
              </div>

              {/* Role Cards */}
              {roleConfig.map((role) => (
                <div
                  key={role.id}
                  className="card clickable"
                  onClick={() => handleCardClick(role.id)}
                >
                  <h3>{role.name}</h3>
                  <p>{countByRoleId(role.id)}</p>
                </div>
              ))}
            </div>

            {message && <p className="success">{message}</p>}
          </>
        )}

        {selectedMenu === "projects" && (
          <div>
            <h2>Projects Section (Coming Soon)</h2>
          </div>
        )}

        {/* Add User Modal */}
        <Modal isOpen={isOpen} onClose={() => setIsOpen(false)}>
          <h2>Add User</h2>

          <form onSubmit={handleSubmit}>
            <input
              name="name"
              placeholder="Name"
              value={form.name}
              onChange={handleChange}
              required
            />

            <input
              name="email"
              placeholder="Email"
              value={form.email}
              onChange={handleChange}
              required
            />

            <input
              name="location"
              placeholder="Location"
              value={form.location}
              onChange={handleChange}
              required
            />

            <button className="primary-btn">Invite</button>
          </form>
        </Modal>
      </div>
    </div>
  );
};

export default SuperAdminDashboard;