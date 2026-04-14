import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="w-full bg-white dark:bg-slate-900 sticky top-0 z-50 border-b border-surface-container/50">
      <div className="flex justify-between items-center px-6 md:px-12 h-20 w-full max-w-screen-2xl mx-auto font-headline antialiased">
        <div className="flex items-center gap-3">
          <span className="material-symbols-outlined text-primary text-2xl" style={{ fontVariationSettings: "'FILL' 1" }}>
            clinical_notes
          </span>
          <div className="text-2xl font-bold tracking-tight text-blue-900 dark:text-white">
            Clinical Curator <span className="font-normal opacity-50">MLOps</span>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="relative hidden md:block">
            <span className="absolute inset-y-0 left-3 flex items-center text-slate-400">
              <span className="material-symbols-outlined text-sm">search</span>
            </span>
            <input 
              className="pl-10 pr-4 py-2 bg-slate-50 dark:bg-slate-800 border-none rounded-full text-sm focus:ring-2 focus:ring-primary w-64 transition-all" 
              placeholder="Search patients or models..." 
              type="text"
            />
          </div>
          <button className="p-2 text-slate-500 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all rounded-full outline-none">
            <span className="material-symbols-outlined">settings</span>
          </button>
          <div className="w-10 h-10 rounded-full overflow-hidden border-2 border-primary-container cursor-pointer hover:opacity-80 transition-opacity">
            <img 
              alt="Doctor Profile" 
              className="w-full h-full object-cover" 
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuCFtIfzfm729pqQ-etZC2BehDxruOdlN5ZlPcRq0sWwesY6ddt2sdw52-ZTL8ZC8BqxaRxYdY3IYZmsB6PQWWmynEhEuoin7vFuXbr8wxiqdqroq8SgtBcbOrfUUtkKypF8ZGWDo1P_tKq8WPWDgEHNTNXYgLs-aBQm-Q1Kl_mqWQQkXtDflHxArGOdB5pkkPBif3ZwuAxw5-SB59GsdYyVbWFtAL_el1ahIc4-nOrtDZW6YesF6A4FRtbU9ROimArsIk6eX7WMa_E"
            />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
