import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { LogoutButton } from "@/components/logout-button";
import type { SessionUser } from "@/lib/types/auth";

function initials(name: string | null): string {
  if (!name) {
    return "?";
  }
  return name
    .split(/\s+/)
    .map((part) => part[0]?.toUpperCase() ?? "")
    .join("")
    .slice(0, 2);
}

export function AppHeader({ user }: { user: SessionUser }) {
  return (
    <header className="flex h-14 items-center justify-between border-b border-border bg-card px-6">
      <div className="font-semibold tracking-tight">diaai</div>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2">
          <Avatar>
            <AvatarFallback>{initials(user.display_name)}</AvatarFallback>
          </Avatar>
          <div className="hidden text-sm sm:block">
            <div className="font-medium">{user.display_name ?? user.user_id}</div>
            <div className="text-xs text-muted-foreground">{user.role}</div>
          </div>
        </div>
        <LogoutButton />
      </div>
    </header>
  );
}
