import api from "./api";

export const getProjects = async () => {
  const res = await api.get("/projects/");
  return res.data;
};

export const createProject = async (data) => {
  const res = await api.post("/projects/", data);
  return res.data;
};

export const getMyProjects = async () => {
  const res = await api.get("/projects/my");
  return res.data;
};

export const assignMembers = async (projectId, data) => {
  const res = await api.post(`/projects/${projectId}/assign`, data);
  return res.data;
};

export const getProjectMembers = async (projectId) => {
  const res = await api.get(`/projects/${projectId}/members`);
  return res.data;
};