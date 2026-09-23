import React, { useState } from 'react';
import { BookOpen, Search, Sparkles, FileText, CheckCircle2, Shield } from 'lucide-react';
import { ragAPI } from '../services/api';

export const KnowledgeSearchPage = () => {
  const [query, setQuery] = useState('Why is repeated authentication failure followed by successful login suspicious?');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setHasSearched(true);
    try {
      const res = await ragAPI.search(query, 5);
      setResults(res.data.results);
    } catch (err) {
      alert('Failed to query knowledge base');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold font-mono tracking-wide text-slate-100 flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-cyan-400" />
          RAG CYBERSECURITY KNOWLEDGE BASE EXPLORER
        </h1>
        <p className="text-xs text-slate-400 mt-0.5 font-mono">
          Vector-embedded playbooks, NIST SP 800-61 guidelines, and MITRE ATT&CK tactical matrices
        </p>
      </div>

      {/* Search Input Card */}
      <div className="soc-card p-5">
        <form onSubmit={handleSearch} className="space-y-3 font-mono">
          <label className="block text-xs text-slate-300 font-bold">
            SEMANTIC KNOWLEDGE QUERY:
          </label>
          <div className="flex gap-2">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask about attack techniques, IoCs, containment policies..."
                className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
              />
            </div>
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="px-5 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all shadow-md shadow-cyan-600/20 disabled:opacity-50"
            >
              {loading ? (
                <span>Retrieving...</span>
              ) : (
                <>
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Retrieve Knowledge</span>
                </>
              )}
            </button>
          </div>

          {/* Quick Prompts */}
          <div className="flex flex-wrap gap-2 pt-2 text-[11px] text-slate-400">
            <span>Try:</span>
            {[
              "Why is repeated authentication failure followed by successful login suspicious?",
              "What is the containment policy for endpoint isolation?",
              "How to detect high-volume data exfiltration over C2?",
              "What is T1548 Abuse Elevation Control Mechanism?"
            ].map((p, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => {
                  setQuery(p);
                }}
                className="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors"
              >
                "{p}"
              </button>
            ))}
          </div>
        </form>
      </div>

      {/* Results Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between font-mono text-xs text-slate-400">
          <span>RETRIEVED KNOWLEDGE SNIPPETS ({results.length}):</span>
          <span className="text-[10px] text-cyan-400">Sublinear TF-IDF Cosine Embedding Space</span>
        </div>

        {loading ? (
          <div className="soc-card p-12 text-center text-slate-500 font-mono text-xs">
            <div className="flex items-center justify-center gap-2">
              <div className="w-4 h-4 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin" />
              <span>Matching high-dimensional vector representations...</span>
            </div>
          </div>
        ) : results.length === 0 && hasSearched ? (
          <div className="soc-card p-8 text-center text-slate-500 font-mono text-xs">
            No relevant knowledge base chunks matched the given query threshold.
          </div>
        ) : (
          results.map((res, idx) => (
            <div key={idx} className="soc-card border-slate-800 hover:border-cyan-500/40 transition-all font-mono">
              <div className="flex items-center justify-between pb-2 mb-3 border-b border-slate-800 text-xs">
                <div className="flex items-center gap-2">
                  <FileText className="w-4 h-4 text-cyan-400" />
                  <span className="font-bold text-slate-200">{res.source}</span>
                  <span className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded">
                    {res.category}
                  </span>
                </div>
                <div className="flex items-center gap-1.5 text-emerald-400 text-xs font-bold">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Match Score: {Math.round(res.score * 100)}%</span>
                </div>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-line">
                {res.text}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
