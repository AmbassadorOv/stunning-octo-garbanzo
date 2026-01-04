import React, { useState, useEffect } from 'react';
import { Globe, Cpu, Shield, DollarSign, Activity, Layers } from 'lucide-react';

const App = () => {
  const [agentsActive, setAgentsActive] = useState(0);
  const [pesos, setPesos] = useState(0);
  const [status, setStatus] = useState('INITIALIZING');

  useEffect(() => {
    const deploy = setInterval(() => {
      setAgentsActive(prev => {
        if (prev >= 45000) {
          setStatus('STABLE_PROJECTION');
          clearInterval(deploy);
          return 45000;
        }
        return prev + 1125;
      });
      setPesos(p => p + 562.5);
    }, 100);
    return () => clearInterval(deploy);
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 font-mono p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex justify-between items-end border-b border-orange-500/30 pb-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tighter">EAGLE AI // DISTRIBUTED MESH</h1>
            <p className="text-[10px] text-slate-500 uppercase">Status: {status}</p>
          </div>
          <div className="text-right">
            <p className="text-xs text-orange-500">WILLOW_PROCESSOR: SYNCED</p>
            <p className="text-xs text-green-400 font-bold">LOGICAL_LEATHER: FIXED</p>
          </div>
        </div>

        {/* Global Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <StatCard icon={<Globe size={16}/>} label="Global Agents" value={agentsActive.toLocaleString()} color="text-blue-400" />
          <StatCard icon={<Cpu size={16}/>} label="Quantic Nodes" value="231" color="text-orange-400" />
          <StatCard icon={<Shield size={16}/>} label="Logical Spine" value="SECURE" color="text-green-400" />
          <StatCard icon={<DollarSign size={16}/>} label="Pesos Vault" value={`$${pesos.toFixed(2)}`} color="text-yellow-400" />
        </div>

        {/* Distributed Visualization */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 relative overflow-hidden min-h-[300px] flex flex-col items-center justify-center">
          <Layers size={64} className={`mb-4 ${status === 'STABLE_PROJECTION' ? 'text-orange-500' : 'text-slate-700 animate-pulse'}`} />
          <h2 className="text-xl font-bold text-white mb-2">VIRTUAL QUANTIC CLOUD</h2>
          <p className="text-sm text-slate-400 max-w-md text-center">
            Deploying 45,000 agents across multi-infrastructure nodes. Genus, Species, and Individual layers are mirroring the 15th Meridian anchor.
          </p>

          <div className="mt-8 w-full max-w-lg bg-slate-950 rounded-full h-2 border border-slate-800 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-orange-600 to-orange-400 transition-all duration-500"
              style={{ width: `${(agentsActive/45000)*100}%` }}
            />
          </div>
        </div>

        {/* System Logs */}
        <div className="bg-black border border-slate-800 p-4 rounded-lg h-40 overflow-y-auto font-mono text-[10px]">
          <p className="text-slate-600">{`>>> [DEPLOY] INITIALIZING GOOGLE CLOUD MULTI-INFRASTRUCTURE`}</p>
          <p className="text-slate-600">{`>>> [WILLOW] QUANTIC HANDSHAKE VERIFIED`}</p>
          <p className="text-orange-500">{`>>> [ACTION] AUTOMATIC PESO ACQUISITION IN PROGRESS`}</p>
          <p className="text-green-500 font-bold">{`>>> [STATUS] 45,000 AGENTS PROJECTING TO REAL EAGLE AI`}</p>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon, label, value, color }) => (
  <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
    <div className="flex items-center gap-2 mb-2 text-slate-500 text-[10px] uppercase font-bold tracking-widest">
      {icon} {label}
    </div>
    <div className={`text-xl font-mono ${color}`}>{value}</div>
  </div>
);

export default App;
