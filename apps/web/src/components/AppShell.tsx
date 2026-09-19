'use client';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { useAuthStore } from '@/stores/authStore';
import { api } from '@/lib/api';
import { ROLE_LABEL } from '@/lib/constants';
import { initials } from '@/lib/utils';
import type { Registry, NavItem } from '@/lib/types';
import { Logo } from './Logo';
import { Icon } from './Icon';

const CORE_NAV: NavItem[] = [
  { label: 'Visão geral', href: '/dashboard', icon: 'home', plugin: 'core' },
  { label: 'Plugins', href: '/plugins', icon: 'puzzle', plugin: 'core', roles: ['admin'] },
  { label: 'Barramento', href: '/events', icon: 'activity', plugin: 'core', roles: ['admin', 'coordinator'] },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const { user, isLoading, hydrate, logout } = useAuthStore();
  const router = useRouter();
  const pathname = usePathname();
  const [nav, setNav] = useState<NavItem[]>([]);
  const [unread, setUnread] = useState(0);

  useEffect(() => { hydrate(); }, [hydrate]);
  useEffect(() => { if (!isLoading && !user) router.replace('/login'); }, [isLoading, user, router]);
  useEffect(() => {
    if (!user) return;
    api<Registry>('/plugins/registry').then((r) => setNav(r.nav)).catch(() => setNav([]));
    api<{ count: number }>('/notifications/unread-count').then((r) => setUnread(r.count)).catch(() => {});
  }, [user]);

  if (isLoading || !user) {
    return <div className="grid min-h-screen place-items-center text-sm text-muted">A carregar o seu portal…</div>;
  }

  const visible = (items: NavItem[]) => items.filter((n) => !n.roles || n.roles.includes(user.role));
  const link = (n: NavItem) => {
    const active = pathname === n.href || pathname.startsWith(n.href + '/');
    return (
      <Link key={n.href} href={n.href}
        className={`flex items-center gap-3 rounded-md px-3 py-2 text-sm ${active ? 'bg-ink text-white' : 'text-ink hover:bg-slate-100'}`}
        aria-current={active ? 'page' : undefined}>
        <Icon name={n.icon ?? 'puzzle'} />
        {n.label}
      </Link>
    );
  };
  const byPlugin = visible(nav).reduce<Record<string, NavItem[]>>((acc, n) => ((acc[n.plugin] ||= []).push(n), acc), {});

  return (
    <div className="flex min-h-screen">
      <aside className="flex w-64 shrink-0 flex-col border-r border-line bg-white px-4 py-5">
        <div className="px-2"><Logo /></div>
        <p className="mt-1 px-2 text-xs text-muted">G Designer School</p>
        <nav className="mt-7 space-y-1" aria-label="Núcleo">{visible(CORE_NAV).map(link)}</nav>
        {Object.entries(byPlugin).map(([plugin, items]) => (
          <nav key={plugin} className="mt-6" aria-label={plugin}>
            <p className="mb-1 px-3 font-mono text-[11px] text-faint">{plugin}</p>
            <div className="space-y-1">{items.map(link)}</div>
          </nav>
        ))}
        <div className="mt-auto border-t border-line pt-4">
          <div className="flex items-center gap-3 px-2">
            <span className="grid h-9 w-9 place-items-center rounded-full bg-ink text-xs font-semibold text-white">
              {initials(user.first_name, user.last_name)}
            </span>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium">{user.first_name} {user.last_name}</p>
              <p className="truncate text-xs text-muted">{ROLE_LABEL[user.role]}</p>
            </div>
            <span className="relative text-muted" title={`${unread} por ler`}>
              <Icon name="bell" />
              {unread > 0 && <span className="absolute -right-1 -top-1 h-2 w-2 rounded-full bg-accent" />}
            </span>
          </div>
          <button onClick={() => logout().then(() => router.replace('/login'))}
            className="mt-3 flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm text-muted hover:bg-slate-100 hover:text-ink">
            <Icon name="logout" /> Terminar sessão
          </button>
        </div>
      </aside>
      <main className="min-w-0 flex-1 overflow-x-hidden px-10 py-8">{children}</main>
    </div>
  );
}
