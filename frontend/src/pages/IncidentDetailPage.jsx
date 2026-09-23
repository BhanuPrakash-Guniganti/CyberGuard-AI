import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  ShieldAlert, 
  Clock, 
  Server, 
  User, 
  Cpu, 
  Bot, 
  Play, 
  CheckCircle2, 
  AlertTriangle, 
  FileText, 
  Sliders, 
  RefreshCw, 
  CornerDownRight, 
  Send,
  BookOpen,
  ArrowRight,
  ShieldCheck,
  Lock,
  Layers,
  Sparkles,
  Info,
  Terminal
} from 'lucide-react';
import { incidentsAPI, investigationAPI, responseAPI } from '../services/api';
import { SeverityBadge } from '../components/common/SeverityBadge';

export const IncidentDetailPage = () => {
  const { id } = useParams();
  const [incident, setIncident] = useState(null);
  const [loading, setLoading] = useState(true);
  const [investigationData, setInvestigationData] = useState(null);
  const [isInvestigating, setIsInvestigating] = useState(false);
  const [chatQuery, setChatQuery] = useState('');
  const [chatMessages, setChatMessages] = useState([]);
  
  // Response Simulation Modal State
  const [selectedAction, setSelectedAction] = useState(null);
  const [isSimulationModalOpen, setIsSimulationModalOpen] = useState(false);
  const [isApprovedByAnalyst, setIsApprovedByAnalyst] = useState(false);
  const [simulationResult, setSimulationResult] = useState(null);
  const [isSimulating, setIsSimulating] = useState(false);

  const fetchIncident = async () => {
    setLoading(true);
    try {
      const res = await incidentsAPI.get(id);
      setIncident(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIncident();
  }, [id]);

  const handleRunInvestigation = async (queryText = null) => {
    setIsInvestigating(true);
    try {
      const res = await investigationAPI.investigate(id, { query: queryText || undefined });
      setInvestigationData(res.data.result);
      if (queryText) {
        setChatMessages(prev => [
          ...prev,
          { role: 'user', content: queryText },
          { 
            role: 'assistant', 
            content: res.data.result.summary,
            grounding: {
              evidenceCount: res.data.result.evidence?.length,
              ragSources: res.data.result.rag_sources
            }
          }
        ]);
        setChatQuery('');
      }
      fetchIncident(); // Refresh updated status
    } catch (err) {
      alert('Failed to complete AI investigation workflow');
    } finally {
      setIsInvestigating(false);
    }
  };

  const handleOpenSimulation = (rec) => {
    setSelectedAction({
      action: rec.action,
      target: rec.target,
      priority: rec.priority,
      rationale: rec.rationale,
      requires_approval: rec.requires_approval
    });
    setIsApprovedByAnalyst(false);
    setSimulationResult(null);
    setIsSimulationModalOpen(true);
  };

  const handleExecuteSimulation = async () => {
    if (!selectedAction) return;
    setIsSimulating(true);
    try {
      const res = await responseAPI.simulate({
        incident_id: id,
        action: selectedAction.action,
        target: selectedAction.target,
        approved: isApprovedByAnalyst,
        analyst_notes: `Manual analyst execution from incident ${id}`
      });
      setSimulationResult(res.data);
      fetchIncident();
    } catch (err) {
      alert('Failed to execute defensive simulation');
    } finally {
      setIsSimulating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-96 text-slate-400 font-mono text-xs">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mb-3" />
        <span>Loading Correlated Incident Telemetry & Graph...</span>
      </div>
    );
  }

  if (!incident) {
    return (
      <div className="soc-card p-12 text-center text-slate-400 font-mono text-xs">
        Incident {id} not found in database.
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* 1. Incident Header Card */}
      <div className="soc-card border-blue-500/30 bg-gradient-to-r from-[#111827] via-[#151D30] to-[#111827] p-6 shadow-2xl relative overflow-hidden">
        <div className="absolute right-0 top-0 w-96 h-full bg-blue-500/5 blur-3xl pointer-events-none" />
        
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-3 mb-2 font-mono">
              <span className="text-xl font-extrabold text-blue-400 tracking-wider">
                INCIDENT {incident.incident_id}
              </span>
              <span className="text-xs bg-slate-800 text-slate-300 px-2.5 py-0.5 rounded border border-slate-700">
                {incident.category}
              </span>
              <SeverityBadge severity={incident.severity} />
            </div>
            <h1 className="text-2xl font-bold text-slate-100 tracking-tight">
              {incident.title}
            </h1>
            <p className="text-xs text-slate-400 mt-2 font-mono max-w-3xl leading-relaxed">
              {incident.description}
            </p>
          </div>

          {/* Risk Score Gauge & Quick Actions */}
          <div className="flex items-center gap-4 shrink-0 bg-slate-900/80 p-4 rounded-xl border border-slate-800 font-mono">
            <div className="text-center pr-4 border-r border-slate-800">
              <div className="text-[10px] text-slate-500 uppercase font-semibold">RISK SCORE</div>
              <div className={`text-3xl font-extrabold ${
                incident.risk_score >= 80 ? 'text-rose-400' : incident.risk_score >= 60 ? 'text-orange-400' : 'text-amber-400'
              }`}>
                {incident.risk_score}<span className="text-sm font-normal text-slate-500">/100</span>
              </div>
              <div className="text-[10px] text-slate-400 font-bold mt-0.5">{incident.severity} Risk</div>
            </div>

            <div className="space-y-2">
              <button
                onClick={() => handleRunInvestigation()}
                disabled={isInvestigating}
                className="w-full px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-2 transition-all shadow-md shadow-blue-600/30 font-mono disabled:opacity-50"
              >
                {isInvestigating ? (
                  <>
                    <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                    <span>Agent Investigating...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-3.5 h-3.5 text-cyan-300" />
                    <span>Trigger AI Investigation</span>
                  </>
                )}
              </button>

              <Link
                to={`/reports/${incident.incident_id}`}
                className="w-full px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors font-mono"
              >
                <FileText className="w-3.5 h-3.5" />
                <span>Executive Report</span>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* 2. AI-Generated Summary & Risk Explanation (Section A & B) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 soc-card border-slate-800 relative">
          <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-800">
            <div className="flex items-center gap-2 font-mono text-xs font-bold text-slate-200">
              <Bot className="w-4 h-4 text-cyan-400" />
              <span>AI INVESTIGATION SUMMARY</span>
            </div>
            <div className="flex items-center gap-2 text-[10px] font-mono">
              <span className="bg-blue-500/10 border border-blue-500/30 text-cyan-300 px-2 py-0.5 rounded flex items-center gap-1">
                <Sparkles className="w-3 h-3 text-cyan-400" />
                AI-Assisted Analysis
              </span>
              <span className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-2 py-0.5 rounded">
                Evidence-backed
              </span>
            </div>
          </div>

          <div className="text-xs text-slate-300 font-mono leading-relaxed space-y-3">
            <p>
              {investigationData?.summary || incident.summary || (
                "Correlated event sequence indicates an active high-risk intrusion attempt. Click 'Trigger AI Investigation' above to execute multi-step agentic log inspection and RAG playbook retrieval."
              )}
            </p>

            {investigationData?.timeline_analysis && (
              <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800 space-y-1.5 text-[11px]">
                <div className="text-cyan-400 font-bold">Correlated Sequence Insights:</div>
                {investigationData.timeline_analysis.map((line, idx) => (
                  <div key={idx} className="flex items-start gap-2 text-slate-300">
                    <CornerDownRight className="w-3.5 h-3.5 text-slate-500 shrink-0 mt-0.5" />
                    <span>{line}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Risk Assessment Breakdown */}
        <div className="soc-card border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 pb-3 mb-3 border-b border-slate-800 font-mono text-xs font-bold text-slate-200">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>RISK SCORE COMPOSITION</span>
            </div>

            <p className="text-[11px] text-slate-400 font-mono leading-relaxed mb-4">
              {incident.risk_assessment?.explanation || (
                `Composite score calculated from event severity, multi-stage attack depth, and asset criticality.`
              )}
            </p>

            <div className="space-y-2.5 font-mono text-xs">
              <div>
                <div className="flex justify-between text-slate-400 text-[11px] mb-1">
                  <span>Severity Factor</span>
                  <span className="text-slate-200 font-bold">High / Critical</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-rose-500 h-full rounded-full" style={{ width: '85%' }} />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-slate-400 text-[11px] mb-1">
                  <span>ML Detection Confidence</span>
                  <span className="text-slate-200 font-bold">94%</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-blue-500 h-full rounded-full" style={{ width: '94%' }} />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-slate-400 text-[11px] mb-1">
                  <span>Attack Kill-Chain Stages</span>
                  <span className="text-slate-200 font-bold">{incident.attack_chain?.length || 4} Correlated</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-cyan-500 h-full rounded-full" style={{ width: '80%' }} />
                </div>
              </div>
            </div>
          </div>

          <div className="pt-3 mt-3 border-t border-slate-800 text-[10px] text-slate-500 font-mono">
            Configured Risk Model: CyberGuard Composite v1.0
          </div>
        </div>
      </div>

      {/* 3. Attack Chain & MITRE ATT&CK Mapping (Section D & G) */}
      <div className="soc-card">
        <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
          <div>
            <h2 className="text-sm font-bold font-mono text-slate-200 flex items-center gap-2">
              <Layers className="w-4 h-4 text-cyan-400" />
              ATTACK CHAIN & MITRE ATT&CK BEHAVIORAL PROGRESSION
            </h2>
            <p className="text-[11px] text-slate-400">
              Observed stage transition mapped to MITRE tactics & techniques
            </p>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30">
            Possible Mapping (Not Definitive Attribution)
          </span>
        </div>

        {/* Step-by-Step Kill Chain Flow */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
          {(incident.attack_chain || []).map((stage, idx) => (
            <div 
              key={stage.stage_id || idx}
              className="bg-slate-900/80 border border-slate-800 hover:border-slate-700 p-3.5 rounded-xl font-mono relative transition-all"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] text-slate-500 font-bold uppercase">
                  STEP 0{idx + 1}
                </span>
                <span className="text-[10px] bg-blue-500/10 text-cyan-300 border border-blue-500/30 px-1.5 py-0.5 rounded font-bold">
                  {stage.mitre_id}
                </span>
              </div>

              <div className="text-xs font-bold text-slate-100 mb-1 leading-snug">
                {stage.stage_name}
              </div>

              <div className="text-[11px] text-blue-400 font-semibold mb-2">
                {stage.tactic}
              </div>

              <p className="text-[11px] text-slate-400 leading-tight">
                {stage.evidence}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* 4. Incident Timeline & Affected Assets (Section C & E) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Timeline */}
        <div className="lg:col-span-2 soc-card">
          <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
            <h2 className="text-sm font-bold font-mono text-slate-200 flex items-center gap-2">
              <Clock className="w-4 h-4 text-blue-400" />
              INCIDENT EVENT TIMELINE
            </h2>
            <span className="text-[10px] font-mono text-slate-400">Chronological Reconstruction</span>
          </div>

          <div className="space-y-3 font-mono text-xs">
            {(incident.timeline || []).map((item, idx) => (
              <div key={idx} className="flex items-start gap-3 p-2.5 rounded-lg bg-slate-900/50 border border-slate-800/60 hover:bg-slate-900 transition-colors">
                <div className="text-[11px] text-slate-400 font-bold min-w-[70px] shrink-0 pt-0.5">
                  {item.time?.slice(11, 19) || item.time}
                </div>
                <div className="w-2 h-2 rounded-full bg-blue-500 shrink-0 mt-1.5" />
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-slate-200">{item.event_type}</span>
                    <span className={`text-[10px] px-1.5 py-0.2 rounded font-bold ${
                      item.status === 'Success' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'
                    }`}>
                      {item.status}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 mt-0.5">{item.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Affected Entities */}
        <div className="soc-card flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 pb-3 mb-4 border-b border-slate-800 font-mono text-xs font-bold text-slate-200">
              <Server className="w-4 h-4 text-cyan-400" />
              <span>AFFECTED ASSETS & ACCOUNTS</span>
            </div>

            <div className="space-y-3 font-mono text-xs">
              <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                <div className="text-[10px] text-slate-500 uppercase font-bold mb-1.5">Compromised / Impacted Assets</div>
                <div className="space-y-1.5">
                  {(incident.affected_assets || []).map((asset) => (
                    <div key={asset} className="flex items-center justify-between text-slate-200 bg-slate-800/60 px-2.5 py-1.5 rounded">
                      <span className="font-bold">{asset}</span>
                      <span className="text-[10px] text-amber-400 bg-amber-500/10 px-1.5 py-0.5 rounded">
                        Target Host
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                <div className="text-[10px] text-slate-500 uppercase font-bold mb-1.5">Targeted User Accounts</div>
                <div className="space-y-1.5">
                  {(incident.affected_users || []).map((u) => (
                    <div key={u} className="flex items-center justify-between text-slate-200 bg-slate-800/60 px-2.5 py-1.5 rounded">
                      <span className="font-bold text-cyan-300">{u}</span>
                      <span className="text-[10px] text-rose-400 bg-rose-500/10 px-1.5 py-0.5 rounded">
                        Compromised
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 font-mono text-[11px] text-slate-400">
            Scope: Confined to 2 hosts & 1 user session
          </div>
        </div>
      </div>

      {/* 5. Interactive Agentic Investigation & Q&A Panel (Section G & Agent Workflow) */}
      <div className="soc-card border-blue-500/40">
        <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
          <div>
            <h2 className="text-sm font-bold font-mono text-slate-100 flex items-center gap-2">
              <Bot className="w-4 h-4 text-cyan-400" />
              INTERACTIVE AI INVESTIGATOR & AGENT WORKBENCH
            </h2>
            <p className="text-[11px] text-slate-400">
              Query incident telemetry, evidence grounding, and RAG cybersecurity playbooks
            </p>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-cyan-300 border border-blue-500/30">
            Agentic Tools Active
          </span>
        </div>

        {/* Display Tool Executions if available */}
        {investigationData?.tool_executions && (
          <div className="mb-4 bg-slate-950 p-3 rounded-xl border border-slate-800 font-mono text-xs">
            <div className="text-[11px] text-cyan-400 font-bold mb-2 flex items-center gap-1.5">
              <Terminal className="w-3.5 h-3.5" />
              <span>AGENT TOOL EXECUTION AUDIT:</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-2">
              {investigationData.tool_executions.map((tool) => (
                <div key={tool.step} className="bg-slate-900 p-2.5 rounded border border-slate-800 text-[11px]">
                  <div className="flex justify-between items-center text-slate-400 mb-1">
                    <span className="font-bold text-slate-300">Step {tool.step}: {tool.tool_name}</span>
                    <span className="text-[10px] text-emerald-400">{tool.duration_ms}ms</span>
                  </div>
                  <div className="text-slate-400 line-clamp-2 text-[10px]">{tool.output_summary}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Chat / Q&A Assistant Stream */}
        <div className="space-y-3 font-mono text-xs mb-4">
          {chatMessages.length === 0 ? (
            <div className="p-4 bg-slate-900/40 rounded-xl border border-slate-800 text-slate-400 text-center text-xs">
              Ask specific questions regarding this incident evidence, timelines, affected systems, or mitigation playbooks.
            </div>
          ) : (
            chatMessages.map((msg, idx) => (
              <div key={idx} className={`p-3.5 rounded-xl border ${
                msg.role === 'user' 
                  ? 'bg-blue-600/10 border-blue-500/30 text-blue-200 ml-8' 
                  : 'bg-slate-900/90 border-slate-800 text-slate-200 mr-8'
              }`}>
                <div className="flex items-center gap-1.5 text-[10px] font-bold text-slate-400 mb-1">
                  {msg.role === 'user' ? <span>SOC Analyst</span> : <span className="text-cyan-400 flex items-center gap-1"><Sparkles className="w-3 h-3" /> CyberGuard AI Investigator</span>}
                </div>
                <div className="text-xs leading-relaxed">{msg.content}</div>
                {msg.grounding?.ragSources && (
                  <div className="mt-2 pt-2 border-t border-slate-800 text-[10px] text-slate-400">
                    <span className="text-cyan-400 font-semibold">Grounded RAG Sources: </span>
                    {msg.grounding.ragSources.map(s => s.source).join(', ')}
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {/* Quick Question Buttons */}
        <div className="flex flex-wrap gap-2 mb-3 font-mono text-[11px]">
          {[
            "Why was this incident classified as high risk?",
            "What evidence supports this incident?",
            "What happened first in the timeline?",
            "What defensive actions could be considered?"
          ].map((prompt, pIdx) => (
            <button
              key={pIdx}
              onClick={() => handleRunInvestigation(prompt)}
              disabled={isInvestigating}
              className="px-2.5 py-1 rounded bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 text-[11px] transition-colors disabled:opacity-50"
            >
              "{prompt}"
            </button>
          ))}
        </div>

        {/* Query Input */}
        <form 
          onSubmit={(e) => {
            e.preventDefault();
            if (chatQuery.trim()) handleRunInvestigation(chatQuery);
          }}
          className="flex gap-2 font-mono"
        >
          <input
            type="text"
            value={chatQuery}
            onChange={(e) => setChatQuery(e.target.value)}
            placeholder="Ask AI Investigator about this incident..."
            className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
          <button
            type="submit"
            disabled={isInvestigating || !chatQuery.trim()}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 transition-colors disabled:opacity-50"
          >
            <Send className="w-3.5 h-3.5" />
            <span>Ask</span>
          </button>
        </form>
      </div>

      {/* 6. AI Defensive Recommendations & Response Simulator Launch (Section H, I & J) */}
      <div className="soc-card">
        <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
          <div>
            <h2 className="text-sm font-bold font-mono text-slate-100 flex items-center gap-2">
              <Sliders className="w-4 h-4 text-emerald-400" />
              RECOMMENDED DEFENSIVE ACTIONS & SIMULATION SANDBOX
            </h2>
            <p className="text-[11px] text-slate-400">
              Policy-checked response playbooks (Requires analyst sign-off for endpoint isolation)
            </p>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
            Policy Validated
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
          {(investigationData?.recommendations || incident.recommendations || [
            { action: "REVOKE_SESSION", target: "user01", priority: "HIGH", rationale: "Invalidate compromised OAuth & Kerberos session tokens.", requires_approval: false },
            { action: "ISOLATE_ENDPOINT", target: "endpoint-03", priority: "CRITICAL", rationale: "Cut off network adapter to stop ongoing data exfiltration.", requires_approval: true },
            { action: "BLOCK_SOURCE", target: "198.51.100.42", priority: "HIGH", rationale: "Enforce boundary firewall drop rule on attacker IP.", requires_approval: false },
            { action: "INCREASE_MONITORING", target: "Subnet 10.0.4.0/24", priority: "MEDIUM", rationale: "Increase EDR process capture frequency to 100%.", requires_approval: false }
          ]).map((rec, rIdx) => (
            <div key={rIdx} className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl flex flex-col justify-between hover:border-slate-700 transition-all">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                    rec.priority === 'CRITICAL' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/30' : 'bg-orange-500/10 text-orange-400 border border-orange-500/30'
                  }`}>
                    {rec.priority}
                  </span>
                  {rec.requires_approval && (
                    <span className="text-[10px] text-amber-400 bg-amber-500/10 px-1.5 py-0.5 rounded flex items-center gap-1 border border-amber-500/30">
                      <Lock className="w-3 h-3" /> Approval Req
                    </span>
                  )}
                </div>

                <div className="text-sm font-bold text-slate-100 mb-1">{rec.action}</div>
                <div className="text-xs text-cyan-400 font-semibold mb-2">Target: {rec.target}</div>
                <p className="text-[11px] text-slate-400 leading-relaxed mb-4">{rec.rationale}</p>
              </div>

              <button
                onClick={() => handleOpenSimulation(rec)}
                className="w-full py-2 bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 border border-blue-500/40 rounded-lg text-xs font-bold flex items-center justify-center gap-1.5 transition-colors"
              >
                <Play className="w-3.5 h-3.5 text-cyan-400" />
                <span>Simulate Response</span>
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Response Simulation Modal */}
      {isSimulationModalOpen && selectedAction && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#111827] border border-slate-700 rounded-2xl w-full max-w-xl p-6 shadow-2xl font-mono text-xs">
            <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
              <div className="flex items-center gap-2 text-sm font-bold text-slate-100">
                <Sliders className="w-4 h-4 text-cyan-400" />
                <span>DEFENSIVE RESPONSE SIMULATOR</span>
              </div>
              <button 
                onClick={() => setIsSimulationModalOpen(false)}
                className="text-slate-400 hover:text-slate-200"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              {/* Simulation Safety Guarantee Banner */}
              <div className="bg-blue-500/10 border border-blue-500/30 p-3 rounded-lg flex items-center gap-2 text-cyan-300 text-xs font-semibold">
                <Lock className="w-4 h-4 text-cyan-400 shrink-0" />
                <span>Simulation Only — Actual Infrastructure Not Modified.</span>
              </div>

              {/* Action Details */}
              <div className="bg-slate-900/80 p-3.5 rounded-lg border border-slate-800 space-y-2">
                <div><span className="text-slate-500">Action:</span> <span className="text-slate-200 font-bold">{selectedAction.action}</span></div>
                <div><span className="text-slate-500">Target Host / Entity:</span> <span className="text-cyan-400 font-bold">{selectedAction.target}</span></div>
                <div><span className="text-slate-500">Rationale:</span> <span className="text-slate-300">{selectedAction.rationale}</span></div>
                <div>
                  <span className="text-slate-500">Policy Requirement:</span>{' '}
                  <span className={selectedAction.requires_approval ? 'text-amber-400 font-bold' : 'text-emerald-400 font-bold'}>
                    {selectedAction.requires_approval ? 'Human Analyst Authorization Required' : 'Standard Automated Execution Allowed'}
                  </span>
                </div>
              </div>

              {/* Human Approval Checkbox */}
              {selectedAction.requires_approval && (
                <div className="bg-slate-900/60 p-3.5 rounded-lg border border-amber-500/30 flex items-start gap-3">
                  <input
                    type="checkbox"
                    id="analystApprove"
                    checked={isApprovedByAnalyst}
                    onChange={(e) => setIsApprovedByAnalyst(e.target.checked)}
                    className="mt-0.5 w-4 h-4 rounded border-slate-700 text-blue-600 focus:ring-blue-500 bg-slate-900"
                  />
                  <label htmlFor="analystApprove" className="text-xs text-slate-300 cursor-pointer">
                    <span className="font-bold text-amber-300">Analyst Sign-off:</span> I authorize this simulated containment action and confirm policy compliance under NIST SP 800-61.
                  </label>
                </div>
              )}

              {/* Simulation Result Output */}
              {simulationResult && (
                <div className="bg-slate-950 p-4 rounded-xl border border-emerald-500/40 space-y-2">
                  <div className="flex items-center gap-2 text-emerald-400 font-bold">
                    <CheckCircle2 className="w-4 h-4" />
                    <span>SIMULATION RESULT: {simulationResult.status}</span>
                  </div>
                  <div className="text-[11px] text-slate-300 space-y-1">
                    <div>Simulation ID: <span className="text-cyan-300">{simulationResult.simulation_id}</span></div>
                    <div>Simulated Effect: <span className="text-slate-200 font-bold">{JSON.stringify(simulationResult.simulated_state_change)}</span></div>
                    <div className="text-emerald-400 text-[10px] font-bold mt-1">
                      ✓ Actual Infrastructure Modified: FALSE (Safe Academic Sandbox)
                    </div>
                  </div>
                </div>
              )}

              {/* Actions Footer */}
              <div className="pt-3 border-t border-slate-800 flex justify-end gap-2">
                <button
                  onClick={() => setIsSimulationModalOpen(false)}
                  className="px-3 py-1.5 bg-slate-800 text-slate-400 rounded"
                >
                  Close
                </button>
                <button
                  onClick={handleExecuteSimulation}
                  disabled={isSimulating || (selectedAction.requires_approval && !isApprovedByAnalyst)}
                  className="px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded font-bold transition-all shadow disabled:opacity-40"
                >
                  {isSimulating ? 'Running Simulation...' : 'Execute Simulation'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
