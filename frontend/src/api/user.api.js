import api from "./axios";

export const addUserApi = (data) =>
  api.post("/users/add", data);
