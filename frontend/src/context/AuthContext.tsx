import  { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { login as apiLogin, logout as apiLogout, refreshToken } from "../api/auth";

interface AuthContextType {
  user: any | null;
  accessToken: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<any | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(
    localStorage.getItem("access_token")
  );

  // Load user profile when token exists
  useEffect(() => {
    if (accessToken) {
      // TODO: fetch user profile if backend has /me
      setUser({ email: "placeholder@example.com" }); // replace when user API ready
    }
  }, [accessToken]);

  const login = async (email: string, password: string) => {
    const res = await apiLogin(email, password);
    setAccessToken(res.access_token);
    setUser({ email }); // replace with real user from backend
  };

  const logout = () => {
    apiLogout();
    setAccessToken(null);
    setUser(null);
  };

  // Handle auto refresh if access token expires
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (accessToken) {
      interval = setInterval(async () => {
        try {
          await refreshToken();
          setAccessToken(localStorage.getItem("access_token"));
        } catch (err) {
          console.error("Failed to refresh token", err);
          logout();
        }
      }, 1000 * 60 * 10); // every 10 mins
    }
    return () => clearInterval(interval);
  }, [accessToken]);

  return (
    <AuthContext.Provider
      value={{
        user,
        accessToken,
        login,
        logout,
        isAuthenticated: !!accessToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// ✅ Hook to use auth easily
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
