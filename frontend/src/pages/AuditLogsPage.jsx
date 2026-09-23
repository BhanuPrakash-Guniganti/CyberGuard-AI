import React, { useState, useEffect } from 'react';
import { ScrollText, RefreshCw, Shield, Clock, CheckCircle2, User, Lock } from 'lucide-react';
import { auditAPI } from '../services/api';

export const AuditLogsPage = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const res = await auditAPI.list();
      setLogs(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  return (
    <div className="space-y-6 max-w-6xl mx-auto font-mono text-xs">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold tracking-wide text-slate-100 flex items-center gap-2">
            <ScrollText className="w-5 h-5 text-blue-400" />
            SOC COMPLIANCE & SIMULATION AUDIT TRAIL
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Immutable log of all human approvals, policy evaluations, and response simulations
          </p>
        </div>
        <button
          onClick={fetchLogs}
          className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg flex items-center gap-1.5 transition-colors"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      {/* Audit Log Table */}
      <div className="soc-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/80 text-[11px] text-slate-400 uppercase border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Timestamp (UTC)</th>
                <th className="py-3 px-4">Analyst / Initiator</th>
                <th className="py-3 px-4">Action</th>
                <th className="py-3 px-4">Incident Target</th>
                <th className="py-3 px-4">Reason / Notes</th>
                <th className="py-3 px-4">Approval</th>
                <th className="py-3 px-4">Simulation Result</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-xs">
              {loading && logs.length === 0 ? (
                <tr>
                  <td colSpan="7" className="py-8 text-center text-slate-500">
                    Loading compliance audit log...
                  </td>
                </tr>
              ) : logs.length === 0 ? (
                <tr>
                  <td colSpan="7" className="py-8 text-center text-slate-500">
                    No audit records recorded yet.
                  </td>
                </tr>
              ) : (
                logs.map((l) => (
                  <tr key={l.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-4 text-slate-400 text-[11px]">
                      {l.timestamp?.slice(0, 19).replace('T', ' ')}
                    </td>
                    <td className="py-3 px-4 text-slate-200 flex items-center gap-1.5">
                      <User className="w-3.5 h-3.5 text-cyan-400" />
                      <span>{l.user}</span>
                    </td>
                    <td className="py-3 px-4 text-blue-400 font-bold">{l.action}</td>
                    <td className="py-3 px-4 text-slate-300">
                      {l.incident_id || 'System'} {l.target ? `(${l.target})` : ''}
                    </td>
                    <td className="py-3 px-4 text-slate-400 text-[11px] max-w-xs truncate">
                      {l.reason || '-'}
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        l.approval_status === 'APPROVED' || l.approval_status === 'AUTO'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                          : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                      }`}>
                        {l.approval_status || 'N/A'}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-emerald-400 font-semibold flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3" />
                        {l.simulation_status || 'COMPLETED'}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
