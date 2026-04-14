import React from 'react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface ECGWaveformProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'stable' | 'alert';
  label?: string;
}

const ECGWaveform: React.FC<ECGWaveformProps> = ({ variant = 'stable', label = 'Live AD8232', className, ...props }) => {
  const isAlert = variant === 'alert';
  const strokeColor = isAlert ? '#ba1a1a' : '#003d9b';
  const liveLabelClass = isAlert ? 'text-error' : 'text-primary';
  const pulseColor = isAlert ? 'bg-error' : 'bg-primary';

  // Path data from the original design
  const stablePath = "M 0 50 L 50 50 L 55 40 L 60 60 L 65 20 L 70 80 L 75 50 L 150 50 L 155 40 L 160 60 L 165 20 L 170 80 L 175 50 L 250 50 L 255 40 L 260 60 L 265 20 L 270 80 L 275 50 L 400 50";
  const alertPath = "M 0 50 L 20 50 L 30 10 L 40 90 L 50 50 L 70 50 L 80 10 L 90 90 L 100 50 L 120 50 L 130 10 L 140 90 L 150 50 L 170 50 L 180 10 L 190 90 L 200 50 L 220 50 L 230 10 L 240 90 L 250 50 L 400 50";

  return (
    <div className={cn("h-32 w-full ecg-grid rounded-lg relative overflow-hidden flex items-center bg-transparent border border-outline-variant/5", className)} {...props}>
      <svg className="absolute inset-0 w-full h-full" preserveAspectRatio="none" viewBox="0 0 400 100">
        <path 
          d={isAlert ? alertPath : stablePath} 
          fill="none" 
          stroke={strokeColor} 
          strokeWidth="2" 
          strokeLinecap="round" 
          strokeLinejoin="round" 
        />
      </svg>
      <div className={cn("absolute top-2 right-2 flex items-center gap-1.5 text-[10px] font-bold uppercase", liveLabelClass)}>
        <span className={cn("w-2 h-2 rounded-full animate-pulse", pulseColor)}></span>
        {label}
      </div>
    </div>
  );
};

export default ECGWaveform;
