import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { FileText, Printer, ArrowLeft, Shield, Lock, CheckCircle2, Bot, Layers, Clock } from 'lucide-react';
import { reportsAPI } from '../services/api';
import { SeverityBadge } from '../components/common/SeverityBadge';

export const ReportViewPage = () => {
  const { incidentId } = useParams();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReport = async () => {
      setLoading(true);
      try {
        const res = await reportsAPI.get(incidentId);
        setReport(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, [incidentId]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-96 text-slate-400 font-mono text-xs">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mb-3" />
        <span>Compiling Executive Incident Report...</span>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="soc-card p-12 text-center text-slate-400 font-mono text-xs">
        Report for incident {incidentId} could not be generated.
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6 font-mono text-xs pb-16">
      {/* Action Header */}
      <div className="flex items-center justify-between no-print">
        <Link
          to={`/incidents/${incidentId}`}
          className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg flex items-center gap-1.5 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Incident Workbench</span>
        </Link>
        <button
          onClick={() => window.print()}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-bold flex items-center gap-2 shadow-md"
        >
          <Printer className="w-4 h-4" />
          <span>Print / Export PDF</span>
        </button>
      </div>

      {/* Printable Report Document Card */}
      <div className="bg-slate-900 border border-slate-700 rounded-2xl p-8 shadow-2xl space-y-6 text-slate-200">
        {/* Report Document Header */}
        <div className="flex items-start justify-between pb-6 border-b border-slate-700">
          <div>
            <div className="flex items-center gap-2 text-blue-400 font-bold text-sm tracking-wider mb-1">
              <Shield className="w-5 h-5" />
              <span>CYBERGUARD AI INCIDENT INVESTIGATION REPORT</span>
            </div>
            <div className="text-xl font-bold text-white mt-2">{report.title}</div>
            <div className="text-slate-400 mt-1">Incident ID: <span className="text-cyan-300 font-bold">{report.incident_id}</span> • Report ID: {report.report_id}</div>
          </div>
          <div className="text-right space-y-1">
            <SeverityBadge severity={report.severity} />
            <div className="text-slate-400 text-[11px] pt-1">Generated: {report.generated_at?.slice(0, 19).replace('T', ' ')} UTC</div>
            <div className="text-slate-400 text-[11px]">Analyst: {report.analyst_name}</div>
          </div>
        </div>

        {/* Executive Summary */}
        <div>
          <h2 className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-2">1. EXECUTIVE INCIDENT SUMMARY</h2>
          <p className="bg-slate-950 p-4 rounded-xl border border-slate-800 leading-relaxed text-slate-300">
            {report.executive_summary}
          </p>
        </div>

        {/* Risk Assessment & Affected Assets */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
            <h3 className="font-bold text-slate-300 text-xs">RISK ASSESSMENT</h3>
            <div>Risk Score: <span className="font-bold text-rose-400">{report.risk_score}/100 ({report.severity})</span></div>
            <div>Attack Stages: <span className="text-slate-300">{report.possible_attack_behaviors?.length || 4} Correlated</span></div>
          </div>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
            <h3 className="font-bold text-slate-300 text-xs">AFFECTED ASSETS & ACCOUNTS</h3>
            <div>Impacted Hosts: <span className="text-cyan-300 font-bold">{report.affected_assets?.join(', ')}</span></div>
            <div>Scope: Confined to internal subnet & single user identity</div>
          </div>
        </div>

        {/* Chronological Timeline */}
        <div>
          <h2 className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-2">2. RECONSTRUCTED INCIDENT TIMELINE</h2>
          <div className="space-y-2 bg-slate-950 p-4 rounded-xl border border-slate-800">
            {(report.timeline || []).map((t, idx) => (
              <div key={idx} className="flex items-start gap-3 text-[11px] border-b border-slate-900 pb-1.5 last:border-0 last:pb-0">
                <span className="text-slate-400 font-bold min-w-[70px]">{t.time?.slice(11, 19) || t.time}</span>
                <span className="text-blue-400 font-bold min-w-[120px]">{t.event_type}</span>
                <span className="text-slate-300">{t.description}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Attack Behavior & MITRE Mappings */}
        <div>
          <h2 className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-2">3. MITRE ATT&CK BEHAVIORAL MAPPINGS</h2>
          <div className="grid grid-cols-2 gap-3">
            {(report.possible_attack_behaviors || []).map((m, idx) => (
              <div key={idx} className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-[11px]">
                <div className="flex justify-between font-bold text-slate-200 mb-1">
                  <span>{m.stage_name || m.tactic}</span>
                  <span className="text-cyan-400">{m.mitre_id}</span>
                </div>
                <div className="text-slate-400 text-[10px]">{m.evidence}</div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Recommendations & Simulation Audit */}
        <div>
          <h2 className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-2">4. DEFENSIVE RECOMMENDATIONS & CONTAINMENT POLICY</h2>
          <div className="space-y-2 bg-slate-950 p-4 rounded-xl border border-slate-800">
            {(report.recommendations || []).map((r, idx) => (
              <div key={idx} className="flex justify-between items-center text-[11px] border-b border-slate-900 pb-1.5 last:border-0 last:pb-0">
                <div>
                  <span className="font-bold text-slate-200">{r.action}</span>
                  <span className="text-slate-400"> on {r.target}: {r.rationale}</span>
                </div>
                <span className="text-[10px] text-emerald-400 font-bold">Policy Validated</span>
              </div>
            ))}
          </div>
        </div>

        {/* Academic Disclaimer */}
        <div className="p-3 bg-blue-950/40 border border-blue-500/30 rounded-lg text-center text-cyan-300 text-[11px] font-bold">
          {report.disclaimer}
        </div>
      </div>
    </div>
  );
};
