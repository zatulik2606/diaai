import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";

import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin", "cyrillic"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin", "cyrillic"],
});

export const metadata: Metadata = {
  title: "diaai",
  description: "Сопровождение пациентов с диабетом",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="ru"
      className={`dark ${inter.variable} ${jetbrainsMono.variable} h-full`}
    >
      <body className="min-h-full">{children}</body>
    </html>
  );
}
