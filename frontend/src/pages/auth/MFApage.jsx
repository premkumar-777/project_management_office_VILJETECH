// src/pages/auth/MFApage.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { verifyMfaApi } from "../../api/auth.api";
import { setAccessToken, setRefreshToken, clearAuthStorage } from "../../api/storage";

export default function MFApage() {
  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const tempToken = sessionStorage.getItem("temp_token");

  if (!tempToken) {
    alert("No registration in progress. Please register first.");
    navigate("/registration");
    return null;
  }

  const handleVerify = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await verifyMfaApi({ temp_token: tempToken, otp });

      if (response.success) {
        // Save tokens in localStorage
        setAccessToken(response.data.access_token);
        setRefreshToken(response.data.refresh_token);

        // Clear temp data
        clearAuthStorage();

        // Redirect based on roles (simplified example)
        if (response.data.roles.includes("Super Admin")) {
          navigate("/dashboard/super-admin");
        } else if (response.data.roles.includes("Admin")) {
          navigate("/dashboard/admin");
        } else {
          navigate("/dashboard/employee");
        }
      } else {
        alert(response.message || "OTP verification failed");
      }
    } catch (err) {
      console.error(err);
      alert("OTP verification failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mfa-page">
      <h2>Enter OTP from your Authenticator app</h2>
      <form onSubmit={handleVerify}>
        <input
          type="text"
          placeholder="Enter OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Verifying..." : "Verify OTP"}
        </button>
      </form>
    </div>
  );
}
