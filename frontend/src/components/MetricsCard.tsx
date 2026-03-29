import React, { useEffect, useState } from 'react';
import { apiClient } from '../services/api';

interface Metric {
  uptime_percentage: number;
  alerts_per_hour: number;
  average_response_time_minutes: number;
  total_incidents: number;
  active_incidents: number;
  camera_count: number;
  zone_count: number;
}

interface RiskDial {
  risk_score: number;
  severity: string;
  high_count: number;
  med_count: number;
  low_count: number;
}

export const MetricsCard: React.FC = () => {
  const [metrics, setMetrics] = useState<Metric | null>(null);
  const [risk, setRisk] = useState<RiskDial | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const metricsData = await apiClient.getMetrics('1h');
        const riskData = await apiClient.getRiskDial();
        setMetrics(metricsData);
        setRisk(riskData);
      } catch (error) {
        console.error('Error fetching metrics:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 1800000); // Update every 30 min

    return () => clearInterval(interval);
  }, []);

  if (loading || !metrics || !risk) {
    return <div className="p-4 text-center">Loading metrics...</div>;
  }

  return (
    <div className="grid grid-cols-2 gap-4 p-4">
      <div className="bg-slate-800 p-4 rounded border border-slate-700">
        <h3 className="text-sm font-semibold text-slate-300 mb-2">Risk Index</h3>
        <div className="text-4xl font-bold text-amber-500">
          {Math.round(risk.risk_score)}
        </div>
        <p className="text-xs text-slate-400 mt-1">{risk.severity}</p>
      </div>

      <div className="bg-slate-800 p-4 rounded border border-slate-700">
        <h3 className="text-sm font-semibold text-slate-300 mb-2">Active Incidents</h3>
        <div className="text-4xl font-bold text-red-500">
          {risk.high_count + risk.med_count + risk.low_count}
        </div>
        <p className="text-xs text-slate-400 mt-1">{risk.high_count} HIGH</p>
      </div>

      <div className="bg-slate-800 p-4 rounded border border-slate-700">
        <h3 className="text-sm font-semibold text-slate-300 mb-2">Uptime</h3>
        <div className="w-full bg-slate-700 rounded-full h-2 my-2">
          <div
            className="bg-blue-500 h-2 rounded-full"
            style={{ width: `${metrics.uptime_percentage}%` }}
          />
        </div>
        <p className="text-xs text-slate-400">{metrics.uptime_percentage.toFixed(1)}%</p>
      </div>

      <div className="bg-slate-800 p-4 rounded border border-slate-700">
        <h3 className="text-sm font-semibold text-slate-300 mb-2">Response Time</h3>
        <div className="text-2xl font-bold text-green-500">
          {metrics.average_response_time_minutes.toFixed(1)}m
        </div>
        <p className="text-xs text-slate-400">Average</p>
      </div>
    </div>
  );
};
