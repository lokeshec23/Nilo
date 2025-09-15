import { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(email, password);
      navigate("/dashboard"); // ✅ react-router navigation
    } catch {
      setError("Invalid credentials");
    }
  };

  return (
    <div className="d-flex align-items-center justify-content-center vh-100 bg-body">
      <div className="card shadow-sm p-4" style={{ width: "360px" }}>
        <div className="text-center mb-3">
          <img
            src="https://wac-cdn.atlassian.com/assets/img/favicons/atlassian/favicon.png"
            alt="Nilo Logo"
            width="40"
            className="mb-2"
          />
          <h4 className="fw-bold">Log in to Nilo</h4>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <input
              type="email"
              className="form-control"
              placeholder="Enter email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <input
              type="password"
              className="form-control"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <div className="text-danger small mb-2">{error}</div>}
          <button type="submit" className="btn btn-primary w-100 mb-3">
            Log in
          </button>
        </form>

        <div className="text-center">
          <small>
            Don’t have an account?{" "}
            <Link to="/register" className="text-primary text-decoration-none">
              Sign up
            </Link>
          </small>
        </div>
      </div>
    </div>
  );
}
