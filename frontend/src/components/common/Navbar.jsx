import React, { useState, useEffect } from 'react';
import { Shield, Radio, Bell, User, LogOut, Cpu, HardDrive } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const Navbar = () => {
  const { user, logout } = useAuth();
  const [time, setTime] = useState(new Date().toUTCString().slice(17, 25) + ' UTC');

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date().toUTCString().slice(17, 25) + ' UTC');
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="h-14 bg-[#0D1322] border-b border-slate-800/80 px-6 flex items-center justify-between sticky top-0 z-30">
      {/* Brand & Live status */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/40 flex items-center justify-center text-blue-400 cyber-glow">
            <Shield className="w-4 h-4 text-blue-400" />
          </div>
          <div>
            <div className="font-bold tracking-wider text-sm text-slate-100 flex items-center gap-1.5 font-mono">
              CYBERGUARD <span className="text-blue-400 font-extrabold">AI</span>
            </div>
            <div className="text-[10px] text-slate-400 tracking-wider">DEFENSE DECISION-SUPPORT</div>
          </div>
        </div>

        <div className="h-5 w-px bg-slate-800 mx-1" />

        {/* Live Pulse */}
        <div className="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded-full text-[11px] font-mono text-emerald-400">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
          <span>SOC SENSORS ONLINE</span>
        </div>
      </div>

      {/* Center status items */}
      <div className="hidden md:flex items-center gap-6 text-xs text-slate-400 font-mono">
        <div className="flex items-center gap-1.5">
          <Cpu className="w-3.5 h-3.5 text-blue-400" />
          <span>ML INFERENCE: <span className="text-slate-200">ACTIVE</span></span>
        </div>
        <div className="flex items-center gap-1.5">
          <HardDrive className="w-3.5 h-3.5 text-cyan-400" />
          <span>RAG INDEX: <span className="text-slate-200">SYNCED</span></span>
        </div>
        <div className="flex items-center gap-1.5 text-slate-300">
          <span className="text-slate-500">TIME:</span>
          <span>{time}</span>
        </div>
      </div>

      {/* User profile & controls */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 text-right">
          <div>
            <div className="text-xs font-medium text-slate-200">{user?.full_name || 'SOC Analyst'}</div>
            <div className="text-[10px] text-blue-400 font-mono">{user?.role || 'Tier-2 Analyst'}</div>
          </div>
          <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300">
            <User className="w-4 h-4" />
          </div>
        </div>

        <button
          onClick={logout}
          title="Sign Out"
          className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
        >
          <LogOut className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
};
