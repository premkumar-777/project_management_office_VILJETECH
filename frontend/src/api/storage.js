// storage.js - central place for tokens and session data

const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";
const TEMP_TOKEN_KEY = "temp_token";

// Save tokens
export const setAccessToken = (token) =>
  localStorage.setItem(ACCESS_TOKEN_KEY, token);

export const getAccessToken = () =>
  localStorage.getItem(ACCESS_TOKEN_KEY);

export const removeAccessToken = () =>
  localStorage.removeItem(ACCESS_TOKEN_KEY);

export const setRefreshToken = (token) =>
  localStorage.setItem(REFRESH_TOKEN_KEY, token);

export const getRefreshToken = () =>
  localStorage.getItem(REFRESH_TOKEN_KEY);

export const removeRefreshToken = () =>
  localStorage.removeItem(REFRESH_TOKEN_KEY);

export const setTempToken = (token) =>
  sessionStorage.setItem(TEMP_TOKEN_KEY, token);

export const getTempToken = () =>
  sessionStorage.getItem(TEMP_TOKEN_KEY);

export const removeTempToken = () =>
  sessionStorage.removeItem(TEMP_TOKEN_KEY);

// Clear all tokens
export const clearAuthStorage = () => {
  removeAccessToken();
  removeRefreshToken();
  removeTempToken();
};
