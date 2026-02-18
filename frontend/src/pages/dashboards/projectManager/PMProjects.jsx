import { useNavigate } from "react-router-dom";

const PMProjects = () => {
  const navigate = useNavigate();

  const projects = [
    { id: 1, name: "Project A" },
    { id: 2, name: "Project B" }
  ];

  return (
    <div>
      <h2>My Projects</h2>

      <table className="user-table">
        <thead>
          <tr>
            <th>Project Name</th>
          </tr>
        </thead>
        <tbody>
          {projects.map((p) => (
            <tr key={p.id} onClick={() => navigate(`/pm/projects/${p.id}`)}>
              <td>{p.name}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PMProjects;