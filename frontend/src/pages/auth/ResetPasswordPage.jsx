import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { resetPasswordApi } from "../../api";

export default function ResetPasswordPage() {
  const [newPassword, setNewPassword] = useState("");
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const email = searchParams.get("email");

  const handleReset = async () => {
    try {
      await resetPasswordApi({ email, new_password: newPassword });
      alert("Password reset successfully!");
      navigate("/auth/login");
    } catch (err) {
      console.error(err.response?.data?.message || err.message);
      alert(err.response?.data?.message || "Password reset failed");
    }
  };

  return (
    <div>
      <h2>Reset Password</h2>
      <input type="password" placeholder="New Password" value={newPassword} onChange={e => setNewPassword(e.target.value)} />
      <button onClick={handleReset}>Reset</button>
    </div>
  );
}
