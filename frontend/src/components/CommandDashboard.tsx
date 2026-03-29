import { useState } from 'react';
import { ThreatQueue } from './ThreatQueue';
import { MetricsCard } from './MetricsCard';
import { apiClient } from '../services/api';

export const CommandDashboard: React.FC = () => {
  const [escalating, setEscalating] = useState(false);

  const handleEscalate = async () => {
    setEscalating(true);
    try {
      // Get HIGH severity incidents and escalate
      const incidents = await apiClient.getIncidents(undefined, 'HIGH');
      if (incidents.length > 0) {
        await apiClient.escalateDispatch(
          incidents.slice(0, 5).map((i: any) => i.id)
        );
        alert('Escalation sent to supervisor');
      }
    } catch (error) {
      console.error('Error escalating:', error);
      alert('Failed to escalate');
    } finally {
      setEscalating(false);
    }
  };

  return (
    <div className="h-full bg-slate-900 text-slate-100 p-4 overflow-auto">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold">SENTINEL — Command Dashboard</h1>
          <p className="text-slate-400 text-sm mt-1">Real-Time Threat Detection & Response</p>
        </div>

        {/* Two-row layout */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          {/* Left: Threat Queue */}
          <div className="col-span-1 bg-slate-800 rounded border border-slate-700 p-4">
            <h2 className="text-lg font-semibold mb-4">THREAT QUEUE</h2>
            <ThreatQueue />
          </div>

          {/* Right: Metrics */}
          <div className="col-span-2">
            <MetricsCard />
          </div>
        </div>

        {/* Zone Grid (Placeholder) */}
        <div className="bg-slate-800 rounded border border-slate-700 p-4 mb-6">
          <h2 className="text-lg font-semibold mb-4">ZONE RISK MAP</h2>
          <div className="grid grid-cols-6 gap-2">
            {Array.from({ length: 6 }).map((_, i) => (
              <div
                key={i}
                className="aspect-square bg-slate-700 rounded flex items-center justify-center text-xs text-slate-400 hover:bg-slate-600 cursor-pointer"
              >
                Zone {i + 1}
              </div>
            ))}
          </div>
        </div>

        {/* Camera Grid (Placeholder) */}
        <div className="bg-slate-800 rounded border border-slate-700 p-4 mb-6">
          <h2 className="text-lg font-semibold mb-4">CAMERA STATUS</h2>
          <div className="grid grid-cols-4 gap-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <div
                key={i}
                className="aspect-video bg-slate-700 rounded border-2 border-slate-600 flex items-center justify-center text-sm text-slate-400"
              >
                CAM-{String(i + 1).padStart(2, '0')}
              </div>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          <button
            onClick={handleEscalate}
            disabled={escalating}
            className="px-6 py-2 bg-red-600 hover:bg-red-700 disabled:bg-slate-600 rounded font-semibold transition"
          >
            {escalating ? 'Escalating...' : 'Escalate HIGH'}
          </button>
          <button className="px-6 py-2 bg-slate-700 hover:bg-slate-600 rounded font-semibold transition">
            Export Report
          </button>
        </div>
      </div>
    </div>
  );
};
