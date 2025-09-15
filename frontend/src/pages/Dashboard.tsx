import { useEffect, useState } from "react";
import AppLayout from "@/layouts/AppLayout";
import { createProject } from "@/api/projects";

interface Project {
  id: string;
  key: string;
  name: string;
  description?: string;
}

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [name, setName] = useState("");
  const [key, setKey] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    // TODO: fetch projects from backend
    setProjects([
      {
        id: "1",
        key: "NILO",
        name: "Nilo App",
        description: "Build Jira clone",
      },
    ]);
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const project = await createProject(key, name, description);
      setProjects([...projects, project]);
      setName("");
      setKey("");
      setDescription("");
    } catch (err) {
      console.error("Create project failed", err);
    }
  };

  return (
    <AppLayout>
      <div className="container py-4">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h1 className="h4">Your Projects</h1>

          {/* Create Project Button (Bootstrap Modal Trigger) */}
          <button
            className="btn btn-primary"
            data-bs-toggle="modal"
            data-bs-target="#createProjectModal"
          >
            Create Project
          </button>
        </div>

        {/* Projects Grid */}
        <div className="row g-3">
          {projects.map((p) => (
            <div className="col-12 col-sm-6 col-lg-4" key={p.id}>
              <div
                className="card h-100 shadow-sm"
                role="button"
                onClick={() =>
                  (window.location.href = `/projects/${p.id}/board`)
                }
              >
                <div className="card-body">
                  <h5 className="card-title text-primary">{p.name}</h5>
                  <h6 className="card-subtitle mb-2 text-muted">{p.key}</h6>
                  <p className="card-text small">{p.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Create Project Modal */}
        <div
          className="modal fade"
          id="createProjectModal"
          tabIndex={-1}
          aria-hidden="true"
        >
          <div className="modal-dialog">
            <div className="modal-content">
              <form onSubmit={handleCreate}>
                <div className="modal-header">
                  <h5 className="modal-title">Create Project</h5>
                  <button
                    type="button"
                    className="btn-close"
                    data-bs-dismiss="modal"
                    aria-label="Close"
                  ></button>
                </div>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label">Project Key</label>
                    <input
                      type="text"
                      className="form-control"
                      value={key}
                      onChange={(e) => setKey(e.target.value)}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label">Project Name</label>
                    <input
                      type="text"
                      className="form-control"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label">Description</label>
                    <textarea
                      className="form-control"
                      value={description}
                      onChange={(e) => setDescription(e.target.value)}
                    />
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="submit" className="btn btn-primary">
                    Create
                  </button>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    data-bs-dismiss="modal"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
