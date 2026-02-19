// src/pages/auth/AuthRoutes.jsx
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./LoginPage";
import RegistrationPage from "./RegistrationPage";
import MFASetupPage from "./MFASetupPage";
import MFApage from "./MFApage";
import ForgotPasswordPage from "./ForgotPasswordPage";
import VerifyOtpPage from "./VerifyOtpPage";
import ResetPasswordPage from "./ResetPasswordPage";

export default function AuthRoutes() {
  return (
    <Routes>
      {/* Login page */}
      <Route path="/auth/login" element={<LoginPage />} />

      {/* Registration page */}
      <Route path="/registration" element={<RegistrationPage />} />

      {/* MFA Setup QR page */}
      <Route path="/auth/mfa-setup" element={<MFASetupPage />} />

      {/* MFA OTP verification page */}
      <Route path="/auth/mfa" element={<MFApage />} />

      {/* Forgot Password flow */}
      <Route path="/auth/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/auth/verify-otp" element={<VerifyOtpPage />} />
      <Route path="/auth/reset-password" element={<ResetPasswordPage />} />

      {/* Redirect any unknown auth routes to login */}
      <Route path="/auth/*" element={<Navigate to="/auth/login" replace />} />
    </Routes>
  );
}
