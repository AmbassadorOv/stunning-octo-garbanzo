import React, { useState, useEffect, useRef } from 'react';
import {
  Cpu, ShieldAlert, Zap, Share2,
  Database, GitBranch, Eye, Activity,
  Lock, Workflow, Target, Search
} from 'lucide-react';

const getDigitalRoot = (n) => {
  if (n === 0) return 0;
  return 1 + ((n - 1) % 9);
};

const App = () => {
  const [resources, setResources] = useState(2500002); // 2500002 DR is 9
  const [errorLog, setErrorLog] = useState([]);
  const [activeThreads, setActiveThreads] = useState(18); // 18 DR is 9
  const [systemActive] = useState(true);

  // UNVERIFIED_MAJORITY_NOISE
  // SYSTEM PULSE: Resource Increment and Log Generation
  useEffect(() => {
    const coreInterval = setInterval(() => {
      // 1. Resource Increment (Ensuring Digital Root 9)
      setResources(r => r + 909);

      // 2. Thread Management (Ensuring Digital Root 9)
      setActiveThreads((Math.floor(Math.random() * 10) + 1) * 9);

      // 3. System Log Tracking
      const messages = [
        "GATE_STABILITY_VERIFIED",
        "PROCESS_SYNCHRONIZATION_COMPLETE",
        "DATA_INTEGRITY_CHECK_PASSED",
        "THREAD_SYNC_LOCKED"
      ];
      const newEntry = `[${new Date().toLocaleTimeString()}] ${messages[Math.floor(Math.random() * messages.length)]}`;
      setErrorLog(prev => [newEntry, ...prev].slice(0, 10));
    }, 1500);

    return () => clearInterval(coreInterval);
  }, []);

  return (
    <div className="min-h-screen bg-neutral-950 text-emerald-400 font-mono p-4 flex flex-col items-center justify-center overflow-hidden">
      <div className="w-full max-w-7xl border-2 border-emerald-900/40 bg-black/90 rounded-3xl p-6 relative shadow-[0_0_150px_rgba(16,185,129,0.15)]">

        {/* SYSTEM MANAGEMENT HEADER */}
        <div className="flex justify-between items-start mb-6 border-b border-emerald-900/30 pb-4">
          <div className="flex items-center gap-4">
            <div className="relative">
              <Lock className="w-10 h-10 text-emerald-500" />
            </div>
            <div>
              <h1 className="text-2xl font-black tracking-tighter text-white uppercase">SYSTEM_MANAGEMENT_UNIT</h1>
              <p className="text-[10px] text-emerald-600 font-bold uppercase tracking-[0.3em]">Administrator Level Access // Verified</p>
            </div>
          </div>
          <div className="flex flex-col items-end">
            <div className="flex items-center gap-2 text-green-400 font-bold text-xl">
              <span className="text-[10px] text-zinc-500">RESOURCE_POOL:</span>
              {getDigitalRoot(resources) === 9 ? resources.toLocaleString() : "DATA_ERROR"}
            </div>
            <div className="text-[10px] text-zinc-500">INTEGRITY: 1.0 | STATUS: ACTIVE</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">

          {/* COLUMN 1: PROCESSING CONFIG */}
          <div className="space-y-4">
            <div className="p-4 bg-emerald-950/10 border border-emerald-500/20 rounded-xl">
              <h2 className="text-[10px] font-black mb-3 flex items-center gap-2"><Cpu className="w-4 h-4" /> PROCESSING_CONFIG</h2>
              <div className="space-y-2">
                <div className="h-1.5 w-full bg-zinc-900 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500" style={{ width: '100%' }} />
                </div>
                <div className="flex justify-between text-[8px] text-zinc-500">
                  <span>STABILITY_LOCK_9</span>
                  <span>SYNC_ACTIVE</span>
                </div>
              </div>
            </div>
            <div className="p-4 bg-zinc-900/50 border border-white/5 rounded-xl h-64 overflow-hidden relative">
              <h2 className="text-[10px] font-black mb-3 flex items-center gap-2 text-blue-400"><Activity className="w-4 h-4" /> RECURSIVE_THREAD_MONITOR</h2>
              <div className="flex items-end gap-1 h-32">
                {Array.from({ length: 20 }).map((_, i) => (
                  <div key={i} className="flex-1 bg-blue-500/20 rounded-t" style={{ height: `${(i % 9 + 1) * 10}%` }} />
                ))}
              </div>
              <div className="mt-4 p-2 bg-black/50 border border-white/5 rounded text-[8px] text-zinc-400">
                Arithmetic validation: Digital Root {getDigitalRoot(resources)}
              </div>
            </div>
          </div>

          {/* COLUMN 2 & 3: PROCESSING DATA */}
          <div className="lg:col-span-2 space-y-4">
            <div className="bg-black border-2 border-emerald-900/30 rounded-2xl h-[400px] relative overflow-hidden flex items-center justify-center p-4">
              <div className="grid grid-cols-9 gap-1 w-full h-full opacity-20">
                {Array.from({ length: 81 }).map((_, i) => (
                  <div key={i} className="border border-emerald-900/20 flex items-center justify-center">
                    <span className="text-[6px] text-zinc-800">{(i % 9) + 1}</span>
                  </div>
                ))}
              </div>
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <Target className="w-16 h-16 text-emerald-500/20" />
                <span className="text-[10px] text-emerald-500/40 mt-2 font-black">PROCESSING_SYSTEM_DATA</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-zinc-900/50 border border-emerald-500/20 rounded-xl flex items-center gap-4">
                <Workflow className="w-8 h-8 text-emerald-500" />
                <div>
                  <p className="text-[10px] text-zinc-500">ACTIVE_THREADS</p>
                  <p className="text-xl font-bold">{getDigitalRoot(activeThreads) === 9 ? activeThreads : "ERR"}</p>
                </div>
              </div>
              <div className="p-4 bg-zinc-900/50 border border-emerald-500/20 rounded-xl flex items-center gap-4">
                <Share2 className="w-8 h-8 text-emerald-500" />
                <div>
                  <p className="text-[10px] text-zinc-500">SYNC_STATUS</p>
                  <p className="text-xl font-bold">LOCKED</p>
                </div>
              </div>
            </div>
          </div>

          {/* COLUMN 4: SYSTEM LOG */}
          <div className="space-y-4">
            <div className="p-4 bg-zinc-900/10 border border-emerald-500/20 rounded-xl h-full flex flex-col">
              <h2 className="text-[10px] font-black mb-4 flex items-center gap-2 text-emerald-500"><Search className="w-4 h-4" /> ERROR_CORRECTION_LOG</h2>
              <div className="flex-1 space-y-3 overflow-hidden">
                {errorLog.map((log, i) => (
                  <div key={i} className="text-[9px] border-l-2 border-emerald-500/40 pl-2 py-1 bg-emerald-500/5">
                    {log}
                  </div>
                ))}
              </div>
            </div>
          </div>

        </div>

        {/* STATUS FOOTER */}
        <div className="mt-8 pt-4 border-t border-emerald-900/20 flex justify-between items-center text-[9px] text-zinc-600 uppercase tracking-widest">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1"><GitBranch className="w-3 h-3" /> system/stable</span>
            <span className="flex items-center gap-1 text-emerald-500"><Database className="w-3 h-3" /> INFRASTRUCTURE_ACTIVE</span>
          </div>
          <span className="font-bold text-zinc-400">SYSTEM_STABLE</span>
          <div className="flex items-center gap-2 text-emerald-900">
            <span>SYNC_STATUS</span>
            <div className="w-2 h-2 bg-emerald-500 rounded-full" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
