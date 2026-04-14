import React from 'react';
import { Card, CardHeader } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';

const DataLineage: React.FC = () => {
  const nodes = [
    { name: "ESP32 Gateways", type: "Data Source", icon: "memory", status: "Streaming" },
    { name: "InfluxDB", type: "Time-Series Store", icon: "database", status: "Indexed" },
    { name: "Feature Store", type: "Engineering", icon: "hub", status: "Computing" },
    { name: "ML Inference", type: "Neural Engine", icon: "psychology", status: "Predicting", active: true },
    { name: "Dashboard", type: "Visualization", icon: "monitoring", status: "Rendering" }
  ];

  const stages = [
    { name: "ESP32 Acquisition", sub: "BLE & WiFi Meshing", status: "Streaming", val: "99.98% Success", time: "12:04:59:001", icon: "sensors" },
    { name: "InfluxDB Hot Tier", sub: "Bucketed Time Series", status: "Indexed", val: "Verified Sum", time: "12:04:59:004", icon: "storage" },
    { name: "ML Inference Engine", sub: "ResNet Clinical Core", status: "Predicting", val: "μ: 0.94 Precision", time: "12:04:59:122", icon: "model_training" }
  ];

  return (
    <div className="space-y-16">
      <header className="flex flex-col gap-4">
        <span className="text-primary font-bold tracking-[0.2em] text-[10px] uppercase">System Architecture</span>
        <h1 className="font-headline text-5xl font-extrabold text-on-background leading-tight">Data Lineage</h1>
        <p className="text-on-surface-variant max-w-2xl text-lg font-medium">
          An end-to-end trace of clinical data packets from edge acquisition to real-time inference visualization.
        </p>
      </header>

      <section className="bg-surface-container-low rounded-2xl p-8 md:p-16 relative overflow-hidden">
        <div className="absolute inset-0 opacity-[0.05] pointer-events-none" style={{ backgroundImage: "radial-gradient(#003d9b 1px, transparent 1px)", backgroundSize: "24px 24px" }}></div>
        
        <div className="relative flex flex-col lg:flex-row justify-between items-center gap-8 min-h-[300px]">
          {nodes.map((node, i) => (
            <React.Fragment key={i}>
              <div className="flex flex-col items-center group z-10 w-40">
                <div className={`w-28 h-28 rounded-full flex items-center justify-center shadow-xl transition-all duration-500 group-hover:scale-110 ${node.active ? 'bg-primary text-white shadow-primary/30' : 'bg-surface-container-lowest text-primary'}`}>
                  <span className="material-symbols-outlined text-4xl" style={{ fontVariationSettings: "'FILL' 0, 'wght' 200" }}>{node.icon}</span>
                </div>
                <div className="mt-6 text-center space-y-1">
                  <h3 className="font-headline font-extrabold text-on-surface tracking-tight">{node.name}</h3>
                  <span className="text-[10px] text-primary font-bold tracking-widest uppercase block opacity-70">{node.type}</span>
                </div>
              </div>
              {i < nodes.length - 1 && (
                <div className="hidden lg:block flex-grow h-[1px] bg-outline-variant/30 relative overflow-hidden mx-4">
                  <div className="absolute inset-0 bg-primary/40 animate-[slide_2s_linear_infinite]" style={{ width: '20%' }}></div>
                </div>
              )}
            </React.Fragment>
          ))}
        </div>
      </section>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {[
          { label: "Data Throughput", value: "1.2", unit: "GB/sec", icon: "speed", status: "LIVE" },
          { label: "End-to-End Latency", value: "142", unit: "ms", icon: "timer", status: "OPTIMAL" },
          { label: "Active Gateways", value: "48", unit: "Units", icon: "settings_input_antenna", status: "NODES OK" }
        ].map((stat, i) => (
          <Card key={i} className="p-8 flex flex-col gap-6 group hover:border-primary/30 transition-all">
            <div className="flex justify-between items-start">
              <span className="material-symbols-outlined text-primary p-3 bg-primary-fixed rounded-xl group-hover:bg-primary group-hover:text-white transition-colors" style={{ fontVariationSettings: "'FILL' 1" }}>{stat.icon}</span>
              <Badge variant="primary">{stat.status}</Badge>
            </div>
            <div>
              <h4 className="text-on-surface-variant font-bold text-[10px] uppercase tracking-widest mb-1">{stat.label}</h4>
              <div className="flex items-baseline gap-2">
                <span className="font-headline text-4xl font-extrabold text-on-background tracking-tighter">{stat.value}</span>
                <span className="text-on-surface-variant font-bold text-xs uppercase opacity-60">{stat.unit}</span>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <Card className="overflow-hidden border-none shadow-2xl">
        <CardHeader className="bg-surface-container-low/30 flex justify-between items-center py-6 px-8">
          <h2 className="font-headline font-extrabold text-xl text-on-background tracking-tight">Stage Details & Transformations</h2>
          <button className="text-primary font-bold text-xs uppercase tracking-widest flex items-center gap-2 hover:opacity-80 transition-all">
            View Detailed Logs <span className="material-symbols-outlined text-sm">arrow_forward</span>
          </button>
        </CardHeader>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-surface-container-low/50 text-[10px] font-bold text-outline tracking-[0.2em] uppercase">
                <th className="px-8 py-5">Stage Name</th>
                <th className="px-8 py-5 text-center">Status</th>
                <th className="px-8 py-5">Validation</th>
                <th className="px-8 py-5 text-right">Last Activity</th>
              </tr>
            </thead>
            <tbody className="text-sm font-medium">
              {stages.map((stage, i) => (
                <tr key={i} className="border-b border-outline-variant/5 hover:bg-surface-container-low/20 transition-colors">
                  <td className="px-8 py-6">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-white transition-all">
                        <span className="material-symbols-outlined">{stage.icon}</span>
                      </div>
                      <div>
                        <p className="font-extrabold text-on-surface leading-tight">{stage.name}</p>
                        <p className="text-[10px] text-outline uppercase tracking-wider mt-0.5">{stage.sub}</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-8 py-6 text-center">
                    <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-green-50 text-green-700 text-[10px] font-bold uppercase tracking-wider ring-1 ring-green-500/20">
                      <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span>
                      {stage.status}
                    </span>
                  </td>
                  <td className="px-8 py-6 text-on-surface-variant font-bold tracking-tight">{stage.val}</td>
                  <td className="px-8 py-6 text-right text-outline font-mono text-[11px] tabular-nums">{stage.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
      
      <style>{`
        @keyframes slide {
          from { transform: translateX(-100%); }
          to { transform: translateX(500%); }
        }
      `}</style>
    </div>
  );
};

export default DataLineage;
