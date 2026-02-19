import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginApi } from "../../api";
import { setTempToken } from "../../api/storage";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await loginApi({ email, password });

      if (res.data.data.mfa_required) {
        // Save temp_token for MFA verification
        setTempToken(res.data.data.temp_token);
        navigate("/auth/mfa");
      } else {
        console.log("Login successful, no MFA needed");
        // Later you can store access_token if backend allows
      }
    } catch (err) {
      console.error(err.response?.data?.message || err.message);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}
