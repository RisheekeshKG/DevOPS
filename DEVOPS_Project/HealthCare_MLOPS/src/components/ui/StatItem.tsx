import React from 'react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface StatItemProps extends React.HTMLAttributes<HTMLDivElement> {
  label: string;
  value: string | number;
  unit?: string;
  variant?: 'default' | 'error' | 'success';
}

export const StatItem: React.FC<StatItemProps> = ({ label, value, unit, variant = 'default', className, ...props }) => {
  const variants = {
    default: 'bg-surface-container-low',
    error: 'bg-error-container/30 border border-error-container/50',
    success: 'bg-green-50'
  };

  const textVariants = {
    default: 'text-on-surface',
    error: 'text-error font-bold',
    success: 'text-green-700 font-bold'
  };

  return (
    <div className={cn("p-3 rounded-lg flex flex-col gap-1 transition-all", variants[variant], className)} {...props}>
      <span className="text-[10px] font-bold text-on-surface-variant uppercase block">{label}</span>
      <div className="flex items-baseline gap-1">
        <span className={cn("font-headline text-2xl font-extrabold tracking-tighter", textVariants[variant])}>{value}</span>
        {unit && <span className="text-[10px] text-on-surface-variant font-medium lowercase">{unit}</span>}
      </div>
    </div>
  );
};
