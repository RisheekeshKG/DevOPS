import React from 'react';
import { NavLink } from 'react-router-dom';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const Navbar: React.FC = () => {
  const navItems = [
    { label: 'Monitoring', icon: 'monitor_heart', path: '/' },
    { label: 'Model Stats', icon: 'analytics', path: '/stats' },
    { label: 'Data', icon: 'database', path: '/data' },
    { label: 'Alerts', icon: 'notifications_active', path: '/alerts', badge: true },
  ];

  return (
    <nav className="bg-white dark:bg-slate-950 border-b border-surface-container/50 sticky top-20 z-40">
      <div className="max-w-screen-2xl mx-auto px-6 md:px-12 flex items-center overflow-x-auto no-scrollbar">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-2 px-6 py-4 border-b-2 transition-all group relative whitespace-nowrap",
                isActive
                  ? "border-primary text-primary font-semibold"
                  : "border-transparent text-slate-500 hover:text-blue-600"
              )
            }
          >
            <span className="material-symbols-outlined text-[20px] group-hover:scale-110 transition-transform">
              {item.icon}
            </span>
            <span className="font-headline text-sm uppercase tracking-wider">{item.label}</span>
            {item.badge && (
              <span className="absolute top-4 right-3 w-1.5 h-1.5 bg-error rounded-full animate-pulse"></span>
            )}
          </NavLink>
        ))}
      </div>
    </nav>
  );
};

export default Navbar;
