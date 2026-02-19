import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { verifyMFA } from "../../networking/authApi";

const MFAOtp = () => {
  const navigate = useNavigate();

  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");

  const handleVerify = async (e) => {
    e.preventDefault();

    const tempToken = sessionStorage.getItem("temp_token");

    if (!tempToken) {
      setError("Session expired. Please login again.");
      return;
    }

    try {
      const response = await verifyMFA({
        temp_token: tempToken,
        otp: otp,
      });

      // 🔥 Extract correct backend structure
      const data = response.data;

      if (response.success) {
        // Store tokens
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
        localStorage.setItem("role", data.roles[0]);

        // Clear temp token
        sessionStorage.removeItem("temp_token");

        // Redirect based on role
        if (data.roles[0] === "Super Admin") {
          navigate("/super-admin/dashboard");
        } else {
          navigate("/");
        }
      }

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Invalid OTP or session expired"
      );
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>MFA Verification</h2>

        <form onSubmit={handleVerify}>
          <input
            type="text"
            placeholder="Enter OTP"
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
            required
          />

          <button type="submit">Verify</button>
        </form>

        {error && <p className="error">{error}</p>}
      </div>
    </div>
  );
};

export default MFAOtp;