import React from 'react';
import { AlertTriangle, AlertCircle, Info, ShieldAlert, ShieldCheck } from 'lucide-react';

export const SeverityBadge = ({ severity }) => {
  const s = severity?.toLowerCase() || 'info';

  if (s === 'critical') {
    return (
      <span className="soc-badge-critical">
        <ShieldAlert className="w-3.5 h-3.5 animate-pulse" />
        CRITICAL
      </span>
    );
  }
  if (s === 'high') {
    return (
      <span className="soc-badge-high">
        <AlertTriangle className="w-3.5 h-3.5" />
        HIGH
      </span>
    );
  }
  if (s === 'medium') {
    return (
      <span className="soc-badge-medium">
        <AlertCircle className="w-3.5 h-3.5" />
        MEDIUM
      </span>
    );
  }
  if (s === 'low') {
    return (
      <span className="soc-badge-low">
        <ShieldCheck className="w-3.5 h-3.5" />
        LOW
      </span>
    );
  }
  return (
    <span className="soc-badge-info">
      <Info className="w-3.5 h-3.5" />
      INFO
    </span>
  );
};
