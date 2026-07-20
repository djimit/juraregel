import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", label: "Dashboard", icon: "📊" },
  { href: "/compliance", label: "Compliance Score", icon: "⚖️" },
  { href: "/agents", label: "AI Agents", icon: "🤖" },
  { href: "/policies", label: "Policies", icon: "📋" },
  { href: "/templates", label: "Templates", icon: "📄" },
  { href: "/architecture", label: "Architectuur", icon: "🏗️" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-[#1a365d] text-white p-6 overflow-y-auto">
      <div className="mb-8">
        <h1 className="text-xl font-bold">🏛️ JuraRegel</h1>
        <p className="text-sm text-blue-200 mt-1">Living Compliance Engine</p>
      </div>
      <nav className="space-y-1">
        {navItems.map((item) => {
          const active = pathname === item.href;
          return (
            <Link key={item.href} href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${active ? "bg-blue-600 text-white" : "text-blue-100 hover:bg-blue-800"}`}>
              <span>{item.icon}</span>
              <span className="font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
