import { useNavigate } from "react-router-dom";

const EmployeeProjects = () => {
  const navigate = useNavigate();

  return (
    <div>
      <h2>My Assigned Projects</h2>
      <table className="user-table">
        <thead>
          <tr>
            <th>Project</th>
          </tr>
        </thead>
        <tbody>
          <tr onClick={() => navigate("/employee/projects/1")}>
            <td>Project Alpha</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default EmployeeProjects;