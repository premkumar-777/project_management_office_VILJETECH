import { useState } from "react";
import { forgotPasswordApi } from "../../api";


export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleForgot = async () => {
    try {
      const res = await forgotPasswordApi({ email });
      setMessage(`OTP sent to ${email}`);
    } catch (err) {
      console.error(err.response?.data?.message || err.message);
      alert(err.response?.data?.message || "Error sending OTP");
    }
  };

  return (
    <div>
      <h2>Forgot Password</h2>
      <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <button onClick={handleForgot}>Send OTP</button>
      <p>{message}</p>
    </div>
  );
}
