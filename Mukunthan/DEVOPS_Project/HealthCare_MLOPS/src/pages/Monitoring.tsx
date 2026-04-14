import React, { useMemo, useState } from 'react';
import { Card, CardHeader, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { StatItem } from '../components/ui/StatItem';
import ECGWaveform from '../components/ui/ECGWaveform';
import { AuroraBackground } from '../components/ui/aurora-background';
import { useVitals } from '../hooks/useVitals';
import GrafanaEmbed from '../components/ui/GrafanaEmbed';

interface Vital {
  label: string;
  value: number | string;
  unit: string;
  variant?: 'default' | 'error' | 'success';
}

const Monitoring: React.FC = () => {
  const { vitals, isConnected } = useVitals();
  const [activeTrends, setActiveTrends] = useState<Record<string, boolean>>({});

  const toggleTrend = (id: string) => {
    setActiveTrends(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const patientProfiles = useMemo(() => ({
    "P001": {
      name: "Elena Rodriguez",
      image: "https://lh3.googleusercontent.com/aida-public/AB6AXuCIGharmxtesLz5aDgBGzu2z9RX0T1F_FOiU6FmgWo6nTV7hVoDxZgrlEQljJacv-0iflofF12ld3UvqHJ-XSylsgt6hIjL83p8BOH7-_uCnphQk3bSfSoeQzty5KZgBqVTgVIwgr1NobVBv2NIG3GGv7Dsb2Pn0UsEezlKoYL3ihac2GCoQ_S7INhi62NfSXQWf6YtvQ0FQUziDCegX_2WvSA_J9dQoYvrUEuy3qhqK_nlx0yE6q5_bY_M88BoNGF8OahjhUab-og",
      ward: "Ward 4A",
      bed: "202",
    },
    "P002": {
      name: "James Chen",
      image: "https://lh3.googleusercontent.com/aida-public/AB6AXuCg-zTxl7QNTHf20nym66zgnfhPYb2636ZyjjLQl5s85FTCHSVowr9KzlLBOp6pKDf0W6NCodCwY-tLsX1M0Kskd1UOLyv1XjH7xPsAOBmwmKHGhL1Fk0GbNe49WIVflxSWWaFzNRK8Jm8lRX-vsG1g7lSz1Kz8rBtbRfvDibBZ6DhE8Tye0gJXZSdwAZkLI7NMIj6GFUrQMef2PKfAWNwTnT7hCGEsQRjYMnqqDpZ3b3bwbZbE0SfqpMgSl_zAq9Dg0rDYYUiXOKk",
      ward: "Ward 4A",
      bed: "205",
    },
    "P003": {
      name: "Sarah Miller",
      image: "https://lh3.googleusercontent.com/aida-public/AB6AXuA_tjCvqXfJndGk_NAzpPTSHsTkKzAFqs7cIo49r1hdE0zfyW-DQapaOjXEjtRQBpOzu64e138-vXZC2g7RLdM6N7olP3yn_g512K-j0VNPCr5nPOgHopUx8Xx9XQhjVXmOtNgi50EveCcRGVvSkrkYghaY6F8AiPdFPYYeACGgIlqkVt1ZroTWyZa--VxUlJA2j_qOg1RC04ndLp9Ri0-3ZUR_FM3Y1MP1Y18rb6R1iJVtk8cu10kCkxnfasg9QjXXhwSc8cUngF4",
      ward: "Ward 4A",
      bed: "210",
    }
  }), []);

  const patientIds = ["P001", "P002", "P003"];

  return (
    <AuroraBackground className="bg-transparent dark:bg-transparent h-auto py-0">
      <div className="flex flex-col lg:flex-row gap-8 items-start w-full relative z-10">
        <div className="flex-grow space-y-8 w-full">
          <header className="mb-8 flex justify-between items-end">
            <div>
              <h1 className="font-headline text-4xl font-extrabold tracking-tight mb-2 text-on-surface">Active Monitoring</h1>
              <p className="text-on-surface-variant font-medium text-lg">Real-time physiological data synthesized via MLOps Pipeline.</p>
            </div>
            <div className="flex items-center gap-2 px-4 py-2 rounded-full border border-outline-variant/30 bg-surface-container-low mb-1">
              <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-success animate-pulse' : 'bg-error'}`}></span>
              <span className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">
                {isConnected ? 'System Live' : 'Connecting...'}
              </span>
            </div>
          </header>

          <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 md:gap-8">
            {patientIds.map((id) => {
              const profile = patientProfiles[id as keyof typeof patientProfiles];
              const data = vitals[id];
              const isHighRisk = data?.risk_label === 'high';
              const status = data?.risk_label ? data.risk_label.toUpperCase() : 'WAITING...';
              const variant = isHighRisk ? 'error' : (data?.risk_label === 'medium' ? 'tertiary' : 'primary');
              const showTrend = activeTrends[id];

              return (
                <Card key={id} className={isHighRisk ? 'border-l-4 border-error/50' : ''}>
                  <CardHeader className="flex justify-between items-start">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 rounded-full overflow-hidden bg-surface-container border-2 border-primary-fixed/20 shadow-sm text-[8px] flex items-center justify-center">
                        {profile.image ? (
                           <img className="w-full h-full object-cover" src={profile.image} alt={profile.name} />
                        ) : (
                           <span className="font-bold">{id}</span>
                        )}
                      </div>
                      <div>
                        <h3 className="font-headline font-bold text-lg text-on-surface">{profile.name}</h3>
                        <Badge variant={variant}>{status}</Badge>
                      </div>
                    </div>
                    <div className="text-right flex flex-col gap-1 items-end">
                      <span className="text-[10px] text-on-surface-variant font-bold uppercase tracking-widest leading-none">{profile.ward}</span>
                      <span className="font-headline font-bold text-primary text-sm uppercase">Bed {profile.bed}</span>
                      <button 
                        onClick={() => toggleTrend(id)}
                        className={`mt-2 flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase tracking-widest transition-all ${
                          showTrend 
                            ? 'bg-primary text-white shadow-lg shadow-primary/20' 
                            : 'bg-surface-container-high text-on-surface hover:bg-surface-container-highest'
                        }`}
                      >
                        <span className="material-symbols-outlined text-[14px]">
                          {showTrend ? 'close' : 'analytics'}
                        </span>
                        {showTrend ? 'Hide Trends' : 'View Trends'}
                      </button>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {showTrend ? (
                      <div className="space-y-4 animate-in fade-in slide-in-from-top-2 duration-500">
                        <div className="flex justify-between items-center text-[10px] font-bold text-outline uppercase tracking-widest">
                          <span>Risk Score History (Grafana)</span>
                          <span className="text-primary">Live Sync</span>
                        </div>
                        <GrafanaEmbed 
                          panelId={5} 
                          variables={{ patient_id: id }} 
                          height={220}
                        />
                        <button 
                          onClick={() => toggleTrend(id)}
                          className="w-full py-2 border-t border-outline-variant/10 text-[10px] font-bold text-on-surface-variant uppercase tracking-widest hover:text-primary transition-colors"
                        >
                          Show Real-time Vitals
                        </button>
                      </div>
                    ) : (
                      <>
                        <ECGWaveform 
                          variant={isHighRisk ? 'alert' : 'stable'} 
                          label={isHighRisk ? 'Tachycardia Alert' : (data ? 'Live Stream Active' : 'Waiting for Device...')} 
                        />
                        <div className="grid grid-cols-3 gap-3 md:gap-4">
                          <StatItem 
                            label="Heart Rate" 
                            value={data?.hr || '--'} 
                            unit="bpm" 
                            variant={isHighRisk ? 'error' : 'default'} 
                          />
                          <StatItem 
                            label="SpO2" 
                            value={data?.spo2 || '--'} 
                            unit="%" 
                            variant={data?.spo2 && data.spo2 < 92 ? 'error' : 'default'} 
                          />
                          <StatItem 
                            label="Temp" 
                            value={data?.temp || '--'} 
                            unit="°C" 
                            variant="default" 
                          />
                        </div>
                        {data && (
                          <div className="pt-4 border-t border-outline-variant/10 flex justify-between items-center text-[10px] font-bold text-on-surface-variant uppercase tracking-tighter">
                              <span>Risk Score: {data.risk_score.toFixed(3)}</span>
                              <span>BP: {data.bp_sys}/{data.bp_dia} mmHg</span>
                          </div>
                        )}
                      </>
                    )}
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>

        <aside className="w-full lg:w-80 space-y-8 flex-shrink-0">
          <Card className="bg-primary text-white border-none shadow-2xl relative overflow-hidden">
            <div className="absolute -right-12 -top-12 w-32 h-32 bg-primary-container rounded-full opacity-30 blur-3xl"></div>
            <CardContent className="p-8 relative z-10 space-y-6">
              <h4 className="font-headline font-bold text-lg mb-4 opacity-80 uppercase tracking-widest text-xs">Infrastructure Status</h4>
              <div className="space-y-6">
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-widest opacity-60 block mb-1">Kafka Throughput</span>
                  <div className="flex items-baseline gap-1">
                    <span className="text-4xl font-extrabold tracking-tighter">1<span className="text-xl opacity-60 ml-1">Hz/node</span></span>
                  </div>
                </div>
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-widest opacity-60 block mb-1">Active Patients</span>
                  <div className="flex items-baseline gap-1">
                    <span className="text-4xl font-extrabold tracking-tighter">{Object.keys(vitals).length}<span className="text-xl opacity-60 ml-1">/3</span></span>
                  </div>
                </div>
              </div>
              <div className="mt-8 pt-8 border-t border-white/10 flex justify-between text-xs font-semibold opacity-70">
                <span>Cluster Node 01</span>
                <span className="text-primary-fixed uppercase tracking-widest">{isConnected ? 'Online' : 'Offline'}</span>
              </div>
            </CardContent>
          </Card>

          <Card className="p-8">
            <div className="flex justify-between items-center mb-6">
              <h4 className="font-headline font-bold text-lg text-on-surface">Recent Alerts</h4>
              <span className="material-symbols-outlined text-outline" style={{ fontVariationSettings: "'OPSZ' 20" }}>history</span>
            </div>
            <div className="space-y-5">
              {Object.values(vitals)
                .filter(v => v.risk_label !== 'low')
                .slice(-3)
                .reverse()
                .map((alert, i) => (
                <div key={i} className="flex gap-4 group">
                  <div className={`mt-1.5 w-1.5 h-1.5 rounded-full flex-shrink-0 ${alert.risk_label === 'high' ? 'bg-error' : 'bg-tertiary'}`}></div>
                  <div className="space-y-0.5">
                    <p className="text-sm font-bold text-on-surface leading-tight group-hover:text-primary transition-colors cursor-pointer">
                      {alert.risk_label === 'high' ? 'Critical Risk Detected' : 'Elevated Risk'}
                    </p>
                    <p className="text-xs text-on-surface-variant font-medium">Patient {alert.patient_id}</p>
                    <span className="text-[10px] text-outline font-bold uppercase tracking-wider">Recently</span>
                  </div>
                </div>
              ))}
              {Object.values(vitals).filter(v => v.risk_label !== 'low').length === 0 && (
                 <p className="text-xs text-on-surface-variant italic py-4">No active alerts recorded.</p>
              )}
            </div>
          </Card>

          <div className="p-6 border border-outline-variant/30 rounded-xl bg-surface-container-low/50 flex gap-4">
            <span className="material-symbols-outlined text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>hub</span>
            <p className="text-xs font-medium text-on-surface-variant leading-relaxed">
              MLOps Bridge synchronized. Data ingestion via <span className="text-primary font-bold">Kafka 2.2.1</span> is stable.
            </p>
          </div>
        </aside>
      </div>
    </AuroraBackground>
  );
};

export default Monitoring;
