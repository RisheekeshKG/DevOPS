import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-slate-200/20 bg-slate-50 dark:bg-slate-950 mt-auto py-6">
      <div className="flex flex-col md:flex-row justify-between items-center px-6 md:px-12 w-full max-w-screen-2xl mx-auto gap-4">
        <div className="flex items-center gap-3">
          <span className="flex h-2 w-2 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
          </span>
          <div className="text-slate-500 dark:text-slate-400 font-inter text-xs tracking-wide uppercase">
            System Health: <span className="text-primary font-bold">ESP32 Operational</span> | <span className="text-primary font-bold">InfluxDB Connected</span>
          </div>
        </div>
        
        <div className="flex gap-8 text-xs font-medium text-slate-400 dark:text-slate-500">
          <a className="hover:text-blue-500 transition-colors" href="#">Status Page</a>
          <a className="hover:text-blue-500 transition-colors" href="#">API Docs</a>
          <a className="hover:text-blue-500 transition-colors" href="#">Emergency Support</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
