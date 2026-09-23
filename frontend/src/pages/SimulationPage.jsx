import React, { useState, useEffect } from 'react';
import { Sliders, Shield, Lock, CheckCircle2, AlertTriangle, Play, RefreshCw, Terminal } from 'lucide-react';
import { responseAPI } from '../services/api';

export const SimulationPage = () => {
  const [action, setAction] = useState('ISOLATE_ENDPOINT');
  const [target, setTarget] = useState('endpoint-03');
  const [incidentId, setIncidentId] = useState('CG-1021');
  const [approved, setApproved] = useState(true);
  const [analystNotes, setAnalystNotes] = useState('Analyst defensive simulation run');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSimulate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await responseAPI.simulate({
        incident_id: incidentId,
        action,
        target,
        approved,
        analyst_notes: analystNotes
      });
      setResult(res.data);
    } catch (err) {
      alert('Simulation execution failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto font-mono text-xs">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold tracking-wide text-slate-100 flex items-center gap-2">
          <Sliders className="w-5 h-5 text-emerald-400" />
          DEFENSIVE RESPONSE SIMULATOR SANDBOX
        </h1>
        <p className="text-xs text-slate-400 mt-0.5">
          Execute policy-validated containment actions in a segregated simulation environment
        </p>
      </div>

      {/* Safety Notice Card */}
      <div className="soc-card border-blue-500/30 bg-blue-950/20 p-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center text-blue-400">
            <Lock className="w-4 h-4" />
          </div>
          <div>
            <div className="font-bold text-slate-200">ACADEMIC SAFETY SANDBOX ACTIVE</div>
            <div className="text-[11px] text-slate-400">All responses operate strictly on simulated sandbox state. Real infrastructure is never modified.</div>
          </div>
        </div>
        <span className="px-2.5 py-1 bg-blue-500/10 text-cyan-300 border border-blue-500/30 rounded text-[11px] font-bold">
          SANDBOX ISOLATED
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Simulator Form */}
        <div className="soc-card p-5">
          <h2 className="text-sm font-bold text-slate-200 mb-4 pb-2 border-b border-slate-800 flex items-center gap-2">
            <Terminal className="w-4 h-4 text-cyan-400" />
            CONFIGURE SIMULATED CONTAINMENT
          </h2>

          <form onSubmit={handleSimulate} className="space-y-3.5">
            <div>
              <label className="block text-slate-400 mb-1">INCIDENT IDENTIFIER</label>
              <input
                type="text"
                value={incidentId}
                onChange={(e) => setIncidentId(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1">DEFENSIVE ACTION</label>
              <select
                value={action}
                onChange={(e) => setAction(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200"
              >
                <option value="ISOLATE_ENDPOINT">ISOLATE_ENDPOINT (Network Disconnection)</option>
                <option value="REVOKE_SESSION">REVOKE_SESSION (Invalidate Tokens)</option>
                <option value="BLOCK_SOURCE">BLOCK_SOURCE (Firewall Perimeter Drop)</option>
                <option value="INCREASE_MONITORING">INCREASE_MONITORING (100% EDR Capture)</option>
                <option value="ESCALATE_INCIDENT">ESCALATE_INCIDENT (Tier-3 Transfer)</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-400 mb-1">TARGET HOST / ENTITY</label>
              <input
                type="text"
                value={target}
                onChange={(e) => setTarget(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1">ANALYST REASONING NOTES</label>
              <input
                type="text"
                value={analystNotes}
                onChange={(e) => setAnalystNotes(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-200"
              />
            </div>

            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800 flex items-center gap-2">
              <input
                type="checkbox"
                id="appCheck"
                checked={approved}
                onChange={(e) => setApproved(e.target.checked)}
                className="rounded border-slate-700 text-blue-600 focus:ring-blue-500"
              />
              <label htmlFor="appCheck" className="text-[11px] text-slate-300 cursor-pointer">
                Human Analyst Sign-off Provided
              </label>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white rounded-lg font-bold flex items-center justify-center gap-2 shadow-lg shadow-emerald-600/20"
            >
              <Play className="w-4 h-4" />
              <span>{loading ? 'Executing Sandbox...' : 'Run Simulation'}</span>
            </button>
          </form>
        </div>

        {/* Live Simulation Output Card */}
        <div className="soc-card p-5 flex flex-col justify-between">
          <div>
            <h2 className="text-sm font-bold text-slate-200 mb-4 pb-2 border-b border-slate-800 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              SIMULATION SANDBOX TELEMETRY
            </h2>

            {result ? (
              <div className="space-y-3">
                <div className="bg-slate-950 p-3.5 rounded-lg border border-emerald-500/40 space-y-2">
                  <div className="flex justify-between text-[11px]">
                    <span className="text-slate-400">Simulation ID:</span>
                    <span className="text-cyan-400 font-bold">{result.simulation_id}</span>
                  </div>
                  <div className="flex justify-between text-[11px]">
                    <span className="text-slate-400">Status:</span>
                    <span className="text-emerald-400 font-bold">{result.status}</span>
                  </div>
                  <div className="flex justify-between text-[11px]">
                    <span className="text-slate-400">Target:</span>
                    <span className="text-slate-200">{result.target}</span>
                  </div>
                  <div className="flex justify-between text-[11px]">
                    <span className="text-slate-400">Action:</span>
                    <span className="text-blue-400 font-bold">{result.action}</span>
                  </div>
                </div>

                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                  <div className="text-slate-500 text-[10px] mb-1">SANDBOX STATE MUTATION:</div>
                  <pre className="text-slate-300 text-[10px] overflow-x-auto">
                    {JSON.stringify(result.simulated_state_change, null, 2)}
                  </pre>
                </div>
              </div>
            ) : (
              <div className="py-16 text-center text-slate-500">
                Execute a response action from the left panel to inspect real-time sandbox telemetry.
              </div>
            )}
          </div>

          <div className="pt-3 border-t border-slate-800 text-[10px] text-emerald-400 font-bold text-center">
            ✓ Simulation Only — Actual Infrastructure Not Modified.
          </div>
        </div>
      </div>
    </div>
  );
};
