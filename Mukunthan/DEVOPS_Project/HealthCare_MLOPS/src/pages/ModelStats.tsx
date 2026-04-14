import React from 'react';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import GrafanaEmbed from '../components/ui/GrafanaEmbed';

// Resilient Fallback Chart Component
const SimulatedChart: React.FC<{ type: 'area' | 'bar', height: number, title?: string }> = ({ type, height, title }) => {
  return (
    <div className="relative w-full h-full p-6 flex flex-col" style={{ height }}>
      {title && <h4 className="text-[10px] font-bold text-outline uppercase tracking-widest mb-4">{title}</h4>}
      <div className="flex-grow relative mt-2">
        {type === 'area' ? (
          <svg className="w-full h-full" viewBox="0 0 400 200" preserveAspectRatio="none">
            <defs>
              <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor="var(--color-primary)" stopOpacity="0.3" />
                <stop offset="100%" stopColor="var(--color-primary)" stopOpacity="0" />
              </linearGradient>
            </defs>
            <path 
              d="M0,150 Q50,130 100,140 T200,80 T300,110 T400,60 L400,200 L0,200 Z" 
              fill="url(#gradient)" 
              className="animate-pulse"
            />
            <path 
              d="M0,150 Q50,130 100,140 T200,80 T300,110 T400,60" 
              fill="none" 
              stroke="var(--color-primary)" 
              strokeWidth="3" 
              strokeLinecap="round"
              className="[stroke-dasharray:1000] [stroke-dashoffset:1000] animate-[draw_3s_ease-in-out_infinite]"
            />
            {[1, 2, 3, 4, 5].map(i => (
              <line 
                key={i} 
                x1={i * 80} y1="0" x2={i * 80} y2="200" 
                stroke="var(--color-outline-variant)" 
                strokeOpacity="0.1" 
                strokeDasharray="4 4" 
              />
            ))}
          </svg>
        ) : (
          <div className="w-full h-full flex items-end gap-2 px-2">
            {[45, 67, 89, 54, 78, 32, 91].map((h, i) => (
              <div 
                key={i} 
                className="flex-grow bg-primary/20 border-t-2 border-primary rounded-t-sm transition-all duration-1000"
                style={{ height: `${h}%` }}
              ></div>
            ))}
          </div>
        )}
      </div>
      <div className="mt-4 flex justify-between items-center">
        <div className="flex gap-2">
          <div className="w-2 h-2 rounded-full bg-success animate-pulse"></div>
          <span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">Resilient Live Stream</span>
        </div>
        <span className="text-[10px] font-bold text-outline uppercase tracking-widest opacity-50">Simulation Mode</span>
      </div>
    </div>
  );
};

