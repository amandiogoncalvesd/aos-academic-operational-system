'use client';
import { useEffect, useRef, useState } from 'react';
import { api, tokenStore } from '@/lib/api';
import { API_URL } from '@/lib/constants';
import type { AOSEvent } from '@/lib/types';
import { formatTime } from '@/lib/utils';

/** Feed em tempo real do Event Bus (SSE). O único elemento animado do produto: o pulso do sistema. */
export function EventFeed({ limit = 12, compact = false }: { limit?: number; compact?: boolean }) {
  const [events, setEvents] = useState<AOSEvent[]>([]);
  const [live, setLive] = useState(false);
  const seen = useRef(new Set<string>());

  useEffect(() => {
    api<AOSEvent[]>(`/events/recent?limit=${limit}`).then((evs) => {
      evs.forEach((e) => seen.current.add(e.id));
      setEvents(evs);
    }).catch(() => {});
    // EventSource não envia Authorization → usamos fetch + ReadableStream
    const ctrl = new AbortController();
    const t = tokenStore.get();
    if (!t) return;
    (async () => {
      try {
        const r = await fetch(`${API_URL}/events/stream`, { headers: { Authorization: `Bearer ${t.access_token}` }, signal: ctrl.signal });
        if (!r.ok || !r.body) return;
        setLive(true);
        const reader = r.body.getReader();
        const dec = new TextDecoder();
        let buf = '';
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          buf += dec.decode(value, { stream: true });
          const chunks = buf.split('\n\n');
          buf = chunks.pop() ?? '';
          for (const c of chunks) {
            const data = c.split('\n').find((l) => l.startsWith('data: '));
            if (!data) continue;
            const ev = JSON.parse(data.slice(6)) as AOSEvent;
            if (seen.current.has(ev.id)) continue;
            seen.current.add(ev.id);
            setEvents((prev) => [ev, ...prev].slice(0, limit));
          }
        }
      } catch { /* abortado */ } finally { setLive(false); }
    })();
    return () => ctrl.abort();
  }, [limit]);

  return (
    <div className="rounded-lg border border-line bg-white">
      <div className="flex items-center justify-between border-b border-line px-4 py-3">
        <h2 className="font-display text-sm font-semibold">Barramento de eventos</h2>
        <span className="flex items-center gap-2 text-xs text-muted">
          <span className={`h-2 w-2 rounded-full ${live ? 'bg-emerald-500 pulse' : 'bg-faint'}`} />
          {live ? 'em directo' : 'histórico'}
        </span>
      </div>
      {events.length === 0 ? (
        <p className="px-4 py-8 text-center text-sm text-muted">Ainda não há eventos. Crie um curso ou registe um utilizador e veja o sistema reagir.</p>
      ) : (
        <ul className="divide-y divide-slate-100 overflow-hidden font-mono text-[12.5px]">
          {events.map((e, i) => (
            <li key={e.id} className={`flex min-w-0 items-baseline gap-4 px-4 py-2 ${i === 0 ? "flash" : ""}`}>
              <span className="w-[68px] shrink-0 text-faint">{formatTime(e.timestamp)}</span>
              <span className="shrink-0 text-action">{e.type}</span>
              {!compact && <span className="min-w-0 flex-1 truncate text-muted">{JSON.stringify(e.payload)}</span>}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
