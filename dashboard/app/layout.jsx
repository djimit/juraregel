import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "../components/Sidebar";

export const metadata: Metadata = {
  title: "JuraRegel Dashboard — Living Compliance Engine",
  description: "Real-time compliance monitoring, AI-gestuurde analyse, en policy evaluatie",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="nl">
      <body className="bg-gray-50 min-h-screen">
        <div className="flex">
          <Sidebar />
          <main className="flex-1 p-8 ml-64">{children}</main>
        </div>
      </body>
    </html>
  );
}
