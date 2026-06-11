/**
 * GeoPort Service - API Access Layer
 * Manages all HTTP requests to the FastAPI backend for booking, tracking, and dashboard data.
 */

export const GeoPortService = {
  apiBase: '',

  /**
   * Fetch all logistics services
   */
  async getServices() {
    const res = await fetch(`${this.apiBase}/api/services`);
    if (!res.ok) throw new Error('Failed to fetch services');
    return res.json();
  },

  /**
   * Fetch all showcase projects/case studies
   */
  async getProjects() {
    const res = await fetch(`${this.apiBase}/api/projects`);
    if (!res.ok) throw new Error('Failed to fetch showcase projects');
    return res.json();
  },

  /**
   * Fetch shipment tracking status
   */
  async getTracking(trackingNumber) {
    const res = await fetch(`${this.apiBase}/api/tracking/${trackingNumber}`);
    if (!res.ok) throw new Error('Shipment record not found');
    return res.json();
  },

  /**
   * Admin login endpoint to retrieve JWT
   */
  async login(email, password) {
    const res = await fetch(`${this.apiBase}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Incorrect credentials');
    }
    return res.json();
  },

  /**
   * Fetch consolidated admin dashboard metrics
   */
  async getDashboardStats(token) {
    const res = await fetch(`${this.apiBase}/api/dashboard/stats`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!res.ok) throw new Error('Unauthorized access');
    return res.json();
  },

  /**
   * Submit contact message
   */
  async submitContactMessage(payload) {
    const res = await fetch(`${this.apiBase}/api/contact`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed to submit message');
    return res.json();
  },

  /**
   * Submit quote request
   */
  async submitQuoteRequest(payload) {
    const res = await fetch(`${this.apiBase}/api/quotes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed to parse quote request');
    return res.json();
  },

  /**
   * Subscribe to newsletter
   */
  async subscribeNewsletter(email) {
    const res = await fetch(`${this.apiBase}/api/newsletter/subscribe`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Subscription failed');
    }
    return res.json();
  }
};

// Expose on window for runtime global access across MPA scripts
if (typeof window !== 'undefined') {
  window.GeoPortService = GeoPortService;
}

export default GeoPortService;
