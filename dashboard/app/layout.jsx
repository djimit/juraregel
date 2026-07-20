import "./globals.css";
import Sidebar from "../components/Sidebar.jsx";

export const metadata = {
  title: "JuraRegel Dashboard — Living Compliance Engine",
  description: "Real-time compliance monitoring, AI-gestuurde analyse, en policy evaluatie",
};

export default function RootLayout({ children }) {
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
