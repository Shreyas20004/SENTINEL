.. _developer-frontend:

================
Frontend Guide
================

Deep-dive guide for React/TypeScript frontend development.

Frontend Stack
==============

- **Framework:** React 18.2 (hooks-based, concurrent rendering)
- **Language:** TypeScript 5.2 (strict mode)
- **Build Tool:** Vite 5.0 (fast bundling, HMR)
- **Styling:** Tailwind CSS 3.3 (utility-first, dark theme)
- **State:** React hooks + Context API (no Redux needed for Phase 1)
- **Routing:** React Router 6 (client-side navigation)
- **HTTP:** axios (Promise-based HTTP client)
- **Real-time:** Socket.IO (WebSocket wrapper)
- **Testing:** Vitest + React Testing Library

Project Structure
==================

.. code-block:: text

   frontend/
   ├── src/
   │   ├── main.tsx              # Entry point
   │   ├── App.tsx               # Router definition
   │   ├── index.css             # Global styles
   │   ├── config.ts             # Configuration
   │   │
   │   ├── components/
   │   │   ├── CommandDashboard.tsx
   │   │   ├── ThreatQueue.tsx
   │   │   ├── MetricsCard.tsx
   │   │   ├── CameraGrid.tsx
   │   │   └── LiveMap.tsx
   │   │
   │   ├── services/
   │   │   ├── api.ts            # axios wrapper
   │   │   └── websocket.ts      # Socket.IO wrapper
   │   │
   │   ├── hooks/
   │   │   ├── useAlerts.ts      # Real-time alerts
   │   │   ├── useMetrics.ts     # Metrics fetching
   │   │   └── useCameras.ts     # Camera status
   │   │
   │   ├── types/
   │   │   └── index.ts          # TypeScript interfaces
   │   │
   │   └── assets/
   │       └── sentinel-logo.svg
   │
   ├── public/
   │   └── index.html
   │
   ├── package.json
   ├── vite.config.ts
   ├── tsconfig.json
   └── tailwind.config.js

React Patterns Used
===================

**Functional Components with Hooks:**

.. code-block:: typescript

   import { useState, useEffect } from 'react';
   
   export const ThreatQueue: React.FC = () => {
     const [incidents, setIncidents] = useState([]);
     const [loading, setLoading] = useState(false);
     
     useEffect(() => {
       const fetchIncidents = async () => {
         setLoading(true);
         const data = await apiClient.getIncidents();
         setIncidents(data);
         setLoading(false);
       };
       
       fetchIncidents();
     }, []); // Empty dependency = run once on mount
     
     if (loading) return <div>Loading...</div>;
     
     return (
       <div>
         {incidents.map(incident => (
           <IncidentItem key={incident.id} incident={incident} />
         ))}
       </div>
     );
   };

**Custom Hooks for Logic Reuse:**

.. code-block:: typescript

   // hooks/useAlerts.ts
   import { useState, useEffect } from 'react';
   import { ws Service } from '../services/websocket';
   
   export const useAlerts = () => {
     const [alerts, setAlerts] = useState([]);
     
     useEffect(() => {
       // Subscribe to WebSocket
       wsService.on('alert', (alert) => {
         setAlerts(prev => [alert, ...prev]);
       });
       
       return () => {
         wsService.off('alert');
       };
     }, []);
     
     return alerts;
   };
   
   // Usage in component
   export const Dashboard = () => {
     const alerts = useAlerts();
     return <ThreatQueue incidents={alerts} />;
   };

**Context for Global State:**

.. code-block:: typescript

   // context/AuthContext.tsx
   import { createContext, useContext } from 'react';
   
   interface AuthContextType {
     user: User | null;
     login: (username: string, password: string) => Promise<void>;
     logout: () => void;
   }
   
   const AuthContext = createContext<AuthContextType | undefined>(undefined);
   
   export const useAuth = () => {
     const context = useContext(AuthContext);
     if (!context) throw new Error('useAuth must be in AuthProvider');
     return context;
   };

API Client Service
===================

**Located:** `src/services/api.ts`

.. code-block:: typescript

   import axios, { AxiosInstance } from 'axios';
   
   export class APIClient {
     private client: AxiosInstance;
     
     constructor(baseURL: string = import.meta.env.VITE_API_URL) {
       this.client = axios.create({ baseURL });
     }
     
     async getIncidents(
       severity?: string,
       limit: number = 100
     ): Promise<Incident[]> {
       const { data } = await this.client.get('/incidents', {
         params: { severity, limit }
       });
       return data;
     }
     
     async createIncident(payload: IncidentCreate): Promise<Incident> {
       const { data } = await this.client.post('/incidents', payload);
       return data;
     }
     
     async escalateAlert(alertIds: string[]): Promise<void> {
       await this.client.post('/dispatch/escalate', { alert_ids: alertIds });
     }
   }
   
   export const apiClient = new APIClient();

**TypeScript Interfaces:**

.. code-block:: typescript

   // types/index.ts
   export interface Incident {
     id: string;
     zone_id: string;
     incident_type: 'LOITERING' | 'CROWD_SURGE' | 'PERIMETER_BREACH';
     severity: 'LOW' | 'MED' | 'HIGH';
     status: 'OPEN' | 'INVESTIGATING' | 'RESOLVED';
     description: string;
     alert_count: number;
     detected_at: string;
     created_at: string;
   }
   
   export interface IncidentCreate {
     zone_id: string;
     incident_type: string;
     severity: string;
     description: string;
   }

