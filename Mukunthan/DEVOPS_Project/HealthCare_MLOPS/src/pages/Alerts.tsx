import React from 'react';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';

const Alerts: React.FC = () => {
  const alerts = [
    { id: "AL-102", type: "Clinical", title: "Tachycardia Alert", patient: "James Chen", bed: "205", severity: "High", time: "2 mins ago", status: "Active", icon: "emergency_home" },
    { id: "AL-101", type: "System", title: "Latency Spike P99", patient: "Cluster Wide", bed: "N/A", severity: "Medium", time: "18 mins ago", status: "Resolved", icon: "timer_off" },
    { id: "AL-100", type: "Clinical", title: "SpO2 Baseline Shift", patient: "Elena Rodriguez", bed: "202", severity: "Low", time: "1 hour ago", status: "Acknowledged", icon: "query_stats" },
    { id: "AL-099", type: "System", title: "Node DB-04 Re-sync", patient: "Storage", bed: "N/A", severity: "Low", time: "3 hours ago", status: "Resolved", icon: "published_with_changes" },
    { id: "AL-098", type: "Clinical", title: "Arrhythmia Suspected", patient: "Sarah Miller", bed: "210", severity: "Medium", time: "5 hours ago", status: "Pending", icon: "heart_broken" }
  ];

  return (
    <div className="space-y-12">
      <header className="flex flex-col gap-4">
        <div className="flex items-center gap-3">
          <Badge variant="error" className="animate-pulse">Live Traffic</Badge>
          <span className="text-on-surface-variant font-bold text-[10px] uppercase tracking-widest">Active Surveillance</span>
        </div>
        <h1 className="font-headline text-5xl font-extrabold text-on-background tracking-tight">Alert Intelligence</h1>
        <p className="text-on-surface-variant max-w-2xl text-lg font-medium">
          Automated clinical alerts and system telemetry anomalies filtered by CV-ResNet classification.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { label: "Active Alerts", value: "02", color: "text-error", sub: "Priority 1" },
          { label: "Mean Time to Ack", value: "4.2", unit: "min", color: "text-primary", sub: "Operational" },
          { label: "System Health", value: "98.4", unit: "%", color: "text-green-600", sub: "Confident" }
        ].map((stat, i) => (
          <Card key={i} className="p-8 border-none bg-surface-container-low shadow-sm hover:shadow-md transition-shadow">
            <h4 className="text-[10px] font-bold text-outline uppercase tracking-[0.2em] mb-2">{stat.label}</h4>
            <div className="flex items-baseline gap-2">
              <span className={`font-headline text-5xl font-extrabold tracking-tighter ${stat.color}`}>{stat.value}</span>
              {stat.unit && <span className="text-xs font-bold text-on-surface-variant uppercase opacity-60 tabular-nums">{stat.unit}</span>}
            </div>
            <p className="text-[10px] font-bold text-outline uppercase tracking-widest mt-4 flex items-center gap-1.5 opacity-60">
              <span className={`w-1.5 h-1.5 rounded-full ${stat.color.replace('text-', 'bg-')}`}></span>
              {stat.sub}
            </p>
          </Card>
        ))}
      </div>

      <Card className="border-none shadow-2xl overflow-hidden">
        <div className="px-8 py-6 bg-surface-container-low/30 border-b border-outline-variant/10 flex justify-between items-center">
          <div className="flex gap-4">
            <button className="px-4 py-2 bg-on-background text-white text-[10px] font-bold uppercase tracking-widest rounded-lg transition-transform active:scale-95 shadow-lg">Newest First</button>
            <button className="px-4 py-2 bg-transparent text-on-surface-variant text-[10px] font-bold uppercase tracking-widest rounded-lg hover:bg-slate-100 transition-all">Filter By Type</button>
          </div>
          <div className="relative group">
            <input 
              type="text" 
              placeholder="Search alert history..." 
              className="pl-4 pr-10 py-2 border border-outline-variant/30 rounded-lg text-xs font-medium focus:ring-1 focus:ring-primary outline-none w-64 bg-transparent group-hover:bg-white transition-colors"
            />
            <span className="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-outline text-sm" style={{ fontVariationSettings: "'OPSZ' 18" }}>search</span>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-surface-container-low/50 text-[10px] font-bold text-outline tracking-[0.2em] uppercase">
                <th className="px-8 py-5">Event ID</th>
                <th className="px-8 py-5">Clinical Event</th>
                <th className="px-8 py-5">Context</th>
                <th className="px-8 py-5 text-center">Severity</th>
                <th className="px-8 py-5 text-right">Activity</th>
              </tr>
            </thead>
            <tbody className="text-sm font-medium">
              {alerts.map((alert) => (
                <tr key={alert.id} className="border-b border-outline-variant/5 group hover:bg-surface-container-low/10 transition-colors">
                  <td className="px-8 py-6">
                    <span className="text-[11px] font-mono font-bold text-outline bg-slate-50 px-2 py-1 rounded ring-1 ring-slate-200">{alert.id}</span>
                  </td>
                  <td className="px-8 py-6">
                    <div className="flex items-center gap-4">
                      <div className={`w-10 h-10 rounded-lg flex items-center justify-center transition-all ${alert.severity === 'High' ? 'bg-error-container text-error' : 'bg-primary-fixed text-primary'}`}>
                        <span className="material-symbols-outlined">{alert.icon}</span>
                      </div>
                      <div>
                        <p className="font-extrabold text-on-surface leading-tight">{alert.title}</p>
                        <p className="text-[10px] text-outline uppercase tracking-wider mt-0.5">{alert.type} Alert</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-8 py-6">
                    <div>
                      <p className="font-bold text-on-surface-variant">{alert.patient}</p>
                      <p className="text-[10px] text-outline uppercase font-mono">{alert.bed !== 'N/A' ? `Bed ${alert.bed}` : 'Global System'}</p>
                    </div>
                  </td>
                  <td className="px-8 py-6 text-center">
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest ring-1 ${
                      alert.severity === 'High' ? 'bg-error-container text-error ring-error/20' : 
                      alert.severity === 'Medium' ? 'bg-amber-50 text-amber-600 ring-amber-500/20' : 
                      'bg-slate-50 text-slate-500 ring-slate-500/10'
                    }`}>
                      {alert.severity}
                    </span>
                  </td>
                  <td className="px-8 py-6 text-right">
                    <div>
                      <p className="font-bold text-on-surface tabular-nums">{alert.status}</p>
                      <p className="text-[10px] text-outline uppercase tracking-wider font-mono mt-0.5">{alert.time}</p>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
      
      <div className="flex justify-center gap-1">
        {[1, 2, 3, 4, 5].map(i => (
          <button key={i} className={`w-8 h-8 rounded-lg flex items-center justify-center text-[10px] font-bold transition-all ${i === 1 ? 'bg-primary text-white' : 'hover:bg-slate-100 text-on-surface-variant'}`}>
            {i}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Alerts;
