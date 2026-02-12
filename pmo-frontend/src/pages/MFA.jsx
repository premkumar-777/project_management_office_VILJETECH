import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";

function MFA() {
  const [otp, setOtp] = useState("");
  const navigate = useNavigate();

const handleVerify = async () => {
  try {
    const res = await API.post("/auth/verify-mfa", {
      temp_token: localStorage.getItem("temp_token"),
      otp: otp,
    });

    localStorage.setItem("access_token", res.data.access_token);
    navigate("/dashboard");
  } catch (err) {
    alert("Invalid OTP");
    console.log(err.response?.data);
  }
};



  return (
    <div className="container">
      <h2>MFA Verification</h2>
      <input
        type="text"
        placeholder="Enter OTP"
        onChange={(e) => setOtp(e.target.value)}
      />
      <button onClick={handleVerify}>Verify</button>
    </div>
  );
}

export default MFA;
