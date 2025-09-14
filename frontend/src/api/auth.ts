import apiClient from "./client";

export async function register(email: string, fullName: string, password: string) {
  debugger
  const res = await apiClient.post("/auth/register", { email, fullName, password });
  return res.data;
}

export async function login(email: string, password: string) {
  try{
    debugger
    const res = await apiClient.post("/auth/login", { email, password });
    if (res.data.access_token) {
      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("refresh_token", res.data.refresh_token);
    }
    return res.data;
  }catch(ex){
    console.error("Error in login function",ex)
  }
}

export async function refreshToken() {
  const refresh_token = localStorage.getItem("refresh_token");
  const res = await apiClient.post("/auth/refresh", { refresh_token });
  if (res.data.access_token) {
    localStorage.setItem("access_token", res.data.access_token);
    localStorage.setItem("refresh_token", res.data.refresh_token);
  }
  return res.data;
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}
