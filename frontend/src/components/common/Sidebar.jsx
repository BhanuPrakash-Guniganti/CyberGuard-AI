import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Activity, 
  AlertOctagon, 
  ShieldAlert, 
  BookOpen, 
  Sliders, 
  FileText, 
  ScrollText,
  Bot
} from 'lucide-react';

const NAV_ITEMS = [
  { name: 'SOC Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Security Events', path: '/events', icon: Activity },
  { name: 'ML Alerts', path: '/alerts', icon: AlertOctagon },
  { name: 'Correlated Incidents', path: '/incidents', icon: ShieldAlert },
  { name: 'RAG Knowledge', path: '/knowledge', icon: BookOpen },
  { name: 'Response Simulator', path: '/simulator', icon: Sliders },
  { name: 'Audit Trail', path: '/audit', icon: ScrollText },
];

export const Sidebar = () => {
  return (
    <aside className="w-64 bg-[#0D1322]/95 border-r border-slate-800/80 flex flex-col justify-between p-4 shrink-0 min-h-[calc(100vh-3.5rem)]">
      <div className="space-y-6">
        <div>
          <div className="text-[10px] font-mono font-semibold tracking-wider text-slate-500 uppercase px-3 mb-2">
            SOC Operations
          </div>
          <nav className="space-y-1">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  end={item.path === '/'}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                      isActive
                        ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30 shadow-sm font-semibold'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                    }`
                  }
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{item.name}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* Quick Spotlight for Incident CG-1021 */}
        <div className="p-3 bg-gradient-to-br from-rose-950/40 via-slate-900/60 to-slate-900/80 border border-rose-500/30 rounded-xl">
          <div className="flex items-center gap-2 mb-1.5">
            <span className="w-2 h-2 rounded-full bg-rose-500 animate-pulse" />
            <span className="text-[11px] font-mono font-bold text-rose-400 uppercase tracking-wide">Featured Incident</span>
          </div>
          <div className="text-xs font-semibold text-slate-200 mb-1">Incident CG-1021</div>
          <p className="text-[11px] text-slate-400 mb-2.5 leading-snug">Multi-Stage Credential Compromise to Data Exfiltration</p>
          <NavLink
            to="/incidents/CG-1021"
            className="block text-center py-1.5 px-2 bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 border border-rose-500/40 rounded-lg text-[11px] font-mono transition-colors"
          >
            Launch Investigation →
          </NavLink>
        </div>
      </div>

      {/* System info */}
      <div className="border-t border-slate-800/80 pt-3 text-[11px] text-slate-500 font-mono space-y-1">
        <div className="flex justify-between">
          <span>PIPELINE:</span>
          <span className="text-slate-400">RandomForest+IsoF</span>
        </div>
        <div className="flex justify-between">
          <span>POLICY:</span>
          <span className="text-slate-400">Strict Sandbox</span>
        </div>
        <div className="flex justify-between text-[10px] text-slate-600 pt-1">
          <span>CYBERGUARD v1.0.0</span>
          <span>SOC DEMO</span>
        </div>
      </div>
    </aside>
  );
};
