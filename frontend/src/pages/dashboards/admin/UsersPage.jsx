import { useNavigate } from "react-router-dom";

const UsersPage = () => {
  const navigate = useNavigate();

  const dummyUsers = [
    { id: 1, name: "John", role: "employee" },
    { id: 2, name: "Sara", role: "project manager" }
  ];

  return (
    <div>
      <h1>Users</h1>

      <table className="user-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Role</th>
          </tr>
        </thead>
        <tbody>
          {dummyUsers.map((u) => (
            <tr
              key={u.id}
              onClick={() => navigate(`/admin/users/${u.id}`)}
              style={{ cursor: "pointer" }}
            >
              <td>{u.name}</td>
              <td>{u.role}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UsersPage;