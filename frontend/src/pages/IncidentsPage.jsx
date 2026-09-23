import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  ShieldAlert, 
  Search, 
  RefreshCw, 
  ArrowRight, 
  Layers, 
  Clock, 
  Server, 
  Activity,
  Flame,
  CheckCircle2
} from 'lucide-react';
import { incidentsAPI } from '../services/api';
import { SeverityBadge } from '../components/common/SeverityBadge';

export const IncidentsPage = () => {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [severityFilter, setSeverityFilter] = useState('All');
  const [statusFilter, setStatusFilter] = useState('All');

  const fetchIncidents = async () => {
    setLoading(true);
    try {
      const res = await incidentsAPI.list({
        severity: severityFilter !== 'All' ? severityFilter : undefined,
        status: statusFilter !== 'All' ? statusFilter : undefined,
      });
      setIncidents(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIncidents();
  }, [severityFilter, statusFilter]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold font-mono tracking-wide text-slate-100 flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-amber-400" />
            CORRELATED SECURITY INCIDENTS
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Temporal & entity-correlated event clusters evaluated by the composite Risk Engine (0–100 score)
          </p>
        </div>
        <button
          onClick={fetchIncidents}
          className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-mono flex items-center gap-1.5 transition-colors self-start md:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Incidents</span>
        </button>
      </div>

      {/* Filter Bar */}
      <div className="soc-card p-4 flex flex-wrap items-center gap-3 font-mono text-xs">
        <span className="text-slate-400">FILTERS:</span>
        <select
          value={severityFilter}
          onChange={(e) => setSeverityFilter(e.target.value)}
          className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-slate-200 focus:outline-none focus:border-blue-500"
        >
          <option value="All">All Severities</option>
          <option value="Critical">Critical</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>

        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-slate-200 focus:outline-none focus:border-blue-500"
        >
          <option value="All">All Statuses</option>
          <option value="Active">Active</option>
          <option value="Investigated">Investigated</option>
          <option value="Contained (Simulated)">Contained (Simulated)</option>
        </select>
      </div>

      {/* Incidents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {loading && incidents.length === 0 ? (
          <div className="col-span-2 py-12 text-center text-slate-500 font-mono text-xs">
            Loading correlated incidents...
          </div>
        ) : incidents.length === 0 ? (
          <div className="col-span-2 py-12 text-center text-slate-500 font-mono text-xs">
            No correlated incidents found for this filter.
          </div>
        ) : (
          incidents.map((inc) => (
            <div 
              key={inc.id}
              className={`soc-card flex flex-col justify-between hover:border-slate-600 transition-all ${
                inc.incident_id === 'CG-1021' ? 'border-rose-500/50 bg-gradient-to-br from-[#111827] to-rose-950/20' : ''
              }`}
            >
              <div>
                {/* Header line */}
                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                  <div className="flex items-center gap-2 font-mono">
                    <span className="text-sm font-bold text-slate-100">{inc.incident_id}</span>
                    <span className="text-[11px] text-slate-400 bg-slate-800/80 px-2 py-0.5 rounded">
                      {inc.category}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <SeverityBadge severity={inc.severity} />
                  </div>
                </div>

                {/* Title & Description */}
                <div className="py-3">
                  <h3 className="text-sm font-bold text-slate-100 leading-snug">{inc.title}</h3>
                  <p className="text-xs text-slate-400 mt-1.5 line-clamp-2 leading-relaxed font-mono">
                    {inc.description}
                  </p>
                </div>

                {/* Metrics Badges */}
                <div className="grid grid-cols-3 gap-2 py-3 border-t border-b border-slate-800/80 font-mono text-[11px]">
                  <div className="bg-slate-900/60 p-2 rounded border border-slate-800/60">
                    <div className="text-slate-500 text-[10px]">RISK SCORE</div>
                    <div className={`text-base font-bold ${
                      inc.risk_score >= 80 ? 'text-rose-400' : inc.risk_score >= 60 ? 'text-orange-400' : 'text-amber-400'
                    }`}>
                      {inc.risk_score}/100
                    </div>
                  </div>

                  <div className="bg-slate-900/60 p-2 rounded border border-slate-800/60">
                    <div className="text-slate-500 text-[10px]">ATTACK STAGES</div>
                    <div className="text-base font-bold text-cyan-400">
                      {inc.attack_chain?.length || 0} Stages
                    </div>
                  </div>

                  <div className="bg-slate-900/60 p-2 rounded border border-slate-800/60">
                    <div className="text-slate-500 text-[10px]">AFFECTED HOSTS</div>
                    <div className="text-base font-bold text-slate-200">
                      {inc.affected_assets?.length || 1}
                    </div>
                  </div>
                </div>

                {/* Affected Entities */}
                <div className="pt-3 text-xs font-mono text-slate-400 space-y-1">
                  <div className="flex items-center gap-1.5">
                    <Server className="w-3.5 h-3.5 text-slate-500" />
                    <span>Assets: <span className="text-slate-300">{inc.affected_assets?.join(', ') || 'N/A'}</span></span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-slate-500" />
                    <span>First Seen: <span className="text-slate-400">{inc.created_at?.slice(0, 19).replace('T', ' ')} UTC</span></span>
                  </div>
                </div>
              </div>

              {/* Action Footer */}
              <div className="pt-4 mt-3 border-t border-slate-800 flex items-center justify-between">
                <span className={`text-[11px] font-mono font-semibold px-2 py-0.5 rounded ${
                  inc.status === 'Contained (Simulated)'
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                    : inc.status === 'Investigated'
                    ? 'bg-blue-500/10 text-blue-400 border border-blue-500/30'
                    : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                }`}>
                  Status: {inc.status}
                </span>

                <Link
                  to={`/incidents/${inc.incident_id}`}
                  className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-mono font-semibold flex items-center gap-1.5 transition-colors shadow-sm"
                >
                  <span>Investigate Incident</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
