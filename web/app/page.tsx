import { redirect } from "next/navigation";

import { defaultPathForRole } from "@/lib/types/auth";
import { getSession } from "@/lib/session";

export default async function HomePage() {
  const session = await getSession();
  redirect(session ? defaultPathForRole(session.role) : "/login");
}
