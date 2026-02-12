// import { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import API from "../api";

// function MFA() {
//   const [otp, setOtp] = useState("");
//   const navigate = useNavigate();

// const handleVerify = async () => {
//   try {
//     const res = await API.post("/auth/verify-mfa", {
//       temp_token: localStorage.getItem("temp_token"),
//       otp: otp,
//     });

//     localStorage.setItem("access_token", res.data.access_token);
//     navigate("/dashboard");
//   } catch (err) {
//     alert("Invalid OTP");
//     console.log(err.response?.data);
//   }
// };



//   return (
//     <div className="container">
//       <h2>MFA Verification</h2>
//       <input
//         type="text"
//         placeholder="Enter OTP"
//         onChange={(e) => setOtp(e.target.value)}
//       />
//       <button onClick={handleVerify}>Verify</button>
//     </div>
//   );
// }

// export default MFA;
import { useEffect, useState } from "react";
import axios from "axios";

export default function MFASetup({ userId }) {
  const [qr, setQr] = useState("");
  const [otp, setOtp] = useState("");

  useEffect(() => {
    axios.post(`http://127.0.0.1:8000/mfa/setup/${userId}`)
      .then(res => {
        setQr(res.data.qr_code);
      });
  }, [userId]);

  const verifyOtp = async () => {
    const res = await axios.post(
      `http://127.0.0.1:8000/mfa/verify/${userId}?otp=${otp}`
    );

    alert(res.data.message || res.data.error);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "40px" }}>
      <h2>Scan QR Code for MFA</h2>

      {qr && <img src={qr} alt="QR Code" width="250" />}

      <div style={{ marginTop: "20px" }}>
        <input
          type="text"
          placeholder="Enter OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
        />
        <button onClick={verifyOtp}>Verify</button>
      </div>
    </div>
  );
}
