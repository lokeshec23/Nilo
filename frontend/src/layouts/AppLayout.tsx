import { ReactNode } from "react";
import Header from "./Header";
import { NavLink } from "react-router-dom";

export default function AppLayout({ children }: { children: ReactNode }) {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `btn mb-2 text-start ${isActive ? "btn-primary" : "btn-light"}`;

  return (
    <div className="d-flex min-vh-100">
      {/* Desktop Sidebar */}
      <nav
        className="d-none d-md-flex flex-column p-3 bg-body-tertiary border-end"
        style={{ width: "220px" }}
      >
        <h5 className="mb-4">Nilo</h5>
        <NavLink to="/dashboard" className={linkClass}>
          Dashboard
        </NavLink>
        <NavLink to="/projects" className={linkClass}>
          Projects
        </NavLink>
        <NavLink to="/backlog" className={linkClass}>
          Backlog
        </NavLink>
        <NavLink to="/board" className={linkClass}>
          Board
        </NavLink>
      </nav>

      {/* Main content */}
      <div className="flex-grow-1 d-flex flex-column">
        {/* Header (sticky top) */}
        <Header />

        {/* Page content */}
        <main className="p-3 bg-body flex-grow-1">{children}</main>
      </div>

      {/* Mobile Offcanvas Sidebar */}
      <div
        className="offcanvas offcanvas-start"
        tabIndex={-1}
        id="sidebarMenu"
        aria-labelledby="sidebarMenuLabel"
      >
        <div className="offcanvas-header">
          <h5 className="offcanvas-title" id="sidebarMenuLabel">
            Nilo
          </h5>
          <button
            type="button"
            className="btn-close"
            data-bs-dismiss="offcanvas"
            aria-label="Close"
          ></button>
        </div>
        <div className="offcanvas-body d-flex flex-column">
          <NavLink
            to="/dashboard"
            className={linkClass}
            data-bs-dismiss="offcanvas"
          >
            Dashboard
          </NavLink>
          <NavLink
            to="/projects"
            className={linkClass}
            data-bs-dismiss="offcanvas"
          >
            Projects
          </NavLink>
          <NavLink
            to="/backlog"
            className={linkClass}
            data-bs-dismiss="offcanvas"
          >
            Backlog
          </NavLink>
          <NavLink
            to="/board"
            className={linkClass}
            data-bs-dismiss="offcanvas"
          >
            Board
          </NavLink>
        </div>
      </div>
    </div>
  );
}
