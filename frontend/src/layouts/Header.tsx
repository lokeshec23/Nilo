import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";

export default function Header() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  const handleToggleTheme = () => {
    try {
      toggleTheme();
    } catch (err) {
      console.error("Theme toggle failed", err);
    }
  };

  const handleLogout = () => {
    try {
      logout();
    } catch (err) {
      console.error("Logout failed", err);
    }
  };

  return (
    <header className="d-flex justify-content-between align-items-center p-2 border-bottom bg-body-tertiary sticky-top">
      {/* Hamburger for mobile */}
      <button
        className="btn btn-outline-secondary d-md-none"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#sidebarMenu"
        aria-controls="sidebarMenu"
      >
        ☰
      </button>

      <span className="ms-2">Welcome {user?.email}</span>

      <div className="d-flex gap-2">
        <button
          className="btn btn-outline-secondary"
          onClick={handleToggleTheme}
        >
          {theme === "light" ? "Dark" : "Light"} Mode
        </button>
        <button className="btn btn-outline-danger" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </header>
  );
}
