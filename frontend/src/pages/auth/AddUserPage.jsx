import { useState } from "react";
import { addUserApi } from "../../api/user.api";

export default function AddUserPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [roleId, setRoleId] = useState(4); // Employee default
  const [location, setLocation] = useState("");

  const handleAddUser = async () => {
    try {
      const res = await addUserApi({
        name,
        email,
        roles: [roleId],
        location,
        status_id: 1, // INVITED
      });

      if (res.data.success) {
        alert("User added! Invite URL: " + res.data.data.invite_url);
      }
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.detail || "Failed to add user");
    }
  };

  return (
    <div>
      <h2>Add User</h2>
      <input placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
      <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input placeholder="Location" value={location} onChange={e => setLocation(e.target.value)} />
      <select value={roleId} onChange={e => setRoleId(Number(e.target.value))}>
        <option value={1}>Super Admin</option>
        <option value={2}>Admin</option>
        <option value={3}>Project Manager</option>
        <option value={4}>Employee</option>
        <option value={5}>Client</option>
      </select>
      <button onClick={handleAddUser}>Add User</button>
    </div>
  );
}
