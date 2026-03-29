import React, { useEffect, useState } from 'react';
import { apiClient } from '../services/api';
import { wsService } from '../services/websocket';

interface Incident {
  id: string;
  incident_type: string;
  zone_id: string;
  severity: string;
  created_at: string;
  alert_count: number;
}

export const ThreatQueue: React.FC = () => {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        const data = await apiClient.getIncidents(undefined, undefined, 50);
        setIncidents(data);
      } catch (error) {
        console.error('Error fetching incidents:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchIncidents();

    // Subscribe to real-time updates via WebSocket
    const handleNewAlert = (alert: any) => {
      console.log('New alert received:', alert);
      fetchIncidents();
    };

    wsService.on('alert', handleNewAlert);

    return () => {
      wsService.off('alert', handleNewAlert);
    };
  }, []);

  if (loading) {
    return <div className="p-4 text-center text-slate-400">Loading incidents...</div>;
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'HIGH':
        return 'border-l-red-500 bg-red-500/10';
      case 'MED':
        return 'border-l-amber-500 bg-amber-500/10';
      case 'LOW':
        return 'border-l-green-500 bg-green-500/10';
      default:
        return 'border-l-slate-500 bg-slate-500/10';
    }
  };

  return (
    <div className="flex flex-col gap-2 max-h-96 overflow-y-auto">
      {incidents.length === 0 ? (
        <div className="p-4 text-center text-slate-400">No incidents</div>
      ) : (
        incidents.map((incident) => (
          <div
            key={incident.id}
            className={`p-3 rounded border-l-4 cursor-pointer hover:bg-slate-700 transition ${getSeverityColor(
              incident.severity
            )}`}
          >
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm font-semibold text-slate-100">
                  {incident.incident_type}
                </p>
                <p className="text-xs text-slate-400">{incident.zone_id}</p>
              </div>
              <span className={`text-xs font-bold px-2 py-1 rounded ${
                incident.severity === 'HIGH'
                  ? 'bg-red-600 text-white'
                  : incident.severity === 'MED'
                  ? 'bg-amber-600 text-white'
                  : 'bg-green-600 text-white'
              }`}>
                {incident.severity}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-2">
              {incident.alert_count} alerts
            </p>
          </div>
        ))
      )}
    </div>
  );
};
