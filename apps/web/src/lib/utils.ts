import { clsx, type ClassValue } from 'clsx';

export const cn = (...i: ClassValue[]) => clsx(i);

export const formatDate = (d: string | Date, opts: Intl.DateTimeFormatOptions = { dateStyle: 'medium', timeStyle: 'short' }) =>
  new Intl.DateTimeFormat('pt-AO', opts).format(new Date(d));

export const formatTime = (d: string | Date) =>
  new Intl.DateTimeFormat('pt-AO', { hour: '2-digit', minute: '2-digit', second: '2-digit' }).format(new Date(d));

export const formatCurrency = (v: number, currency = 'AOA') =>
  new Intl.NumberFormat('pt-AO', { style: 'currency', currency, maximumFractionDigits: 0 }).format(v);

export const initials = (first: string, last: string) => `${first[0] ?? ''}${last[0] ?? ''}`.toUpperCase();
