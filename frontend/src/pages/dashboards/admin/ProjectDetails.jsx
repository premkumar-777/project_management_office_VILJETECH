import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  assignMembers,
  getProjectMembers,
} from "../../../networking/projectApi";
import { getUsers } from "../../../networking/userApi";
import "../../../App.css";

const ProjectDetails = () => {
  const { projectId } = useParams();
  const [members, setMembers] = useState([]);
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState("");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const memberData = await getProjectMembers(projectId);
    const userData = await getUsers();
    setMembers(memberData);
    setUsers(userData);
  };

  const handleAssign = async () => {
    if (!selectedUser) return;

    await assignMembers(projectId, {
      user_id: selectedUser,
    });

    fetchData();
  };

  return (
    <div>
      <h2>Project Members</h2>

      <div className="detail-card">
        <h3>Assign User</h3>

        <select onChange={(e) => setSelectedUser(e.target.value)}>
          <option value="">Select User</option>
          {users.map((u) => (
            <option key={u.id} value={u.id}>
              {u.name} ({u.roles?.[0]})
            </option>
          ))}
        </select>

        <button className="primary-btn" onClick={handleAssign}>
          Assign
        </button>
      </div>

      <table className="user-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Role</th>
          </tr>
        </thead>
        <tbody>
          {members.map((m) => (
            <tr key={m.id}>
              <td>{m.name}</td>
              <td>{m.roles?.[0]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ProjectDetails;