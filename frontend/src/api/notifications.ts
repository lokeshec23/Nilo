import apiClient from "./client";

export async function getNotifications() {
  const res = await apiClient.get("/notifications");
  return res.data;
}
