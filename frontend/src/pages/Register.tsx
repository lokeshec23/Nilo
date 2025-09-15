import { useState } from "react";
import { register } from "@/api/auth";
import { useNavigate, Link } from "react-router-dom";

export default function RegisterPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await register(email, fullName, password);
      navigate("/login"); // ✅ react-router navigation
    } catch {
      setError("Registration failed");
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
          <h4 className="fw-bold">Sign up for Nilo</h4>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <input
              type="text"
              className="form-control"
              placeholder="Full Name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <input
              type="email"
              className="form-control"
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <input
              type="password"
              className="form-control"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <div className="text-danger small mb-2">{error}</div>}
          <button type="submit" className="btn btn-primary w-100 mb-3">
            Sign up
          </button>
        </form>

        <div className="text-center">
          <small>
            Already have an account?{" "}
            <Link to="/login" className="text-primary text-decoration-none">
              Log in
            </Link>
          </small>
        </div>
      </div>
    </div>
  );
}
