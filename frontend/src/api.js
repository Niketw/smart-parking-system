const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

async function http(method, path, body, signal) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
    signal,
  });
  if (!res.ok) {
    let detail = 'Request failed';
    try {
      const data = await res.json();
      detail = data?.error || JSON.stringify(data);
    } catch (err) {
      console.error('Failed to parse error response', err);
    }
    throw new Error(`${res.status} ${res.statusText}: ${detail}`);
  }
  const text = await res.text();
  return text ? JSON.parse(text) : null;
}

export const api = {
  createTicket(payload, signal) {
    return http('POST', '/api/tickets', payload, signal);
  },
  listTickets(params = {}, signal) {
    const usp = new URLSearchParams();
    if (params.isActive !== undefined) usp.set('isActive', String(params.isActive));
    if (params.licensePlate) usp.set('licensePlate', params.licensePlate);
    if (params.ticketNumber) usp.set('ticketNumber', params.ticketNumber);
    const qs = usp.toString();
    return http('GET', `/api/tickets${qs ? `?${qs}` : ''}`, undefined, signal);
  },
  searchTickets(q, signal) {
    const usp = new URLSearchParams({ q });
    return http('GET', `/api/tickets/search?${usp.toString()}`, undefined, signal);
  },
  getTicket(id, signal) {
    return http('GET', `/api/tickets/${id}`, undefined, signal);
  },
  updateTicket(id, payload, signal) {
    return http('PATCH', `/api/tickets/${id}`, payload, signal);
  },
  checkoutTicket(id, signal) {
    return http('POST', `/api/tickets/${id}/checkout`, {}, signal);
  },
};


