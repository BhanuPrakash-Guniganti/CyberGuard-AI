import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Search, 
  Filter, 
  RefreshCw, 
  ChevronLeft, 
  ChevronRight, 
  Code, 
  X,
  AlertTriangle,
  Cpu,
  Plus
} from 'lucide-react';
import { eventsAPI } from '../services/api';
import { SeverityBadge } from '../components/common/SeverityBadge';

export const EventsPage = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [severityFilter, setSeverityFilter] = useState('All');
  const [statusFilter, setStatusFilter] = useState('All');
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [isInjectModalOpen, setIsInjectModalOpen] = useState(false);
  const [newEvent, setNewEvent] = useState({
    source_ip: '198.51.100.99',
    destination_ip: '10.0.4.15',
    username: 'test_user',
    device: 'endpoint-03',
    event_type: 'Failed Login',
    status: 'Failure',
    severity: 'High',
    port: 22,
    protocol: 'TCP',
    bytes_transferred: 1400,
    command: '',
    process_name: 'sshd'
  });

  const fetchEvents = async () => {
    setLoading(true);
    try {
      const res = await eventsAPI.list({
        search: search || undefined,
        severity: severityFilter !== 'All' ? severityFilter : undefined,
        status: statusFilter !== 'All' ? statusFilter : undefined,
        limit: 100
      });
      setEvents(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, [severityFilter, statusFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchEvents();
  };

  const handleInjectSubmit = async (e) => {
    e.preventDefault();
    try {
      await eventsAPI.ingest({
        ...newEvent,
        timestamp: new Date().toISOString()
      });
      setIsInjectModalOpen(false);
      fetchEvents();
    } catch (err) {
      alert('Failed to ingest event');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold font-mono tracking-wide text-slate-100 flex items-center gap-2">
            <Activity className="w-5 h-5 text-blue-400" />
            SECURITY EVENT EXPLORER
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Ingested network, endpoint, and authentication telemetry with live ML anomaly tagging
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsInjectModalOpen(true)}
            className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-mono font-semibold flex items-center gap-1.5 transition-colors shadow-sm"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Ingest Custom Event</span>
          </button>
          <button
            onClick={fetchEvents}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-mono flex items-center gap-1.5 transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="soc-card p-4">
        <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row gap-3 items-center">
          <div className="relative flex-1 w-full">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by IP, username, device, event type, or command..."
              className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 font-mono"
            />
          </div>

          <div className="flex items-center gap-2 w-full md:w-auto">
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 font-mono focus:outline-none focus:border-blue-500"
            >
              <option value="All">All Severities</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
              <option value="Info">Info</option>
            </select>

            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 font-mono focus:outline-none focus:border-blue-500"
            >
              <option value="All">All Statuses</option>
              <option value="Success">Success</option>
              <option value="Failure">Failure</option>
            </select>

            <button
              type="submit"
              className="px-4 py-1.5 bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 border border-blue-500/40 rounded-lg text-xs font-mono transition-colors shrink-0"
            >
              Apply Filter
            </button>
          </div>
        </form>
      </div>

      {/* Events Table */}
      <div className="soc-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/80 font-mono text-[11px] text-slate-400 uppercase border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Timestamp (UTC)</th>
                <th className="py-3 px-4">Event Type</th>
                <th className="py-3 px-4">Source IP</th>
                <th className="py-3 px-4">Dest IP / Target</th>
                <th className="py-3 px-4">User</th>
                <th className="py-3 px-4">Device</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Severity</th>
                <th className="py-3 px-4">ML Tag</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 font-mono text-xs">
              {loading && events.length === 0 ? (
                <tr>
                  <td colSpan="10" className="py-8 text-center text-slate-500">
                    <div className="flex items-center justify-center gap-2">
                      <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
                      <span>Streaming security events...</span>
                    </div>
                  </td>
                </tr>
              ) : events.length === 0 ? (
                <tr>
                  <td colSpan="10" className="py-8 text-center text-slate-500">
                    No security events matched your query.
                  </td>
                </tr>
              ) : (
                events.map((evt) => (
                  <tr key={evt.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-4 text-slate-400 text-[11px]">
                      {evt.timestamp?.slice(11, 19) || evt.timestamp}
                    </td>
                    <td className="py-3 px-4 text-slate-100 font-semibold">{evt.event_type}</td>
                    <td className="py-3 px-4 text-cyan-400">{evt.source_ip}</td>
                    <td className="py-3 px-4 text-slate-300">{evt.destination_ip || 'local'}</td>
                    <td className="py-3 px-4 text-amber-300">{evt.username}</td>
                    <td className="py-3 px-4 text-slate-300">{evt.device}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        evt.status === 'Success' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                      }`}>
                        {evt.status}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <SeverityBadge severity={evt.severity} />
                    </td>
                    <td className="py-3 px-4">
                      {evt.is_anomaly || evt.predicted_attack_type !== 'Normal' ? (
                        <span className="inline-flex items-center gap-1 text-[10px] text-rose-400 font-semibold bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/30">
                          <Cpu className="w-3 h-3" />
                          {evt.predicted_attack_type || 'Anomaly'}
                        </span>
                      ) : (
                        <span className="text-slate-500 text-[11px]">Normal</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => setSelectedEvent(evt)}
                        className="px-2 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-[11px] font-mono border border-slate-700"
                      >
                        Inspect
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Inspect Event Modal Drawer */}
      {selectedEvent && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#111827] border border-slate-700 rounded-xl w-full max-w-2xl max-h-[85vh] flex flex-col shadow-2xl">
            <div className="p-4 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2 font-mono text-sm font-bold text-slate-100">
                <Code className="w-4 h-4 text-cyan-400" />
                <span>EVENT TELEMETRY INSPECTOR: {selectedEvent.id}</span>
              </div>
              <button
                onClick={() => setSelectedEvent(null)}
                className="text-slate-400 hover:text-slate-200 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="p-5 overflow-y-auto space-y-4 font-mono text-xs">
              <div className="grid grid-cols-2 gap-3 bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                <div><span className="text-slate-500">Event ID:</span> <span className="text-slate-200">{selectedEvent.id}</span></div>
                <div><span className="text-slate-500">Timestamp:</span> <span className="text-slate-200">{selectedEvent.timestamp}</span></div>
                <div><span className="text-slate-500">Source IP:</span> <span className="text-cyan-400">{selectedEvent.source_ip}</span></div>
                <div><span className="text-slate-500">Target IP:</span> <span className="text-slate-200">{selectedEvent.destination_ip}</span></div>
                <div><span className="text-slate-500">User:</span> <span className="text-amber-300">{selectedEvent.username}</span></div>
                <div><span className="text-slate-500">Device:</span> <span className="text-slate-200">{selectedEvent.device}</span></div>
                <div><span className="text-slate-500">Bytes Out:</span> <span className="text-slate-200">{selectedEvent.bytes_transferred?.toLocaleString()} bytes</span></div>
                <div><span className="text-slate-500">Port / Protocol:</span> <span className="text-slate-200">{selectedEvent.port} / {selectedEvent.protocol}</span></div>
              </div>

              {selectedEvent.command && (
                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                  <div className="text-slate-500 mb-1 text-[11px]">EXECUTED COMMAND:</div>
                  <code className="text-rose-400 font-bold">{selectedEvent.command}</code>
                </div>
              )}

              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <div className="text-slate-500 mb-1 text-[11px]">RAW TELEMETRY JSON:</div>
                <pre className="text-slate-300 text-[11px] overflow-x-auto">
                  {JSON.stringify(selectedEvent, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Ingest Event Modal */}
      {isInjectModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#111827] border border-slate-700 rounded-xl w-full max-w-lg p-6 shadow-2xl font-mono text-xs">
            <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
              <h2 className="font-bold text-sm text-slate-100 flex items-center gap-2">
                <Plus className="w-4 h-4 text-blue-400" />
                INGEST SECURITY EVENT TO ML PIPELINE
              </h2>
              <button onClick={() => setIsInjectModalOpen(false)} className="text-slate-400 hover:text-slate-200">
                <X className="w-4 h-4" />
              </button>
            </div>
            <form onSubmit={handleInjectSubmit} className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-400 mb-1">EVENT TYPE</label>
                  <input
                    type="text"
                    value={newEvent.event_type}
                    onChange={(e) => setNewEvent({ ...newEvent, event_type: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-slate-200"
                  />
                </div>
                <div>
                  <label className="block text-slate-400 mb-1">SEVERITY</label>
                  <select
                    value={newEvent.severity}
                    onChange={(e) => setNewEvent({ ...newEvent, severity: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-slate-200"
                  >
                    <option value="Critical">Critical</option>
                    <option value="High">High</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                    <option value="Info">Info</option>
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-400 mb-1">SOURCE IP</label>
                  <input
                    type="text"
                    value={newEvent.source_ip}
                    onChange={(e) => setNewEvent({ ...newEvent, source_ip: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-slate-200"
                  />
                </div>
                <div>
                  <label className="block text-slate-400 mb-1">USERNAME</label>
                  <input
                    type="text"
                    value={newEvent.username}
                    onChange={(e) => setNewEvent({ ...newEvent, username: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-slate-200"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-400 mb-1">DEVICE</label>
                  <input
                    type="text"
                    value={newEvent.device}
                    onChange={(e) => setNewEvent({ ...newEvent, device: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-slate-200"
                  />
                </div>
                <div>
                  <label className="block text-slate-400 mb-1">STATUS</label>
                  <select
                    value={newEvent.status}
                    onChange={(e) => setNewEvent({ ...newEvent, status: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-slate-200"
                  >
                    <option value="Failure">Failure</option>
                    <option value="Success">Success</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-slate-400 mb-1">COMMAND (OPTIONAL)</label>
                <input
                  type="text"
                  value={newEvent.command}
                  onChange={(e) => setNewEvent({ ...newEvent, command: e.target.value })}
                  placeholder="e.g. sudo cat /etc/shadow"
                  className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-slate-200"
                />
              </div>
              <div className="pt-3 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setIsInjectModalOpen(false)}
                  className="px-3 py-1.5 bg-slate-800 text-slate-400 rounded"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded font-bold"
                >
                  Stream & Evaluate Event
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
