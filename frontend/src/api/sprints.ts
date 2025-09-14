import apiClient from "./client";

export async function createSprint(projectId: string, name: string, goal?: string) {
  const res = await apiClient.post(`/projects/${projectId}/sprints`, { name, goal });
  return res.data;
}

export async function startSprint(id: string) {
  const res = await apiClient.post(`/sprints/${id}/start`);
  return res.data;
}

export async function completeSprint(id: string) {
  const res = await apiClient.post(`/sprints/${id}/complete`);
  return res.data;
}
