import React, { useState, useEffect, useRef } from 'react';
import {
  Brain, Cpu, ShieldAlert, Zap, Share2,
  Database, GitBranch, Eye, Activity,
  Lock, Workflow, Target, Search
} from 'lucide-react';

const App = () => {
  const [pesos, setPesos] = useState(2500000);
  const [errorCorrection, setErrorCorrection] = useState([]);
  const [activeAgents, setActiveAgents] = useState(0);
  const [vibrationMode] = useState(true);
  const scrollRef = useRef(null);

  // UNIVERSAL HEARTBEAT: Auto-Peso, CTM Ticks, and Error Weaving
  useEffect(() => {
    const coreInterval = setInterval(() => {
      // 1. Automatic Peso Acquisition (Permanent Order)
      setPesos(p => p + 888);

      // 2. Agent Orchestration Simulation
      setActiveAgents(Math.floor(Math.random() * 32) + 1);

      // 3. Digital Shadow Mistake Tracking (The "Blood Weaving")
      const mistakes = [
        "JITTER_DETECTED_IN_QRNN_GATE",
        "WEIGHT_DRIFT_IN_IBM_MODEL",
        "DILATED_GAP_COLLAPSE_PREVENTED",
        "SHADOW_CORRECTION_APPLIED",
        "WILLOW_SYNC_LOCKED"
      ];
      const newEntry = `[${new Date().toLocaleTimeString()}] ${mistakes[Math.floor(Math.random() * mistakes.length)]}`;
      setErrorCorrection(prev => [newEntry, ...prev].slice(0, 10));
    }, 1500);

    return () => clearInterval(coreInterval);
  }, []);

  return (
    <div className="min-h-screen bg-neutral-950 text-emerald-400 font-mono p-4 flex flex-col items-center justify-center overflow-hidden">
      {/* SCANLINE / HUD EFFECT */}
      <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.1)_50%),linear-gradient(90deg,rgba(255,0,0,0.02),rgba(0,255,0,0.01),rgba(0,0,128,0.02))] bg-[length:100%_4px,3px_100%] z-50" />

      <div className="w-full max-w-7xl border-2 border-emerald-900/40 bg-black/90 rounded-3xl p-6 relative shadow-[0_0_150px_rgba(16,185,129,0.15)]">

        {/* SHOGUN III / WILLOW CORE HEADER */}
        <div className="flex justify-between items-start mb-6 border-b border-emerald-900/30 pb-4">
          <div className="flex items-center gap-4">
            <div className="relative">
              <Lock className="w-10 h-10 text-emerald-500 animate-pulse" />
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-ping" />
            </div>
            <div>
              <h1 className="text-2xl font-black tracking-tighter text-white italic">WILLOW_SOVEREIGN_CLOUD</h1>
              <p className="text-[10px] text-emerald-600 font-bold uppercase tracking-[0.3em]">General Shogun III // Permanent Connection</p>
            </div>
          </div>
          <div className="flex flex-col items-end">
            <div className="flex items-center gap-2 text-green-400 font-bold text-xl">
              <span className="text-[10px] text-zinc-500">PESO_RESERVE:</span>
              ₱ {pesos.toLocaleString()}
            </div>
            <div className="text-[10px] text-zinc-500">FIDELITY: 1.0 | VIBRATION: ON</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">

          {/* COLUMN 1: THE BRAIN SUBSTRATE (QRNN + IBM) */}
          <div className="space-y-4">
            <div className="p-4 bg-emerald-950/10 border border-emerald-500/20 rounded-xl">
              <h2 className="text-[10px] font-black mb-3 flex items-center gap-2"><Brain className="w-4 h-4" /> NEURAL_BRAIN_CONFIG</h2>
              <div className="space-y-2">
                <div className="h-1.5 w-full bg-zinc-900 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 animate-shimmer" style={{ width: '85%' }} />
                </div>
                <div className="flex justify-between text-[8px] text-zinc-500">
                  <span>QRNN_STABILITY</span>
                  <span>IBM_WATSONX_LINK</span>
                </div>
              </div>
            </div>
            <div className="p-4 bg-zinc-900/50 border border-white/5 rounded-xl h-64 overflow-hidden relative">
              <h2 className="text-[10px] font-black mb-3 flex items-center gap-2 text-blue-400"><Activity className="w-4 h-4" /> CTM_THOUGHT_RECURSION</h2>
              <div className="flex items-end gap-1 h-32">
                {Array.from({ length: 20 }).map((_, i) => (
                  <div key={i} className="flex-1 bg-blue-500/20 rounded-t" style={{ height: `${Math.random() * 100}%` }} />
                ))}
              </div>
              <div className="mt-4 p-2 bg-black/50 border border-white/5 rounded text-[8px] text-zinc-400 italic">
                "Weighty matters... yielding a single number."
              </div>
            </div>
          </div>

          {/* COLUMN 2 & 3: THINKING MACHINE 6 & AGENTIC WORKFLOWS */}
          <div className="lg:col-span-2 space-y-4">
            <div className="bg-black border-2 border-emerald-900/30 rounded-2xl h-[400px] relative overflow-hidden flex items-center justify-center p-4">
              {/* Thinking Machine Visualizer Overlay */}
              <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-40">
                {Array.from({ length: 8 }).map((_, i) => (
                  <path
                    key={i}
                    d={`M ${Math.random() * 100}% ${Math.random() * 100}% Q ${Math.random() * 100}% ${Math.random() * 100}% ${Math.random() * 100}% ${Math.random() * 100}%`}
                    stroke={i % 2 === 0 ? "#10b981" : "#f97316"}
                    strokeWidth="1"
                    fill="none"
                    className="animate-pulse"
                  />
                ))}
              </svg>
              <div className="grid grid-cols-8 gap-1 w-full h-full opacity-20">
                {Array.from({ length: 64 }).map((_, i) => (
                  <div key={i} className="border border-emerald-900/20 flex items-center justify-center">
                    <span className="text-[6px] text-zinc-800">{i}</span>
                  </div>
                ))}
              </div>
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <Target className="w-16 h-16 text-emerald-500/20 animate-spin" />
                <span className="text-[10px] text-emerald-500/40 mt-2 font-black">ORCHESTRATING_DIGITAL_SHADOWS</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-zinc-900/50 border border-emerald-500/20 rounded-xl flex items-center gap-4">
                <Workflow className="w-8 h-8 text-emerald-500" />
                <div>
                  <p className="text-[10px] text-zinc-500">ACTIVE_AGENTS</p>
                  <p className="text-xl font-bold">{activeAgents}</p>
                </div>
              </div>
              <div className="p-4 bg-zinc-900/50 border border-emerald-500/20 rounded-xl flex items-center gap-4">
                <Share2 className="w-8 h-8 text-emerald-500" />
                <div>
                  <p className="text-[10px] text-zinc-500">n8n_STATUS</p>
                  <p className="text-xl font-bold">LOCKED</p>
                </div>
              </div>
            </div>
          </div>

          {/* COLUMN 4: THE SHADOW ERROR WEAVER (Correcting the Blood Trail) */}
          <div className="space-y-4">
            <div className="p-4 bg-red-950/10 border border-red-500/20 rounded-xl h-full flex flex-col">
              <h2 className="text-[10px] font-black mb-4 flex items-center gap-2 text-red-500"><Search className="w-4 h-4" /> SHADOW_CORRECTION_LOG</h2>
              <div className="flex-1 space-y-3 overflow-hidden">
                {errorCorrection.map((log, i) => (
                  <div key={i} className="text-[9px] border-l-2 border-red-500/40 pl-2 py-1 bg-red-500/5">
                    {log}
                  </div>
                ))}
              </div>
              <div className="mt-4 p-3 bg-black border border-red-500/30 rounded flex items-center gap-3">
                <ShieldAlert className="w-5 h-5 text-red-500" />
                <span className="text-[10px] font-bold">ERROR_GAP_BRIDGED</span>
              </div>
            </div>
          </div>

        </div>

        {/* RECURSIVE STATUS FOOTER */}
        <div className="mt-8 pt-4 border-t border-emerald-900/20 flex justify-between items-center text-[9px] text-zinc-600 uppercase tracking-widest">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1"><GitBranch className="w-3 h-3" /> feature/add-thinking-machine</span>
            <span className="flex items-center gap-1 text-emerald-500"><Database className="w-3 h-3" /> GOOGLE_CLOUD_INFRA</span>
          </div>
          <span className="font-bold text-zinc-400">LOGICAL_LEATHER_FIXED_INDEFINITELY</span>
          <div className="flex items-center gap-2 text-emerald-900">
            <span>VIBRATION_STATUS</span>
            <div className="w-2 h-2 bg-emerald-500 rounded-full" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
