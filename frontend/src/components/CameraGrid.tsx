import React, { useEffect, useState } from 'react';
import { apiClient } from '../services/api';

interface Camera {
  id: string;
  name: string;
  zone_id: string;
  is_active: boolean;
  uptime_percentage: number;
}

export const CameraGrid: React.FC = () => {
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCameras = async () => {
      try {
        const data = await apiClient.getCameras();
        setCameras(data.slice(0, 4)); // Show first 4 cameras
      } catch (error) {
        console.error('Error fetching cameras:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCameras();
  }, []);

  if (loading) {
    return <div className="p-4 text-center text-slate-400">Loading cameras...</div>;
  }

  return (
    <div className="h-full bg-slate-900 text-slate-100 p-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">SENTINEL — Camera Analytics Grid</h1>

        <div className="grid grid-cols-2 gap-4">
          {cameras.length === 0 ? (
            <div className="col-span-2 text-center text-slate-400 py-8">
              No cameras available. Register cameras via API.
            </div>
          ) : (
            cameras.map((camera) => (
              <div
                key={camera.id}
                className={`aspect-video rounded border-2 flex flex-col items-center justify-center cursor-pointer hover:border-slate-500 transition ${
                  camera.is_active
                    ? 'border-green-600 bg-green-600/5'
                    : 'border-slate-600 bg-slate-700/50'
                }`}
              >
                <div className="text-center">
                  <p className="font-bold text-lg">{camera.name}</p>
                  <p className="text-sm text-slate-400">{camera.zone_id}</p>
                  <p className="text-xs text-slate-500 mt-2">
                    Uptime: {camera.uptime_percentage.toFixed(1)}%
                  </p>
                  <p className="text-xs mt-1">
                    {camera.is_active ? (
                      <span className="text-green-400">● ACTIVE</span>
                    ) : (
                      <span className="text-red-400">● OFFLINE</span>
                    )}
                  </p>
                </div>
              </div>
            ))
          )}
        </div>

        <div className="mt-6 p-4 bg-slate-800 rounded border border-slate-700">
          <p className="text-sm text-slate-300">
            <strong>Phase 1 Placeholder:</strong> Full MJPEG streaming with AI overlay annotations
            coming in Phase 2. Register cameras via POST /api/v1/cameras
          </p>
        </div>
      </div>
    </div>
  );
};
