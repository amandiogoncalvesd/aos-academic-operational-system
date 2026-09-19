'use client';
import { create } from 'zustand';
import { api, login as apiLogin, tokenStore } from '@/lib/api';
import type { User } from '@/lib/types';

interface AuthState {
  user: User | null; isLoading: boolean; isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  hydrate: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null, isLoading: true, isAuthenticated: false,
  async login(email, password) {
    tokenStore.set(await apiLogin(email, password));
    const user = await api<User>('/auth/me');
    set({ user, isAuthenticated: true, isLoading: false });
  },
  async logout() {
    try { await api('/auth/logout', { method: 'POST' }); } catch { /* já expirado */ }
    tokenStore.set(null);
    set({ user: null, isAuthenticated: false, isLoading: false });
  },
  async hydrate() {
    if (!tokenStore.get()) return set({ isLoading: false });
    try { set({ user: await api<User>('/auth/me'), isAuthenticated: true, isLoading: false }); }
    catch { tokenStore.set(null); set({ isLoading: false }); }
  },
}));
