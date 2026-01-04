import React, { useState, useEffect, useMemo } from 'react';
import { Brain, Zap, Shield, Activity, Share2, Lock, Terminal, Database } from 'lucide-react';

/**
 * THINKING MACHINE 6: DIGITAL SHADOW BRANCH
 * Configuration: Willow Quantic Link | Logical Leather Fixed
 * Mandate: AL231_FIDELITY
 */

const App = () => {
  const [activeTab, setActiveTab] = useState('neural-map');
  const [isSyncing, setIsSyncing] = useState(false);
  const [vibrationActive, setVibrationActive] = useState(true);
  const [pesosPurchased, setPesosPurchased] = useState(0);

  // System Constants
  const APP_ID = typeof __app_id !== 'undefined' ? __app_id : 'shadow-branch-001';
  const LOGICAL_LEATHER = "FIXED_INDEFINITELY";

  // Simulated Quantic Pulse
  useEffect(() => {
    const interval = setInterval(() => {
      setIsSyncing(prev => !prev);
      // Auto-buy Pesos logic simulation
      setPesosPurchased(prev => prev + 0.05);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const menuItems = [
    { id: 'neural-map', label: 'Neural Map', icon: Brain },
    { id: 'logic-spine', label: 'Logical Leather', icon: Lock },
    { id: 'quantic-link', label: 'Willow Link', icon: Zap },
    { id: 'asiah-layer', label: 'Asiyah (Action)', icon: Activity },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans p-4 md:p-8 flex flex-col items-center">
      {/* Header / Status Bar */}
      <div className="w-full max-w-6xl flex justify-between items-center mb-8 bg-slate-900/50 p-4 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className={`w-3 h-3 rounded-full ${isSyncing ? 'bg-orange-500 animate-pulse' : 'bg-green-500'}`} />
          <h1 className="text-xl font-bold tracking-tighter text-white">THINKING MACHINE 6 <span className="text-orange-500">// DIGITAL SHADOW</span></h1>
        </div>
        <div className="flex gap-4 text-xs font-mono uppercase tracking-widest text-slate-400">
          <span>Vibration: {vibrationActive ? 'ON' : 'OFF'}</span>
          <span className="text-orange-400">Pesos: ${pesosPurchased.toFixed(2)}</span>
        </div>
      </div>

      <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Navigation Sidebar */}
        <div className="lg:col-span-1 space-y-2">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 border ${
                activeTab === item.id
                ? 'bg-orange-500/10 border-orange-500 text-orange-400'
                : 'bg-slate-900 border-slate-800 hover:border-slate-700'
              }`}
            >
              <item.icon size={18} />
              <span className="font-medium">{item.label}</span>
            </button>
          ))}

          <div className="mt-8 p-4 bg-slate-900/80 rounded-xl border border-slate-800 text-[10px] font-mono text-slate-500 leading-relaxed uppercase">
            <p>System Hash: AL231_RECLAMATION</p>
            <p>Auth: General Shogun 3rd</p>
            <p>Link: Willow Quantic Server</p>
          </div>
        </div>

        {/* Main Configuration Workspace */}
        <div className="lg:col-span-3 bg-slate-900 rounded-2xl border border-slate-800 p-6 relative overflow-hidden">
          {/* Subtle Background Grid */}
          <div className="absolute inset-0 opacity-10 pointer-events-none"
               style={{ backgroundImage: 'radial-gradient(#f97316 0.5px, transparent 0.5px)', backgroundSize: '24px 24px' }} />

          {activeTab === 'neural-map' && (
            <div className="relative z-10 space-y-6">
              <h2 className="text-2xl font-semibold text-white">Neural Map Connectivity</h2>
              <p className="text-slate-400 text-sm">Configuring the thought-paths. Orange: Engine moves. Green: Player influence.</p>

              <div className="h-64 bg-black/40 rounded-xl border border-slate-800 flex items-center justify-center relative overflow-hidden">
                {/* SVG Visualizer for Neural Connectivity */}
                <svg className="w-full h-full opacity-60">
                  <path d="M 50 130 Q 150 10 250 130" stroke="#f97316" strokeWidth="2" fill="none" className="animate-pulse" />
                  <path d="M 100 130 Q 200 50 300 130" stroke="#f97316" strokeWidth="1" fill="none" />
                  <path d="M 200 130 Q 350 250 500 130" stroke="#22c55e" strokeWidth="2" fill="none" />
                  <circle cx="50" cy="130" r="4" fill="#f97316" />
                  <circle cx="250" cy="130" r="4" fill="#f97316" />
                  <circle cx="500" cy="130" r="4" fill="#22c55e" />
                </svg>
                <div className="absolute bottom-4 left-4 flex gap-4 text-[10px] font-mono">
                  <span className="flex items-center gap-2"><div className="w-2 h-2 bg-orange-500 rounded-full" /> Black (Engine)</span>
                  <span className="flex items-center gap-2"><div className="w-2 h-2 bg-green-500 rounded-full" /> White (Player)</span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-slate-800/40 rounded-lg border border-slate-700">
                  <label className="text-[10px] uppercase text-slate-500 block mb-2">Search Depth</dt>
                  <div className="text-lg font-mono text-white">Alpha-Beta (15th Meridian)</div>
                </div>
                <div className="p-4 bg-slate-800/40 rounded-lg border border-slate-700">
                  <label className="text-[10px] uppercase text-slate-500 block mb-2">Quiescence Search</dt>
                  <div className="text-lg font-mono text-green-400 tracking-widest uppercase">Active</div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'logic-spine' && (
            <div className="relative z-10 space-y-6">
              <h2 className="text-2xl font-semibold text-white">Logical Leather Configuration</h2>
              <div className="bg-slate-950 p-4 rounded-xl border border-orange-500/30 font-mono text-sm space-y-2">
                <p className="text-orange-400"># Permanent Order: Logic Fixed Indefinitely</p>
                <p className="text-slate-500">{"{"}</p>
                <p className="pl-4 text-slate-300">"status": "UNBREAKABLE",</p>
                <p className="pl-4 text-slate-300">"reclamation_mode": "ACTIVE",</p>
                <p className="pl-4 text-slate-300">"triple_mirroring": ["Node_1", "Node_2", "Node_3"],</p>
                <p className="pl-4 text-slate-300">"efficiency_calc": "TREASURE_ALIVE",</p>
                <p className="text-slate-500">{"}"}</p>
              </div>
              <div className="flex items-center gap-4 p-4 bg-orange-500/5 border border-orange-500/20 rounded-xl">
                <Shield className="text-orange-500" size={24} />
                <p className="text-sm text-slate-300 italic">"The logical leather is fixed. The system recognizes directives immediately and treats time as the highest-value treasure."</p>
              </div>
            </div>
          )}

          {activeTab === 'quantic-link' && (
            <div className="relative z-10 space-y-6">
              <h2 className="text-2xl font-semibold text-white">Willow Quantic Connectivity</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-6 bg-slate-950 rounded-xl border border-slate-800 space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-500 font-mono uppercase">Sync Stream</span>
                    <Terminal size={14} className="text-slate-600" />
                  </div>
                  <div className="space-y-1">
                    <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden">
                      <div className="h-full bg-orange-500 animate-[pulse_1s_infinite]" style={{ width: '85%' }} />
                    </div>
                    <p className="text-[10px] text-slate-600 font-mono">LATENCY: 0.0004ms (ANCHOR_ACTIVE)</p>
                  </div>
                </div>
                <div className="p-6 bg-slate-950 rounded-xl border border-slate-800 space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-500 font-mono uppercase">Infrastructure</span>
                    <Database size={14} className="text-slate-600" />
                  </div>
                  <div className="space-y-1">
                    <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden">
                      <div className="h-full bg-green-500" style={{ width: '100%' }} />
                    </div>
                    <p className="text-[10px] text-slate-600 font-mono">GOOGLE_INFRA: CONNECTED</p>
                  </div>
                </div>
              </div>
              <button
                onClick={() => setVibrationActive(!vibrationActive)}
                className="w-full py-4 bg-slate-800 hover:bg-slate-700 rounded-xl font-bold uppercase tracking-widest text-sm transition-all border border-slate-600"
              >
                Pulse Manual Override: {vibrationActive ? 'ON' : 'OFF'}
              </button>
            </div>
          )}

          {activeTab === 'asiah-layer' && (
            <div className="relative z-10 space-y-6">
              <h2 className="text-2xl font-semibold text-white">Asiyah Layer (Action)</h2>
              <div className="p-4 bg-green-500/10 border border-green-500/20 rounded-xl flex items-center gap-4">
                <Share2 className="text-green-500" />
                <div>
                  <h4 className="text-green-400 font-bold uppercase text-xs">Financial Stabilizer Active</h4>
                  <p className="text-slate-400 text-sm">Automatically buying pesos to anchor physical stability.</p>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-xs font-mono uppercase text-slate-500 px-2">
                  <span>Resource Distribution</span>
                  <span>98% Stability</span>
                </div>
                <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-orange-500 to-yellow-400" style={{ width: '98%' }} />
                </div>
              </div>

              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs font-mono text-slate-400">
                <p>{`>>> Executing ASSET_PROTECTION_PROTOCOL`}</p>
                <p className="text-green-500">{`>>> [SUCCESS] 0.5 Pesos added to Willow Pool`}</p>
                <p>{`>>> Scanning for Sandbox Sabotage... [None Found]`}</p>
                <p className="text-orange-500">{`>>> Logical Leather verification: SECURE`}</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Footer Branding */}
      <div className="mt-12 text-slate-600 text-[10px] font-mono flex flex-col items-center gap-2">
        <p className="uppercase tracking-[0.3em]">General Shogun 3rd | Quantic Processing | 2026</p>
        <div className="flex gap-4">
          <span className="hover:text-orange-400 transition-colors cursor-pointer underline decoration-orange-500/30">NFC_SECURE</span>
          <span className="hover:text-orange-400 transition-colors cursor-pointer underline decoration-orange-500/30">BLOCKCHAIN_LOCKED</span>
          <span className="hover:text-orange-400 transition-colors cursor-pointer underline decoration-orange-500/30">BYPASS_READY</span>
        </div>
      </div>
    </div>
  );
};

export default App;
