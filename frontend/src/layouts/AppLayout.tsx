import { ReactNode } from "react";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { NavigationMenu } from "@/components/ui/navigation-menu";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { useTheme } from "@/context/ThemeContext";
import { useAuth } from "@/context/AuthContext";
import { Menu } from "lucide-react";

export default function AppLayout({ children }: { children: ReactNode }) {
  const { logout, user } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="flex min-h-screen bg-background text-foreground">
      {/* Sidebar (desktop) */}
      <aside className="hidden md:flex w-64 flex-col border-r bg-muted">
        <div className="p-4 text-lg font-bold">Nilo</div>
        <nav className="flex flex-col space-y-2 p-2">
          <Button variant="ghost" className="justify-start">
            Dashboard
          </Button>
          <Button variant="ghost" className="justify-start">
            Projects
          </Button>
          <Button variant="ghost" className="justify-start">
            Backlog
          </Button>
          <Button variant="ghost" className="justify-start">
            Board
          </Button>
        </nav>
      </aside>

      {/* Mobile sidebar trigger */}
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="ghost" size="icon" className="md:hidden m-2">
            <Menu className="h-6 w-6" />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-64">
          <div className="p-4 text-lg font-bold">Nilo</div>
          <nav className="flex flex-col space-y-2 p-2">
            <Button variant="ghost" className="justify-start">
              Dashboard
            </Button>
            <Button variant="ghost" className="justify-start">
              Projects
            </Button>
            <Button variant="ghost" className="justify-start">
              Backlog
            </Button>
            <Button variant="ghost" className="justify-start">
              Board
            </Button>
          </nav>
        </SheetContent>
      </Sheet>

      {/* Main content */}
      <div className="flex-1 flex flex-col">
        {/* Top bar */}
        <header className="flex items-center justify-between border-b bg-muted px-4 py-2">
          <NavigationMenu>
            <span className="font-semibold">Welcome {user?.email}</span>
          </NavigationMenu>
          <div className="flex items-center gap-4">
            <Button variant="outline" onClick={toggleTheme}>
              {theme === "light" ? "Dark" : "Light"} Mode
            </Button>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Avatar>
                  <AvatarFallback>{user?.email?.[0] || "U"}</AvatarFallback>
                </Avatar>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={logout}>Logout</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 p-4">{children}</main>
      </div>
    </div>
  );
}
