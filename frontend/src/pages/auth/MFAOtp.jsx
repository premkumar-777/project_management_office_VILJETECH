import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { verifyMFA } from "../../networking/authApi";
import { getDashboardRoute } from "../../utils/roleRedirect";
import "../../App.css";

const MFAOtp = () => {
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const tempToken = localStorage.getItem("temp_token");

    if (!tempToken) {
      setError("Session expired. Please login again.");
      navigate("/login");
      return;
    }

    try {
      const res = await verifyMFA({
        temp_token: tempToken,
        otp: otp.trim(), // backend expects string
      });

      if (!res.success) {
        setError(res.message || "Invalid OTP");
        return;
      }

      const data = res.data;

      localStorage.setItem("access_token", data.access_token);

      const normalizedRole = data.roles[0].toLowerCase();
      localStorage.setItem("role", normalizedRole);

      localStorage.removeItem("temp_token");

      navigate(getDashboardRoute(normalizedRole));

    } catch (err) {
      setError("Invalid OTP");
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>MFA Verification</h2>

        {error && <p className="error">{error}</p>}

        <input
          type="text"
          placeholder="Enter OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
          required
        />

        <button type="submit">Verify</button>
      </form>
    </div>
  );
};

export default MFAOtp;