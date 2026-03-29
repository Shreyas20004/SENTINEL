import axios, { AxiosInstance } from 'axios';

class APIClient {
  private client: AxiosInstance;
  private baseURL: string;

  constructor(baseURL: string = import.meta.env.VITE_API_URL || 'http://localhost:8000') {
    this.baseURL = baseURL;
    this.client = axios.create({
      baseURL: `${baseURL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Incidents
  async getIncidents(region?: string, severity?: string, limit?: number) {
    const response = await this.client.get('/incidents', {
      params: { region, severity, limit: limit || 100 },
    });
    return response.data;
  }

  async getIncident(incidentId: string) {
    const response = await this.client.get(`/incidents/${incidentId}`);
    return response.data;
  }

  // Alerts
  async getAlerts(limit?: number) {
    const response = await this.client.get('/alerts', {
      params: { limit: limit || 50 },
    });
    return response.data;
  }

  async createAlert(alert: any) {
    const response = await this.client.post('/alerts', alert);
    return response.data;
  }

  // Metrics
  async getMetrics(window?: string) {
    const response = await this.client.get('/metrics', {
      params: { window: window || '1h' },
    });
    return response.data;
  }

  async getRiskDial() {
    const response = await this.client.get('/metrics/risk-dial');
    return response.data;
  }

  // Zones
  async getZones() {
    const response = await this.client.get('/zones');
    return response.data;
  }

  // Cameras
  async getCameras(zone?: string) {
    const response = await this.client.get('/cameras', {
      params: { zone },
    });
    return response.data;
  }

  async getCamera(cameraId: string) {
    const response = await this.client.get(`/cameras/${cameraId}`);
    return response.data;
  }

  // Dispatch
  async escalateDispatch(alertIds: string[]) {
    const response = await this.client.post('/dispatch/escalate', {
      alert_ids: alertIds,
    });
    return response.data;
  }

  // Reports
  async generateReport(fromDate: string, toDate: string) {
    const response = await this.client.post('/reports/generate', {
      from_date: fromDate,
      to_date: toDate,
    });
    return response.data;
  }

  // Health check
  async healthCheck() {
    const response = await axios.get(`${this.baseURL}/health`);
    return response.data;
  }
}

export const apiClient = new APIClient();
