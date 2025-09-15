import { ReactNode } from "react";
import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";

export default function AppLayout({ children }: { children: ReactNode }) {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="d-flex min-vh-100">
      {/* Sidebar */}
      <nav
        className="d-none d-md-flex flex-column p-3 bg-body-tertiary border-end"
        style={{ width: "220px" }}
      >
        <h5 className="mb-4">Nilo</h5>
        <a href="/dashboard" className="btn btn-light mb-2 text-start">
          Dashboard
        </a>
        <a href="/projects" className="btn btn-light mb-2 text-start">
          Projects
        </a>
        <a href="/backlog" className="btn btn-light mb-2 text-start">
          Backlog
        </a>
        <a href="/board" className="btn btn-light mb-2 text-start">
          Board
        </a>
      </nav>

      {/* Main content area */}
      <div className="flex-grow-1 d-flex flex-column">
        {/* Top bar */}
        <header className="d-flex justify-content-between align-items-center p-2 border-bottom bg-body-tertiary">
          <span>Welcome {user?.email}</span>
          <div className="d-flex gap-2">
            <button className="btn btn-outline-secondary" onClick={toggleTheme}>
              {theme === "light" ? "Dark" : "Light"} Mode
            </button>
            <button className="btn btn-outline-danger" onClick={logout}>
              Logout
            </button>
          </div>
        </header>

        {/* Page content - flex-grow makes it stretch */}
        <main className="p-3 bg-body flex-grow-1">{children}</main>
      </div>
    </div>
  );
}
