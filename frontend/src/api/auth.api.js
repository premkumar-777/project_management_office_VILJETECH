import api from "./axios";

// LOGIN
export const loginApi = (data) =>
  api.post("/auth/login", data);

// VERIFY MFA
export const verifyMfaApi = (data) =>
  api.post("/auth/verify-mfa", data);

// REFRESH TOKEN
export const refreshTokenApi = (data) =>
  api.post("/auth/refresh", data);

// REGISTRATION (SET PASSWORD)
export const registrationApi = (data) =>
  api.post("/auth/registration", data);

// FORGOT PASSWORD
export const forgotPasswordApi = (data) =>
  api.post("/password/forgot", data);

// VERIFY OTP
export const verifyOtpApi = (data) =>
  api.post("/password/verify-otp", data);

// RESET PASSWORD
export const resetPasswordApi = (data) =>
  api.post("/password/reset", data);

// REGENERATE MFA QR
export const regenerateQrApi = (data) =>
  api.post("/mfa/regenerate-qr", data);