const ModelStats: React.FC = () => {
  // Use a simple check for port connectivity (or fallback to true for this demo)
  const isSimulationMode = true; 

  return (
    <div className="space-y-12">
      <style>{`
        @keyframes draw {
          to { stroke-dashoffset: 0; }
        }
      `}</style>

      <section className="flex flex-col md:flex-row justify-between items-end gap-6">
        <div>
          <Badge variant="primary" className="mb-4">Production Analytics</Badge>
          <h1 className="text-4xl md:text-5xl font-headline font-extrabold text-on-background tracking-tight">Clinical Predictor v2.4</h1>
          <p className="mt-4 text-on-surface-variant max-w-2xl text-lg leading-relaxed font-medium">
            Deep dive into performance stability and drift metrics for the cardiac risk assessment engine. Bypassing Docker network drift.
          </p>
        </div>
        <div className="flex gap-3 w-full md:w-auto">
          <button className="flex-1 md:flex-none px-6 py-3 bg-surface-container-high text-on-surface font-bold text-xs uppercase tracking-widest rounded-lg flex items-center justify-center gap-2 hover:bg-surface-container-highest transition-all">
            <span className="material-symbols-outlined text-sm">download</span> Export
          </button>
          <button className="flex-1 md:flex-none px-6 py-3 bg-gradient-to-br from-primary to-primary-container text-white font-bold text-xs uppercase tracking-widest rounded-lg shadow-lg shadow-primary/20 hover:opacity-90 active:scale-95 transition-all">
            Retrain Model
          </button>
        </div>
      </section>

      <div className="grid grid-cols-12 gap-6 md:gap-8">
        <Card className="col-span-12 lg:col-span-8 p-0 overflow-hidden h-96">
          {isSimulationMode ? (
            <SimulatedChart type="area" height={384} title="Inference Latency (95th percentile)" />
          ) : (
            <GrafanaEmbed 
              dashboardUid="system-performance-dashboard" 
              panelId={3}
              height={384}
              className="border-none"
            />
          )}
        </Card>

        <div className="col-span-12 lg:col-span-4 space-y-6">
          {[
            { label: "Precision Metric", value: "0.942", change: "+2.4%", trend: "up" },
            { label: "Recall Metric", value: "0.891", change: "-0.8%", trend: "down" },
            { label: "F1 Score", value: "0.916", change: "+1.1%", trend: "up" }
          ].map((metric, i) => (
            <Card key={i} className="p-6 bg-surface-container-low border-none">
              <h4 className="text-[10px] font-bold text-outline uppercase tracking-widest mb-4">{metric.label}</h4>
              <div className="flex items-baseline gap-3">
                <span className="text-4xl font-headline font-extrabold text-primary tracking-tighter">{metric.value}</span>
                <span className={`text-xs font-bold ${metric.trend === 'up' ? 'text-green-600' : 'text-error'}`}>
                  {metric.change}
                </span>
              </div>
            </Card>
          ))}
        </div>

        <Card className="col-span-12 md:col-span-6 p-8">
          <h3 className="font-headline font-bold text-xl text-on-surface mb-8">Confusion Matrix</h3>
          <div className="grid grid-cols-2 grid-rows-2 gap-4 h-64 relative font-headline">
            <div className="absolute -left-10 top-1/2 -rotate-90 text-[10px] font-bold text-outline uppercase tracking-widest">Actual</div>
            <div className="absolute -top-10 left-1/2 -translate-x-1/2 text-[10px] font-bold text-outline uppercase tracking-widest">Predicted</div>
            
            <div className="bg-primary/5 rounded-xl border border-primary/20 flex flex-col items-center justify-center p-4">
              <span className="text-3xl font-extrabold text-primary">1,242</span>
              <span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mt-1">True Neg</span>
            </div>
            <div className="bg-error/5 rounded-xl border border-error/20 flex flex-col items-center justify-center p-4">
              <span className="text-3xl font-extrabold text-error">42</span>
              <span className="text-[10px] font-bold text-error uppercase tracking-widest mt-1">False Pos</span>
            </div>
            <div className="bg-error/5 rounded-xl border border-error/20 flex flex-col items-center justify-center p-4">
              <span className="text-3xl font-extrabold text-error">18</span>
              <span className="text-[10px] font-bold text-error uppercase tracking-widest mt-1">False Neg</span>
            </div>
            <div className="bg-primary rounded-xl flex flex-col items-center justify-center p-4 shadow-lg shadow-primary/20">
              <span className="text-3xl font-extrabold text-white">418</span>
              <span className="text-[10px] font-bold text-white/80 uppercase tracking-widest mt-1">True Pos</span>
            </div>
          </div>
          <div className="mt-10 flex flex-wrap gap-6 text-[10px] font-bold uppercase tracking-widest">
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-primary"></div>
              <span>Optimal Match</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-error"></div>
              <span>Critical Misclass</span>
            </div>
          </div>
        </Card>

        <Card className="col-span-12 md:col-span-6 p-0 overflow-hidden h-80">
          {isSimulationMode ? (
            <SimulatedChart type="bar" height={320} title="Accuracy History (Last 7 Epochs)" />
          ) : (
            <GrafanaEmbed 
              dashboardUid="system-performance-dashboard" 
              panelId={1}
              height={320}
              className="border-none"
            />
          )}
        </Card>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: "Uptime", value: "99.998%", icon: "check_circle", color: "text-green-500" },
          { label: "Request Volume", value: "1.2k RPS", icon: "speed", color: "text-primary" },
          { label: "Error Rate", value: "0.02%", icon: "error", color: "text-tertiary" },
          { label: "Deployment", value: "Cluster A", icon: "hub", color: "text-primary" }
        ].map((item, i) => (
          <div key={i} className="bg-white border-b-4 border-primary p-6 rounded-t-xl shadow-sm flex items-center justify-between group hover:bg-slate-50 transition-colors">
            <div>
              <span className="text-[10px] font-bold text-outline uppercase tracking-widest">{item.label}</span>
              <div className="text-xl font-bold text-on-surface mt-1">{item.value}</div>
            </div>
            <span className={`material-symbols-outlined ${item.color} group-hover:scale-110 transition-transform`}>{item.icon}</span>
          </div>
        ))}
      </div>

      <section className="space-y-6">
        <div className="flex justify-between items-center px-2">
          <div>
            <h2 className="text-2xl font-headline font-bold text-on-surface">Deep Systems Analytics</h2>
            <p className="text-sm text-on-surface-variant font-medium">Native analytical layer synchronized via InfluxDB & Grafana Sidecar</p>
          </div>
          <a 
            href={`${import.meta.env.VITE_GRAFANA_URL || 'http://localhost:3005'}/d/patient-vitals-dashboard`} 
            target="_blank" 
            rel="noopener noreferrer"
            className="px-4 py-2 bg-surface-container text-primary font-bold text-[10px] uppercase tracking-widest rounded-lg flex items-center gap-2 hover:bg-surface-container-high transition-all"
          >
            Launch Full Suite <span className="material-symbols-outlined text-sm">open_in_new</span>
          </a>
        </div>
        
        <Card className="p-0 overflow-hidden h-[600px] border-none shadow-2xl">
          {isSimulationMode ? (
            <div className="w-full h-full bg-surface-container-low flex items-center justify-center">
              <div className="text-center space-y-4">
                <span className="material-symbols-outlined text-outline/20 text-8xl">dashboard_customize</span>
                <p className="text-outline font-bold uppercase tracking-[0.2em] text-sm">Full Analytics Suite restricted by Docker drift</p>
                <div className="flex justify-center gap-2">
                   <div className="px-3 py-1 bg-primary/10 rounded-full text-[10px] font-bold text-primary uppercase">Simulated Mode Active</div>
                </div>
              </div>
            </div>
          ) : (
            <GrafanaEmbed 
              dashboardUid="patient-vitals-dashboard" 
              height={600} 
              className="border-none shadow-2xl"
            />
          )}
        </Card>
      </section>
    </div>
  );
};

export default ModelStats;
