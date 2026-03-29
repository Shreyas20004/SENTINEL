import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { CommandDashboard } from './components/CommandDashboard';
import { LiveMap } from './components/LiveMap';
import { CameraGrid } from './components/CameraGrid';
import { apiClient } from './services/api';
import { wsService } from './services/websocket';
import '@fontsource/share-tech-mono';
import './index.css';

function App() {
  const [isHealthy, setIsHealthy] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        await apiClient.healthCheck();
        wsService.connect();
        setIsHealthy(true);
      } catch (error) {
        console.error('Health check failed:', error);
        setIsHealthy(false);
      } finally {
        setLoading(false);
      }
    };

    checkHealth();

    return () => {
      wsService.disconnect();
    };
  }, []);

  if (loading) {
    return (
      <div className="h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-slate-100 mb-4">SENTINEL</h1>
          <p className="text-slate-400">Connecting to backend...</p>
        </div>
      </div>
    );
  }

  if (!isHealthy) {
    return (
      <div className="h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-slate-100 mb-4">SENTINEL</h1>
          <p className="text-red-400 mb-4">Backend unavailable</p>
          <p className="text-slate-400 text-sm">
            Make sure Docker container is running:
            <br />
            <code className="bg-slate-800 p-2 inline-block mt-2">docker-compose up</code>
          </p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="h-screen flex flex-col bg-slate-900">
        {/* Navigation */}
        <nav className="bg-slate-800 border-b border-slate-700 px-6 py-3 flex items-center gap-6">
          <h1 className="text-2xl font-bold text-slate-100">SENTINEL</h1>
          <div className="flex gap-4 ml-auto">
            <Link
              to="/"
              className="text-slate-300 hover:text-slate-100 font-mono text-sm transition"
            >
              Dashboard
            </Link>
            <Link
              to="/map"
              className="text-slate-300 hover:text-slate-100 font-mono text-sm transition"
            >
              Map
            </Link>
            <Link
              to="/cameras"
              className="text-slate-300 hover:text-slate-100 font-mono text-sm transition"
            >
              Cameras
            </Link>
          </div>
          <div className="ml-4 px-3 py-1 bg-green-600 text-white text-xs rounded font-mono">
            ONLINE
          </div>
        </nav>

        {/* Routes */}
        <div className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<CommandDashboard />} />
            <Route path="/map" element={<LiveMap />} />
            <Route path="/cameras" element={<CameraGrid />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
