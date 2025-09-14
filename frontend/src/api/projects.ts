import apiClient from "./client";

export async function createProject(key: string, name: string, description?: string) {
  const res = await apiClient.post("/projects", { key, name, description });
  return res.data;
}

export async function getProject(id: string) {
  const res = await apiClient.get(`/projects/${id}`);
  return res.data;
}

export async function inviteMember(projectId: string, email: string, roles: string[]) {
  const res = await apiClient.post(`/projects/${projectId}/invite`, { email, roles });
  return res.data;
}

export async function listMembers(projectId: string) {
  const res = await apiClient.get(`/projects/${projectId}/members`);
  return res.data;
}
