'use client';
import { useCallback, useEffect, useState } from 'react';
import { api } from '@/lib/api';
import type { Plugin, Registry } from '@/lib/types';

export default function PluginsPage() {
  const [plugins, setPlugins] = useState<Plugin[]>([]);
  const [registry, setRegistry] = useState<Registry | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(() => {
    api<Plugin[]>('/plugins').then(setPlugins).catch((e) => setError(e.message));
    api<Registry>('/plugins/registry').then(setRegistry).catch(() => {});
  }, []);
  useEffect(load, [load]);

  async function toggle(p: Plugin) {
    try { await api(`/plugins/${p.id}/${p.is_active ? 'deactivate' : 'activate'}`, { method: 'POST' }); load(); }
    catch (e) { setError(e instanceof Error ? e.message : 'Falhou'); }
  }

  return (
    <div className="mx-auto max-w-5xl">
      <h1 className="font-display text-3xl font-semibold tracking-tight">Plugins</h1>
      <p className="mt-1 text-sm text-muted">Tudo no AOS é um plugin. Os de sistema não podem ser desligados.</p>
      {error && <p role="alert" className="mt-4 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

      <table className="mt-8 w-full border-separate border-spacing-0 overflow-hidden rounded-lg border border-line bg-white text-sm">
        <thead className="text-left text-xs text-muted">
          <tr>{['Plugin', 'Versão', 'Estado', 'Permissões', ''].map((h) => <th key={h} className="border-b border-line px-4 py-2.5 font-medium">{h}</th>)}</tr>
        </thead>
        <tbody>
          {plugins.map((p) => {
            const rt = registry?.plugins[p.slug];
            return (
              <tr key={p.id} className="align-top">
                <td className="border-b border-slate-100 px-4 py-3">
                  <p className="font-medium">{p.name}</p>
                  <p className="font-mono text-xs text-faint">{p.slug}</p>
                  {p.description && <p className="mt-1 max-w-md text-muted">{p.description}</p>}
                  {rt?.error && <p className="mt-1 font-mono text-xs text-red-600">{rt.error}</p>}
                </td>
                <td className="border-b border-slate-100 px-4 py-3 font-mono text-xs">{p.version}</td>
                <td className="border-b border-slate-100 px-4 py-3">
                  <span className={`inline-flex items-center gap-1.5 ${p.is_active ? 'text-emerald-700' : 'text-muted'}`}>
                    <span className={`h-1.5 w-1.5 rounded-full ${p.is_active ? 'bg-emerald-500' : 'bg-faint'}`} />
                    {p.is_active ? 'activo' : 'inactivo'}{p.is_system ? ' · sistema' : ''}
                  </span>
                </td>
                <td className="border-b border-slate-100 px-4 py-3 font-mono text-xs text-muted">{p.permissions.join(', ') || '—'}</td>
                <td className="border-b border-slate-100 px-4 py-3 text-right">
                  {!p.is_system && <button onClick={() => toggle(p)} className="btn-ghost">{p.is_active ? 'Desactivar' : 'Activar'}</button>}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {registry && (
        <div className="mt-8 grid gap-6 md:grid-cols-3">
          <HookList title="Eventos subscritos" data={registry.events} />
          <HookList title="Filters" data={registry.filters} />
          <HookList title="Actions" data={registry.actions} />
        </div>
      )}
    </div>
  );
}

function HookList({ title, data }: { title: string; data: Record<string, string[]> }) {
  const entries = Object.entries(data);
  return (
    <div className="rounded-lg border border-line bg-white p-4">
      <h2 className="font-display text-sm font-semibold">{title}</h2>
      {entries.length === 0 ? <p className="mt-2 text-sm text-muted">Nenhum registado ainda.</p> : (
        <ul className="mt-3 space-y-2 font-mono text-xs">
          {entries.map(([k, v]) => <li key={k}><span className="text-action">{k}</span><br /><span className="text-faint">← {v.join(', ')}</span></li>)}
        </ul>
      )}
    </div>
  );
}
