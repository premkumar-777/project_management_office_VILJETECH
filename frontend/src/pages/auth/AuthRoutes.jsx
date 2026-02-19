// src/pages/auth/AuthRoutes.jsx
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./LoginPage";
import RegistrationPage from "./RegistrationPage";
import MFApage from "./MFApage";
import ForgotPasswordPage from "./ForgotPasswordPage";
import VerifyOtpPage from "./VerifyOtpPage";
import ResetPasswordPage from "./ResetPasswordPage";

export default function AuthRoutes() {
  return (
    <Routes>
      {/* Login page */}
      <Route path="/auth/login" element={<LoginPage />} />

      {/* Registration page (via invitation link) */}
      <Route path="/registration/*" element={<RegistrationPage />} />


      {/* MFA page */}
      <Route path="/auth/mfa" element={<MFApage />} />

      {/* Forgot Password flow */}
      <Route path="/auth/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/auth/verify-otp" element={<VerifyOtpPage />} />
      <Route path="/auth/reset-password" element={<ResetPasswordPage />} />

      {/* Redirect unknown auth routes to login */}
      <Route path="/auth/*" element={<Navigate to="/auth/login" replace />} />
    </Routes>
  );
}
