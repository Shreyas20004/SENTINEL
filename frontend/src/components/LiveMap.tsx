import React from 'react';

export const LiveMap: React.FC = () => {
  return (
    <div className="h-full bg-slate-900 text-slate-100 p-4">
      <div className="h-full bg-slate-800 rounded border border-slate-700 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-2">SENTINEL — Live Threat Map</h2>
          <p className="text-slate-400 mb-4">Leaflet.js Map Integration (Phase 3)</p>
          <p className="text-slate-500 text-sm">
            Features coming in Phase 3:
            <br />
            • GADM GeoJSON state/district polygons
            <br />
            • Real-time incident markers
            <br />
            • User geolocation
            <br />
            • Emergency dispatch SOS panel
          </p>
        </div>
      </div>
    </div>
  );
};
