"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, MessageSquare, Trophy } from "lucide-react";

import { cn } from "@/lib/utils";

type NavItem = {
  href: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  roles: Array<"doctor" | "diabetic">;
};

const NAV_ITEMS: NavItem[] = [
  {
    href: "/dashboard",
    label: "Dashboard",
    icon: LayoutDashboard,
    roles: ["diabetic"],
  },
  {
    href: "/leaderboard",
    label: "Leaderboard",
    icon: Trophy,
    roles: ["doctor"],
  },
  {
    href: "/chat",
    label: "Chat",
    icon: MessageSquare,
    roles: ["doctor", "diabetic"],
  },
];

export function AppSidebar({ role }: { role: string }) {
  const pathname = usePathname();
  const items = NAV_ITEMS.filter((item) =>
    item.roles.includes(role as "doctor" | "diabetic"),
  );

  return (
    <aside className="hidden w-60 shrink-0 border-r border-border bg-card md:flex md:flex-col">
      <nav className="flex flex-col gap-1 p-4">
        {items.map((item) => {
          const active = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors",
                active
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
              )}
            >
              <Icon className="size-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
