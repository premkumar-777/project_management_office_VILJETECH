import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getProjects, createProject } from "../../../networking/projectApi";
import "../../../App.css";

const ProjectsPage = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  const [form, setForm] = useState({
    project_name: "",
    client_name: "",
    location: "",
    description: "",
    start_date: "",
    end_date: "",
  });

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    const data = await getProjects();
    setProjects(data);
  };

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createProject(form);
    setIsOpen(false);
    fetchProjects();
  };

  return (
    <div>
      <h1>Projects</h1>

      <button className="primary-btn" onClick={() => setIsOpen(true)}>
        + Create Project
      </button>

      {isOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>Create Project</h2>
            <form onSubmit={handleSubmit}>
              <input name="project_name" placeholder="Project Name" onChange={handleChange} required />
              <input name="client_name" placeholder="Client Name" onChange={handleChange} required />
              <input name="location" placeholder="Location" onChange={handleChange} required />
              <textarea name="description" placeholder="Description" onChange={handleChange} required />
              <input type="date" name="start_date" onChange={handleChange} required />
              <input type="date" name="end_date" onChange={handleChange} required />
              <button className="primary-btn">Create</button>
            </form>
          </div>
        </div>
      )}

      <table className="user-table">
        <thead>
          <tr>
            <th>Project Name</th>
            <th>Client</th>
          </tr>
        </thead>
        <tbody>
          {projects.map((p) => (
            <tr
              key={p.id}
              onClick={() => navigate(`/admin/projects/${p.id}`)}
              style={{ cursor: "pointer" }}
            >
              <td>{p.project_name}</td>
              <td>{p.client_name}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ProjectsPage;