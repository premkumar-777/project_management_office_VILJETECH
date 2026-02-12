// import { useState } from "react";
// import API from "../api";

// function AddUser() {
//   const [name, setName] = useState("");
//   const [email, setEmail] = useState("");

//   const handleAddUser = async () => {
//     try {
//       await API.post("/users/add", {
//         name,
//         email,
//         roles: [2],  // Change role id as needed
//         location: "Chennai",
//         status_id: 1,
//       });

//       alert("User Created Successfully");
//     } catch (err) {
//       alert("Unauthorized or Failed");
//     }
//   };

//   return (
//     <div className="container">
//       <h2>Add User</h2>
//       <input
//         type="text"
//         placeholder="Name"
//         onChange={(e) => setName(e.target.value)}
//       />
//       <input
//         type="text"
//         placeholder="Email"
//         onChange={(e) => setEmail(e.target.value)}
//       />
//       <button onClick={handleAddUser}>Create</button>
//     </div>
//   );
// }

// export default AddUser;
import { useState } from "react";
import API from "../api";

function AddUser() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("3"); // default role id
  const [location, setLocation] = useState("");
  const [statusId, setStatusId] = useState("1");

  const handleAddUser = async () => {
    try {
      await API.post("/users/add", {
        name: name,
        email: email,
        roles: [parseInt(role)],   // backend expects list
        location: location,
        status_id: parseInt(statusId),
      });

      alert("User Created Successfully");
    } catch (err) {
      alert("Failed to create user");
      console.log(err.response?.data);
    }
  };

  return (
    <div className="container">
      <h2>Add User</h2>

      <input
        type="text"
        placeholder="Name"
        onChange={(e) => setName(e.target.value)}
      />

      <input
        type="email"
        placeholder="Email"
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="text"
        placeholder="Location"
        onChange={(e) => setLocation(e.target.value)}
      />

      <select onChange={(e) => setRole(e.target.value)}>
        <option value="1">Super Admin</option>
        <option value="2">Admin</option>
        <option value="3">Project Manager</option>
        <option value="4">Employee</option>
      </select>

      <select onChange={(e) => setStatusId(e.target.value)}>
        <option value="1">Active</option>
        <option value="2">Inactive</option>
      </select>

      <button onClick={handleAddUser}>Create User</button>
    </div>
  );
}

export default AddUser;
