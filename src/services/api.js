// API service layer for communicating with Flask backend
const API_BASE = import.meta.env.VITE_API_URL || '/api'

/**
 * Generic fetch wrapper with auth headers
 */
async function apiFetch(endpoint, options = {}) {
  const { supabase } = await import('./supabase.js')
  const { data: { session } } = await supabase.auth.getSession()
  
  const headers = {
    'Content-Type': 'application/json',
    ...(session?.access_token && { 'Authorization': `Bearer ${session.access_token}` }),
    ...options.headers
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Request failed' }))
    throw new Error(error.message || `HTTP ${response.status}`)
  }

  return response.json()
}

// ─── Auth & Profile ───────────────────────────────────────
export const profileApi = {
  get: () => apiFetch('/profile'),
  update: (data) => apiFetch('/profile', { method: 'PUT', body: JSON.stringify(data) }),
  getPartner: () => apiFetch('/profile/partner'),
  linkPartner: (code) => apiFetch('/partner/link', { method: 'POST', body: JSON.stringify({ code }) }),
}

// ─── Questions ────────────────────────────────────────────
export const questionsApi = {
  getCategories: () => apiFetch('/questions/categories'),
  getRandom: (category) => apiFetch(`/questions/random?category=${category}`),
  getToday: () => apiFetch('/questions/today'),
  answer: (questionId, answer) => apiFetch('/questions/answer', { method: 'POST', body: JSON.stringify({ questionId, answer }) }),
  getHistory: (page = 1) => apiFetch(`/questions/history?page=${page}`),
}

// ─── Selfies ──────────────────────────────────────────────
export const selfieApi = {
  getAll: (page = 1) => apiFetch(`/selfies?page=${page}`),
  react: (selfieId, reaction) => apiFetch(`/selfies/${selfieId}/react`, { method: 'POST', body: JSON.stringify({ reaction }) }),
  getRandom: () => apiFetch('/selfies/random'),
  delete: (selfieId) => apiFetch(`/selfies/${selfieId}`, { method: 'DELETE' }),
}

// ─── Wardrobe ─────────────────────────────────────────────
export const wardrobeApi = {
  getItems: (filters = {}) => apiFetch(`/wardrobe?${new URLSearchParams(filters)}`),
  addItem: (data) => apiFetch('/wardrobe', { method: 'POST', body: JSON.stringify(data) }),
  updateItem: (id, data) => apiFetch(`/wardrobe/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteItem: (id) => apiFetch(`/wardrobe/${id}`, { method: 'DELETE' }),
  getOutfits: () => apiFetch('/wardrobe/outfits'),
  createOutfit: (data) => apiFetch('/wardrobe/outfits', { method: 'POST', body: JSON.stringify(data) }),
  getRequests: () => apiFetch('/wardrobe/requests'),
  sendRequest: (data) => apiFetch('/wardrobe/requests', { method: 'POST', body: JSON.stringify(data) }),
  updateRequest: (id, status) => apiFetch(`/wardrobe/requests/${id}`, { method: 'PUT', body: JSON.stringify({ status }) }),
}

// ─── Health ───────────────────────────────────────────────
export const healthApi = {
  getPlans: () => apiFetch('/health/plans'),
  createPlan: (data) => apiFetch('/health/plans', { method: 'POST', body: JSON.stringify(data) }),
  updatePlan: (id, data) => apiFetch(`/health/plans/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  logActivity: (planId, data) => apiFetch(`/health/plans/${planId}/log`, { method: 'POST', body: JSON.stringify(data) }),
  getPartnerPlans: () => apiFetch('/health/partner'),
  react: (planId, reaction) => apiFetch(`/health/plans/${planId}/react`, { method: 'POST', body: JSON.stringify({ reaction }) }),
  getStreaks: () => apiFetch('/health/streaks'),
}

// ─── Activity Feed ────────────────────────────────────────
export const activityApi = {
  getFeed: (page = 1) => apiFetch(`/activity?page=${page}`),
}

// ─── Notifications ────────────────────────────────────────
export const notificationApi = {
  getAll: () => apiFetch('/notifications'),
  markRead: (id) => apiFetch(`/notifications/${id}/read`, { method: 'PUT' }),
  markAllRead: () => apiFetch('/notifications/read-all', { method: 'PUT' }),
}

// ─── Widgets ──────────────────────────────────────────────
export const widgetApi = {
  getConfig: () => apiFetch('/widgets'),
  saveConfig: (data) => apiFetch('/widgets', { method: 'PUT', body: JSON.stringify(data) }),
}

// ─── Games ────────────────────────────────────────────────
export const gameApi = {
  getGames: () => apiFetch('/games'),
  getScores: (gameId) => apiFetch(`/games/${gameId}/scores`),
  submitScore: (gameId, score) => apiFetch(`/games/${gameId}/score`, { method: 'POST', body: JSON.stringify({ score }) }),
}

// ─── Stats ────────────────────────────────────────────────
export const statsApi = {
  getRelationshipStats: () => apiFetch('/stats/relationship'),
}