WebSocket Integration
=====================

**Service Wrapper:**

.. code-block:: typescript

   import io, { Socket } from 'socket.io-client';
   
   export class WebSocketService {
     private socket: Socket | null = null;
     private reconnectAttempts = 0;
     private maxReconnectAttempts = 5;
     
     connect(url: string = import.meta.env.VITE_API_URL) {
       this.socket = io(url, {
         reconnection: true,
         reconnectionDelay: 1000,
         reconnectionDelayMax: 5000,
         reconnectionAttempts: this.maxReconnectAttempts
       });
       
       this.socket.on('connect', () => {
         console.log('Connected to WebSocket');
         this.reconnectAttempts = 0;
       });
       
       this.socket.on('disconnect', () => {
         this.reconnectAttempts++;
       });
     }
     
     on(event: string, callback: (data: any) => void) {
       this.socket?.on(event, callback);
     }
     
     off(event: string) {
       this.socket?.off(event);
     }
   }

**Usage in Component:**

.. code-block:: typescript

   export const ThreatQueue = () => {
     const [incidents, setIncidents] = useState<Incident[]>([]);
     
     useEffect(() => {
       // Fetch initial incidents
       apiClient.getIncidents().then(setIncidents);
       
       // Listen for real-time updates
       wsService.on('alert', (alert: Alert) => {
         // Add to threat queue
         setIncidents(prev => [
           { ...alert, status: 'OPEN' },
           ...prev
         ]);
       });
       
       return () => wsService.off('alert');
     }, []);
     
     return (
       <div className="space-y-2">
         {incidents.map(incident => (
           <IncidentItem key={incident.id} incident={incident} />
         ))}
       </div>
     );
   };

Styling with Tailwind
=====================

**Dark theme configuration:**

.. code-block:: javascript

   // tailwind.config.js
   module.exports = {
     darkMode: 'class',
     theme: {
       extend: {
         colors: {
           danger: '#EF4444',
           warning: '#F59E0B',
           success: '#10B981'
         }
       }
     }
   };

**Component styling example:**

.. code-block:: typescript

   export const MetricsCard = ({ metrics }) => {
     const riskColor = metrics.risk_score > 70 ? 'text-red-500' : 
                       metrics.risk_score > 45 ? 'text-yellow-500' : 
                       'text-green-500';
     
     return (
       <div className="bg-slate-900 rounded-lg p-6 border border-slate-800">
         <h3 className="text-white text-lg font-semibold mb-4">Risk Dial</h3>
         <div className={`text-4xl font-bold ${riskColor}`}>
           {metrics.risk_score.toFixed(0)}
         </div>
         <p className="text-slate-400 mt-2">{metrics.severity}</p>
       </div>
     );
   };

Performance Optimization
=========================

**Memoization (prevent unnecessary re-renders):**

.. code-block:: typescript

   import { memo } from 'react';
   
   const IncidentItem = memo(({ incident } => {
     return <div>{incident.type}</div>;
   });

**Code splitting (lazy loading):**

.. code-block:: typescript

   import { lazy, Suspense } from 'react';
   
   const LiveMap = lazy(() => import('./LiveMap'));
   
   export const App = () => {
     return (
       <Suspense fallback={<div>Loading map...</div>}>
         <Routes>
           <Route path="/map" element={<LiveMap />} />
         </Routes>
       </Suspense>
     );
   };

**Polling optimization:**

.. code-block:: typescript

   const POLLING_INTERVAL = 5000; // 5 seconds
   
   useEffect(() => {
     const timer = setInterval(() => {
       apiClient.getIncidents().then(setIncidents);
     }, POLLING_INTERVAL);
     
     return () => clearInterval(timer);
   }, []);

Testing React Components
========================

**Example test:**

.. code-block:: typescript

   import { render, screen, waitFor } from '@testing-library/react';
   import { vi } from 'vitest';
   import ThreatQueue from './ThreatQueue';
   
   vi.mock('../services/api');
   
   test('displays incidents in severity order', async () => {
     const mockIncidents = [
       { id: '1', severity: 'MED' },
       { id: '2', severity: 'HIGH' }
     ];
     
     vi.mocked(apiClient.getIncidents).mockResolvedValue(mockIncidents);
     
     render(<ThreatQueue />);
     
     await waitFor(() => {
       const items = screen.getAllByRole('listitem');
       expect(items[0]).toHaveTextContent('HIGH');
     });
   });

Type Safety
===========

**Strict TypeScript configuration (`tsconfig.json`):**

.. code-block:: json

   {
     "compilerOptions": {
       "strict": true,
       "noImplicitAny": true,
       "strictNullChecks": true,
       "strictFunctionTypes": true,
       "noUnusedLocals": true,
       "noUnusedParameters": true
     }
   }

Prevents:
- Implicit `any` types
- Null/undefined errors
- Type mismatches
- Unused variables

Accessibility (A11y)
====================

**ARIA labels:**

.. code-block:: typescript

   <button
     aria-label="Escalate threat"
     className="..."
     onClick={handleEscalate}
   >
     <EscalateIcon />
   </button>

**Keyboard navigation:**

.. code-block:: typescript

   const handleKeydown = (e: React.KeyboardEvent) => {
     if (e.key === 'E') {
       handleEscalate();
     }
   };

Next Steps
==========

→ See :ref:`developer-testing` for component testing

→ Check :ref:`developer-setup` for environment setup

--------

**Last Updated:** March 29, 2026
