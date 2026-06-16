import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

import { defaultPathForRole } from "@/lib/types/auth";
import { parseSessionCookie, SESSION_COOKIE } from "@/lib/session";

const PUBLIC_PATHS = ["/login"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const session = parseSessionCookie(
    request.cookies.get(SESSION_COOKIE)?.value,
  );

  if (pathname.startsWith("/api/auth")) {
    return NextResponse.next();
  }

  const isPublic = PUBLIC_PATHS.some(
    (path) => pathname === path || pathname.startsWith(`${path}/`),
  );

  if (!session && !isPublic) {
    const loginUrl = request.nextUrl.clone();
    loginUrl.pathname = "/login";
    return NextResponse.redirect(loginUrl);
  }

  if (session && pathname === "/login") {
    const target = request.nextUrl.clone();
    target.pathname = defaultPathForRole(session.role);
    return NextResponse.redirect(target);
  }

  if (session?.role === "doctor" && pathname.startsWith("/dashboard")) {
    const target = request.nextUrl.clone();
    target.pathname = "/leaderboard";
    return NextResponse.redirect(target);
  }

  if (pathname === "/") {
    const target = request.nextUrl.clone();
    target.pathname = session
      ? defaultPathForRole(session.role)
      : "/login";
    return NextResponse.redirect(target);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
