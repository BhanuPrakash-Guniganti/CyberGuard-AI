import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Activity, 
  ShieldAlert, 
  AlertOctagon, 
  CheckCircle2, 
  Zap, 
  ArrowUpRight, 
  RefreshCw,
  TrendingUp,
  Cpu,
  Layers
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  Tooltip, 
  PieChart, 
  Pie, 
  Cell, 
  BarChart, 
  Bar 
} from 'recharts';
import { dashboardAPI } from '../services/api';
import { SeverityBadge } from '../components/common/SeverityBadge';

export const DashboardPage = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const res = await dashboardAPI.getStats();
      setStats(res.data);
    } catch (err) {
      setError('Failed to fetch SOC metrics from backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  if (loading && !stats) {
    return (
      <div className="flex flex-col items-center justify-center h-96 text-slate-400 font-mono text-xs">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mb-3" />
        <span>Aggregating Real-Time Security Telemetry...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold tracking-wide text-slate-100 font-mono flex items-center gap-2">
            <Layers className="w-5 h-5 text-blue-400" />
            SECURITY OPERATIONS CENTER (SOC) DASHBOARD
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-time Machine Learning Threat Detection, Correlation & Defensive Response Engine
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={fetchStats}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-mono flex items-center gap-1.5 transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh Telemetry</span>
          </button>
          <Link
            to="/incidents/CG-1021"
            className="px-3.5 py-1.5 bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 border border-rose-500/40 rounded-lg text-xs font-mono font-semibold flex items-center gap-1.5 transition-all cyber-glow-red"
          >
            <Zap className="w-3.5 h-3.5 text-rose-400" />
            <span>Active Incident CG-1021</span>
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <div className="soc-card border-blue-500/30 relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
            <span>TOTAL EVENTS</span>
            <Activity className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-slate-100 mt-2">
            {stats?.total_events || 0}
          </div>
          <div className="text-[11px] text-emerald-400 mt-1 flex items-center gap-1">
            <TrendingUp className="w-3 h-3" /> Live Sensor Stream
          </div>
        </div>

        <div className="soc-card border-amber-500/30">
          <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
            <span>ACTIVE INCIDENTS</span>
            <ShieldAlert className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-amber-300 mt-2">
            {stats?.active_incidents || 0}
          </div>
          <div className="text-[11px] text-slate-400 mt-1">Correlated Clusters</div>
        </div>

        <div className="soc-card border-rose-500/40 bg-rose-950/20">
          <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
            <span>CRITICAL INCIDENTS</span>
            <ShieldAlert className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-rose-400 mt-2">
            {stats?.critical_incidents || 0}
          </div>
          <div className="text-[11px] text-rose-400/80 mt-1">Requires Immediate Action</div>
        </div>

        <div className="soc-card border-orange-500/30">
          <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
            <span>ML ALERTS</span>
            <AlertOctagon className="w-4 h-4 text-orange-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-orange-300 mt-2">
            {stats?.open_alerts || 0}
          </div>
          <div className="text-[11px] text-slate-400 mt-1">RF & IsoForest Flagged</div>
        </div>

        <div className="soc-card border-emerald-500/30">
          <div className="flex items-center justify-between text-slate-400 text-xs font-mono">
            <span>INVESTIGATED</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-300 mt-2">
            {stats?.investigated_incidents || 0}
          </div>
          <div className="text-[11px] text-emerald-400/80 mt-1">Agent Processed</div>
        </div>
      </div>

      {/* Visual Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Threat Activity Area Chart */}
        <div className="lg:col-span-2 soc-card">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-bold font-mono text-slate-200">THREAT TELEMETRY OVER TIME</h2>
              <p className="text-[11px] text-slate-400">Events, Anomaly Invocations & Detection Peaks</p>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/30">
              15-Min Windows
            </span>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats?.threat_activity || []}>
                <defs>
                  <linearGradient id="colorEvents" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorAlerts" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#EF4444" stopOpacity={0.6}/>
                    <stop offset="95%" stopColor="#EF4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="time" stroke="#475569" fontSize={11} />
                <YAxis stroke="#475569" fontSize={11} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
                  itemStyle={{ color: '#E2E8F0' }}
                />
                <Area type="monotone" dataKey="events_count" stroke="#3B82F6" fillOpacity={1} fill="url(#colorEvents)" name="Total Events" />
                <Area type="monotone" dataKey="alerts_count" stroke="#EF4444" fillOpacity={1} fill="url(#colorAlerts)" name="ML Alerts" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Severity Distribution Pie */}
        <div className="soc-card flex flex-col justify-between">
          <div>
            <h2 className="text-sm font-bold font-mono text-slate-200 mb-1">SEVERITY BREAKDOWN</h2>
            <p className="text-[11px] text-slate-400 mb-2">Proportion of Telemetry Severities</p>
          </div>
          <div className="h-48 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats?.severity_distribution || []}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={75}
                  paddingAngle={4}
                >
                  {(stats?.severity_distribution || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-800 text-[11px] font-mono">
            {(stats?.severity_distribution || []).slice(0, 4).map((s) => (
              <div key={s.name} className="flex items-center justify-between text-slate-300">
                <span className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: s.color }} />
                  {s.name}:
                </span>
                <span className="font-bold">{s.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Category Breakdown & Recent Alerts Table */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Attack Category Bar Chart */}
        <div className="soc-card">
          <h2 className="text-sm font-bold font-mono text-slate-200 mb-1">ATTACK CATEGORY CLASSIFICATION</h2>
          <p className="text-[11px] text-slate-400 mb-4">Supervised Random Forest Detections</p>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats?.category_distribution || []} layout="vertical">
                <XAxis type="number" stroke="#475569" fontSize={11} />
                <YAxis dataKey="category" type="category" stroke="#94A3B8" fontSize={10} width={110} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
                />
                <Bar dataKey="count" fill="#3B82F6" radius={[0, 4, 4, 0]} name="Detected Instances" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent ML Alerts Table */}
        <div className="lg:col-span-2 soc-card">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-bold font-mono text-slate-200">RECENT ML-TRIGGERED ALERTS</h2>
              <p className="text-[11px] text-slate-400">Classified in real-time by Random Forest & Isolation Forest</p>
            </div>
            <Link to="/alerts" className="text-xs font-mono text-blue-400 hover:text-blue-300 flex items-center gap-1">
              View All Alerts <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900/60 font-mono text-[11px] text-slate-400 uppercase border-b border-slate-800">
                <tr>
                  <th className="py-2.5 px-3">Alert ID</th>
                  <th className="py-2.5 px-3">Attack Type</th>
                  <th className="py-2.5 px-3">Severity</th>
                  <th className="py-2.5 px-3">Confidence</th>
                  <th className="py-2.5 px-3">Target Device</th>
                  <th className="py-2.5 px-3">Incident</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono">
                {(stats?.recent_alerts || []).map((alert) => (
                  <tr key={alert.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-2.5 px-3 text-blue-400 font-semibold">{alert.alert_id}</td>
                    <td className="py-2.5 px-3 text-slate-200">{alert.attack_type}</td>
                    <td className="py-2.5 px-3">
                      <SeverityBadge severity={alert.severity} />
                    </td>
                    <td className="py-2.5 px-3">
                      <div className="flex items-center gap-2">
                        <div className="w-12 bg-slate-800 rounded-full h-1.5 overflow-hidden">
                          <div 
                            className="bg-blue-500 h-full rounded-full" 
                            style={{ width: `${Math.round((alert.confidence || 0.8) * 100)}%` }} 
                          />
                        </div>
                        <span className="text-slate-400 text-[11px]">{Math.round((alert.confidence || 0.8) * 100)}%</span>
                      </div>
                    </td>
                    <td className="py-2.5 px-3 text-slate-300">{alert.device}</td>
                    <td className="py-2.5 px-3">
                      {alert.incident_id ? (
                        <Link 
                          to={`/incidents/${alert.incident_id}`}
                          className="px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 hover:bg-blue-500/20 border border-blue-500/30 text-[11px]"
                        >
                          {alert.incident_id}
                        </Link>
                      ) : (
                        <span className="text-slate-600">-</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
