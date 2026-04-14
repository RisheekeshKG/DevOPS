import React from 'react';

interface GrafanaEmbedProps {
  dashboardUid?: string;
  panelId?: number | string;
  variables?: Record<string, string>;
  width?: string | number;
  height?: string | number;
  className?: string;
  theme?: 'light' | 'dark';
  refresh?: string;
  kiosk?: boolean;
}

const GrafanaEmbed: React.FC<GrafanaEmbedProps> = ({
  dashboardUid = 'patient-vitals-dashboard',
  panelId,
  variables = {},
  width = "100%",
  height = 300,
  className = "",
  theme = 'dark',
  refresh = '5s',
  kiosk = true,
}) => {
  const baseUrl = import.meta.env.VITE_GRAFANA_URL || 'http://localhost:3005';
  
  // Choose endpoint: /d/ for full dashboard, /d-solo/ for individual panels
  const endpoint = panelId ? 'd-solo' : 'd';
  
  const url = new URL(`${baseUrl}/${endpoint}/${dashboardUid}`);
  
  // Add base params
  url.searchParams.append('orgId', '1');
  url.searchParams.append('theme', theme);
  url.searchParams.append('refresh', refresh);
  
  if (kiosk) {
    url.searchParams.append('kiosk', '1');
  }
  
  if (panelId) {
    url.searchParams.append('panelId', panelId.toString());
  }
  
  // Add user-defined variables
  Object.entries(variables).forEach(([key, value]) => {
    url.searchParams.append(`var-${key}`, value);
  });

  return (
    <div className={`relative overflow-hidden rounded-xl bg-surface-container-low ${className}`} style={{ height }}>
      <div className="absolute inset-0 flex items-center justify-center -z-10 bg-surface-container-low">
        <div className="flex flex-col items-center gap-2 text-outline/30 animate-pulse">
          <span className="material-symbols-outlined text-4xl">analytics</span>
          <span className="text-[10px] font-bold uppercase tracking-widest">Loading Analytics...</span>
        </div>
      </div>
      <iframe
        src={url.toString()}
        width={width}
        height={height}
        frameBorder="0"
        title="Grafana Analytics"
        className="relative z-10 w-full h-full opacity-0 transition-opacity duration-700"
        onLoad={(e) => (e.currentTarget.style.opacity = '1')}
      ></iframe>
    </div>
  );
};

export default GrafanaEmbed;
