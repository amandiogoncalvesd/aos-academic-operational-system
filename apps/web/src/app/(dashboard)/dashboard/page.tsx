'use client';
import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import type { Health, Paginated, Registry, User } from '@/lib/types';
import { useAuthStore } from '@/stores/authStore';
import { EventFeed } from '@/components/EventFeed';
import Link from 'next/link';

export default function DashboardPage() {
  const user = useAuthStore((s) => s.user)!;
  const [health, setHealth] = useState<Health | null>(null);
  const [registry, setRegistry] = useState<Registry | null>(null);
  const [users, setUsers] = useState<number | null>(null);

  useEffect(() => {
    fetch('/health').then((r) => r.json()).then(setHealth).catch(() => {});
    api<Registry>('/plugins/registry').then(setRegistry).catch(() => {});
    if (user.role === 'admin') api<Paginated<User>>('/users?page_size=1').then((r) => setUsers(r.total)).catch(() => {});
  }, [user.role]);

  const active = registry ? Object.values(registry.plugins).filter((p) => p.status === 'active').length : 0;
  const subs = registry ? Object.values(registry.events).reduce((a, b) => a + b.length, 0) : 0;
  const hour = new Date().getHours();
  const greet = hour < 12 ? 'Bom dia' : hour < 19 ? 'Boa tarde' : 'Boa noite';

  return (
    <div className="mx-auto max-w-5xl">
      <h1 className="font-display text-3xl font-semibold tracking-tight">{greet}, {user.first_name}.</h1>
      <p className="mt-1 text-sm text-muted">
        O núcleo está {health ? <span className="text-emerald-600">operacional</span> : 'a responder…'}
        {health && <> · v{health.version} · barramento <span className="font-mono">{health.event_bus}</span></>}
      </p>

      <div className="mt-8 grid gap-px overflow-hidden rounded-lg border border-line bg-line sm:grid-cols-3">
        <Stat label="Plugins activos" value={active} hint={registry ? `${Object.keys(registry.plugins).length} descobertos` : ''} href="/plugins" />
        <Stat label="Subscrições de eventos" value={subs} hint={registry ? `${Object.keys(registry.filters).length} filtros registados` : ''} href="/events" />
        <Stat label="Utilizadores" value={users ?? '—'} hint="todas as instituições" />
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_320px]">
        <EventFeed />
        <div className="rounded-lg border border-line bg-white p-5">
          <h2 className="font-display text-sm font-semibold">Comece por aqui</h2>
          <ol className="mt-3 space-y-3 text-sm">
            <li><Link className="text-action hover:underline" href="/sis/courses">Criar o primeiro curso</Link><p className="text-muted">O plugin SIS publica <code className="font-mono text-xs">sis.course.created</code>.</p></li>
            <li><Link className="text-action hover:underline" href="/plugins">Ver plugins e hooks</Link><p className="text-muted">Actions, filters e quem os regista.</p></li>
            <li><a className="text-action hover:underline" href="/docs" target="_blank" rel="noreferrer">Abrir a documentação da API</a><p className="text-muted">Swagger gerado pelo núcleo.</p></li>
          </ol>
        </div>
      </div>
    </div>
  );
}

function Stat({ label, value, hint, href }: { label: string; value: number | string; hint?: string; href?: string }) {
  const body = (
    <div className="bg-white p-5">
      <p className="text-sm text-muted">{label}</p>
      <p className="mt-2 font-display text-3xl font-semibold tracking-tight">{value}</p>
      {hint && <p className="mt-1 text-xs text-faint">{hint}</p>}
    </div>
  );
  return href ? <Link href={href} className="block hover:bg-slate-50">{body}</Link> : body;
}
