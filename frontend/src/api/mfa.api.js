// src/api/mfa.api.js
import api from "./axios";

// 🔹 Setup MFA for a specific user (user_id from temp_token)
export const setupMfaApi = (user_id, temp_token) => {
  return api.post(`/mfa/setup/${user_id}`, { temp_token });
};

// 🔹 Verify MFA OTP for a specific user
export const verifyMfaApi = (user_id, { temp_token, otp }) => {
  return api.post(`/mfa/verify/${user_id}`, { temp_token, otp });
};

// 🔹 Regenerate MFA QR (optional)
export const regenerateQrApi = ({ email, otp }) => {
  return api.post("/mfa/regenerate-qr", { email, otp });
};
