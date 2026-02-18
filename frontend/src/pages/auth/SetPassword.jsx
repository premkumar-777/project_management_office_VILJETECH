import { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { setPassword } from "../../networking/authApi";
import { getDashboardRoute } from "../../utils/roleRedirect";
import "../../App.css";

const SetPassword = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const tokenFromUrl = searchParams.get("token");

  const [form, setForm] = useState({
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");

  useEffect(() => {
    if (tokenFromUrl) {
      localStorage.setItem("temp_token", tokenFromUrl);
    }
  }, [tokenFromUrl]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    const tempToken = localStorage.getItem("temp_token");

    try {
      const res = await setPassword({
        temp_token: tempToken,
        password: form.password,
      });

      if (res.mfa_required) {
        localStorage.setItem("temp_token", res.temp_token);
        navigate("/mfa");
        return;
      }

      if (res.access_token) {
        localStorage.setItem("access_token", res.access_token);
        localStorage.setItem("user", JSON.stringify(res.user));

        const route = getDashboardRoute(res.user.roles);
        navigate(route);
      }
    } catch (err) {
      setError("Failed to set password");
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Create Password</h2>

        {error && <p className="error">{error}</p>}

        <input
          type="password"
          name="password"
          placeholder="Create Password"
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm Password"
          onChange={handleChange}
          required
        />

        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default SetPassword;