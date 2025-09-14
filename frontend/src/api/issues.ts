import apiClient from "./client";

export async function createIssue(projectId: string, summary: string, description?: string) {
  const res = await apiClient.post("/issues", { projectId, summary, description });
  return res.data;
}

export async function updateIssue(id: string, updates: any) {
  const res = await apiClient.patch(`/issues/${id}`, updates);
  return res.data;
}

export async function transitionIssue(id: string, status: string) {
  const res = await apiClient.post(`/issues/${id}/transition`, { status });
  return res.data;
}

export async function getIssue(id: string) {
  const res = await apiClient.get(`/issues/${id}`);
  return res.data;
}

export async function getBacklog(projectId: string) {
  const res = await apiClient.get(`/issues/projects/${projectId}/backlog`);
  return res.data;
}

export async function getBoard(projectId: string) {
  const res = await apiClient.get(`/issues/projects/${projectId}/board`);
  return res.data;
}
