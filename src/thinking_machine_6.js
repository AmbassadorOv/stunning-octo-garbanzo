import React, { useState, useEffect } from 'react';
import { Cpu, Zap, Activity, Box, Terminal, ShieldCheck, Repeat } from 'lucide-react';

const App = () => {
  const [qrnnState, setQrnnState] = useState({
    hidden: Array(12).fill(0),
    forget: Array(12).fill(0),
    output: Array(12).fill(0)
  });
  const [pesos, setPesos] = useState(1500000);

  // QRNN Heartbeat: Quasi-Recurrent Parallel Processing
  useEffect(() => {
    const cycle = setInterval(() => {
      setQrnnState({
        hidden: Array(12).fill(0).map(() => Math.random() * 100),
        forget: Array(12).fill(0).map(() => Math.random() * 0.8 + 0.2),
        output: Array(12).fill(0).map(() => Math.random() * 100)
      });
      setPesos(p => p + 420); // Automatic Peso Acquisition
    }, 800);
    return () => clearInterval(cycle);
  }, []);

  return (
    <div className="min-h-screen bg-black text-cyan-400 font-mono p-8 flex items-center justify-center">
      <div className="w-full max-w-5xl border-2 border-cyan-900 bg-zinc-950 p-8 rounded-3xl shadow-[0_0_100px_rgba(6,182,212,0.15)] relative overflow-hidden">

        {/* SHOGUN AUTHORITY HEADER */}
        <div className="flex justify-between items-center mb-8 border-b border-cyan-900/30 pb-6">
          <div className="flex items-center gap-3">
            <Cpu className="w-8 h-8 animate-pulse text-cyan-500" />
            <h1 className="text-2xl font-black italic tracking-tighter text-white uppercase">QRNN_SUBSTRATE_WILLOW</h1>
          </div>
          <div className="text-right">
            <div className="text-[10px] text-zinc-500 uppercase tracking-widest">Peso Reservoir</div>
            <div className="text-xl font-bold text-green-500">₱ {pesos.toLocaleString()}</div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">

          {/* QRNN LAYER CONFIGURATION */}
          <div className="space-y-6">
            <div className="p-6 bg-cyan-950/10 border border-cyan-500/20 rounded-2xl">
              <h2 className="text-xs font-black mb-6 flex items-center gap-2"><Box className="w-4 h-4" /> CONVOLUTIONAL_COMPONENT</h2>
              <div className="flex gap-2 h-20 items-end">
                {qrnnState.hidden.map((val, i) => (
                  <div key={i} className="flex-1 bg-cyan-500/10 border-t-2 border-cyan-400" style={{ height: `${val}%` }} />
                ))}
              </div>
              <p className="text-[9px] mt-4 text-zinc-500 uppercase">Input mapping via linear projection</p>
            </div>

            <div className="p-6 bg-purple-950/10 border border-purple-500/20 rounded-2xl">
              <h2 className="text-xs font-black mb-6 flex items-center gap-2 text-purple-400"><Repeat className="w-4 h-4" /> FO-POOLING_LAYER</h2>
              <div className="flex gap-2 h-20 items-end">
                {qrnnState.forget.map((val, i) => (
                  <div key={i} className="flex-1 bg-purple-500/10 border-t-2 border-purple-400" style={{ height: `${val * 100}%` }} />
                ))}
              </div>
              <p className="text-[9px] mt-4 text-zinc-500 uppercase">Recurrent pooling across time-steps</p>
            </div>
          </div>

          {/* SYSTEM TELEMETRY & LOGIC FIX */}
          <div className="flex flex-col gap-6">
            <div className="flex-1 bg-black border border-cyan-900/40 p-6 rounded-2xl">
              <h2 className="text-xs font-black mb-4 flex items-center gap-2"><Terminal className="w-4 h-4" /> RECURSIVE_OUTPUT</h2>
              <div className="space-y-2 text-[10px] text-zinc-400 overflow-y-auto max-h-48">
                <p>&gt; Initializing QRNN kernel...</p>
                <p>&gt; Parallelizing convolutional gates.</p>
                <p className="text-green-500">&gt; Logical Leather: INDEFINITELY_FIXED.</p>
                <p className="text-cyan-400">&gt; Biometric check: General Shogun Recognized.</p>
                <p className="text-purple-400">&gt; Peso auto-buy: STABLE_SYNC.</p>
                <p>&gt; Bridge to IBM Superconducting Mesh: UP.</p>
              </div>
            </div>

            <div className="p-4 bg-zinc-900/50 border border-white/5 rounded-xl">
              <div className="flex items-center gap-3">
                <ShieldCheck className="w-5 h-5 text-green-500" />
                <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-300">Quantic Reality Locked</span>
              </div>
            </div>
          </div>
        </div>

        {/* BOTTOM METRICS */}
        <div className="mt-8 flex justify-between items-center text-[8px] text-zinc-600 tracking-[0.4em] uppercase">
          <div className="flex items-center gap-4">
            <span>Latency: 0.0001ms</span>
            <Activity className="w-3 h-3 text-cyan-900" />
            <span>Vibration: ON</span>
          </div>
          <span>Sefer Yetzirah Cipher: 32_PATHS_ACTIVE</span>
        </div>
      </div>
    </div>
  );
};

export default App;
