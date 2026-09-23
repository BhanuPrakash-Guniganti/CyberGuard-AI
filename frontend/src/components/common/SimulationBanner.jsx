import React from 'react';
import { Shield, Lock } from 'lucide-react';

export const SimulationBanner = () => {
  return (
    <div className="bg-gradient-to-r from-blue-950/80 via-slate-900 to-indigo-950/80 border-b border-blue-500/20 px-4 py-2 text-xs text-blue-300/90 flex items-center justify-between">
      <div className="flex items-center gap-2">
        <Shield className="w-3.5 h-3.5 text-cyan-400" />
        <span className="font-semibold text-slate-200">CYBERGUARD DEFENSE SIMULATION</span>
        <span className="text-slate-500">•</span>
        <span>Controlled Academic Decision-Support Environment</span>
      </div>
      <div className="flex items-center gap-1.5 font-mono text-[11px] bg-blue-500/10 border border-blue-500/30 px-2 py-0.5 rounded text-cyan-300">
        <Lock className="w-3 h-3 text-cyan-400" />
        Simulation Only — Actual Infrastructure Not Modified
      </div>
    </div>
  );
};
