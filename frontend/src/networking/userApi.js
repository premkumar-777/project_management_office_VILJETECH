import api from "./api"; // adjust path if needed

export const createUser = async (data) => {
  const res = await api.post("/users/add", data);
  return res.data;
};

export const getUsers = async () => {
  const res = await api.get("/users");
  return res.data;
};