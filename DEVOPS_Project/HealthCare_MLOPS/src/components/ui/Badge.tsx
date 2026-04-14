import React from 'react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'primary' | 'secondary' | 'tertiary' | 'error' | 'success' | 'outline';
  children: React.ReactNode;
}

export const Badge: React.FC<BadgeProps> = ({ variant = 'primary', className, children, ...props }) => {
  const variants = {
    primary: 'bg-primary-fixed text-on-primary-fixed-variant',
    secondary: 'bg-secondary-container text-on-secondary-container',
    tertiary: 'bg-tertiary-container text-on-tertiary-container',
    error: 'bg-error-container text-on-error-container',
    success: 'bg-green-100 text-green-800',
    outline: 'border border-outline-variant text-on-surface-variant'
  };

  return (
    <span 
      className={cn(
        "px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider rounded-full inline-flex items-center justify-center",
        variants[variant],
        className
      )} 
      {...props}
    >
      {children}
    </span>
  );
};
