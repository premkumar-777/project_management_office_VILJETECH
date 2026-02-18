import api from "./api";

export const loginUser = async (data) => {
  const response = await api.post("/auth/login", data);
  return response.data;
};

export const setPassword = async (data) => {
  const response = await api.post("/auth/set-password", data);
  return response.data;
};

export const verifyMFA = async (data) => {
  const response = await api.post("/auth/verify-mfa", data);
  return response.data;
};