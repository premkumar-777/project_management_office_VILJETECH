import { useState, useEffect } from "react";
import Sidebar from "../../components/layout/Sidebar";
import Modal from "../../components/ui/Modal";
import { createUser, getUsers } from "../../networking/userApi";
import "../../App.css";

const SuperAdminDashboard = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [users, setUsers] = useState([]);
  const [message, setMessage] = useState("");

  const [form, setForm] = useState({
    name: "",
    email: "",
    location: "",
    role: "admin",
  });

  // ✅ FIXED FUNCTION
  const fetchUsers = async () => {
    try {
      const data = await getUsers();
      setUsers(data);
    } catch (error) {
      console.error("Failed to fetch users", error);
    }
  };

  // ✅ CALL ON LOAD
  useEffect(() => {
    fetchUsers();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // ✅ FIXED PAYLOAD (roles as array)
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const payload = {
        name: form.name,
        email: form.email,
        location: form.location,
        roles: [form.role],   // IMPORTANT
      };

      const res = await createUser(payload);
      setMessage(res.message);
      setIsOpen(false);
      fetchUsers();   // refresh list
    } catch (err) {
      console.error(err.response?.data);
      alert("Failed to create user");
    }
  };

  const countByRole = (role) =>
    users.filter((u) => u.roles?.[0] === role).length;

  return (
    <div className="layout">
      <Sidebar />

      <div className="main-content">
        <h1>Super Admin Dashboard</h1>

        <div className="card-grid">
          <div className="card">Admins: {countByRole("admin")}</div>
          <div className="card">PMs: {countByRole("project manager")}</div>
          <div className="card">Employees: {countByRole("employee")}</div>
          <div className="card">Clients: {countByRole("client")}</div>
        </div>

        <button className="primary-btn" onClick={() => setIsOpen(true)}>
          + Add Resource
        </button>

        {message && <p className="success">{message}</p>}

        <table className="user-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Location</th>
              <th>Role</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id}>
                <td>{u.name}</td>
                <td>{u.email}</td>
                <td>{u.location}</td>
                <td>{u.roles?.[0]}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <Modal isOpen={isOpen} onClose={() => setIsOpen(false)}>
          <h2>Add Resource</h2>

          <form onSubmit={handleSubmit}>
            <input
              name="name"
              placeholder="Name"
              onChange={handleChange}
              required
            />

            <input
              name="email"
              placeholder="Email"
              onChange={handleChange}
              required
            />

            <input
              name="location"
              placeholder="Location"
              onChange={handleChange}
              required
            />

            <select name="role" onChange={handleChange}>
              <option value="admin">Admin</option>
              <option value="project manager">Project Manager</option>
              <option value="employee">Employee</option>
              <option value="client">Client</option>
            </select>

            <button className="primary-btn">Invite</button>
          </form>
        </Modal>
      </div>
    </div>
  );
};

export default SuperAdminDashboard;