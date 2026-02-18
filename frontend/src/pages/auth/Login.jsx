import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../../networking/authApi";
import "../../App.css";

const Login = () => {
  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await loginUser(form);

      if (!res.success) {
        setError(res.message || "Invalid credentials");
        return;
      }

      const data = res.data;

      // If MFA required
      if (data.mfa_required) {
        localStorage.setItem("temp_token", data.temp_token);

        const normalizedRole = data.roles[0].toLowerCase();
        localStorage.setItem("role", normalizedRole);

        navigate("/mfa");
        return;
      }

      // Direct login (client case)
      if (data.access_token) {
        localStorage.setItem("access_token", data.access_token);

        const normalizedRole = data.roles[0].toLowerCase();
        localStorage.setItem("role", normalizedRole);

        navigate(getDashboardRoute(normalizedRole));
      }

    } catch (err) {
      setError("Invalid credentials");
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Login</h2>

        {error && <p className="error">{error}</p>}

        <input
          type="email"
          name="email"
          placeholder="Email"
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={handleChange}
          required
        />

        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;