import { API_URL } from './constants';

export class ApiError extends Error {
  constructor(public status: number, message: string) { super(message); }
}

const TOKEN_KEY = 'aos.tokens';
export type Tokens = { access_token: string; refresh_token: string; expires_in: number };

export const tokenStore = {
  get(): Tokens | null {
    if (typeof window === 'undefined') return null;
    const raw = localStorage.getItem(TOKEN_KEY);
    return raw ? (JSON.parse(raw) as Tokens) : null;
  },
  set(t: Tokens | null) {
    if (typeof window === 'undefined') return;
    t ? localStorage.setItem(TOKEN_KEY, JSON.stringify(t)) : localStorage.removeItem(TOKEN_KEY);
  },
};

async function refresh(): Promise<Tokens | null> {
  const t = tokenStore.get();
  if (!t) return null;
  const r = await fetch(`${API_URL}/auth/refresh`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: t.refresh_token }),
  });
  if (!r.ok) { tokenStore.set(null); return null; }
  const nt = (await r.json()) as Tokens;
  tokenStore.set(nt);
  return nt;
}

export async function api<T>(path: string, init: RequestInit = {}, retry = true): Promise<T> {
  const t = tokenStore.get();
  const headers = new Headers(init.headers);
  if (t) headers.set('Authorization', `Bearer ${t.access_token}`);
  if (init.body && !(init.body instanceof FormData) && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json');
  const r = await fetch(`${API_URL}${path}`, { ...init, headers });
  if (r.status === 401 && retry && t) {
    const nt = await refresh();
    if (nt) return api<T>(path, init, false);
  }
  if (!r.ok) {
    let msg = r.statusText;
    try { msg = (await r.json()).detail ?? msg; } catch { /* ignore */ }
    throw new ApiError(r.status, typeof msg === 'string' ? msg : JSON.stringify(msg));
  }
  if (r.status === 204) return undefined as T;
  return (await r.json()) as T;
}

export const login = (email: string, password: string) =>
  api<Tokens>('/auth/login/json', { method: 'POST', body: JSON.stringify({ email, password }) });
