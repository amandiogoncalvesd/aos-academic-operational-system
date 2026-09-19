'use client';
import { FormEvent, useCallback, useEffect, useState } from 'react';
import { api } from '@/lib/api';
import type { Course, Enrollment } from '@/lib/types';
import { useAuthStore } from '@/stores/authStore';

export default function CoursesPage() {
  const user = useAuthStore((s) => s.user)!;
  const canCreate = user.role === 'admin' || user.role === 'coordinator';
  const [courses, setCourses] = useState<Course[]>([]);
  const [mine, setMine] = useState<Enrollment[]>([]);
  const [form, setForm] = useState({ code: '', name: '', credits: 6, capacity: 30 });
  const [msg, setMsg] = useState<{ kind: 'ok' | 'err'; text: string } | null>(null);

  const load = useCallback(() => {
    api<Course[]>('/sis/courses').then(setCourses).catch(() => {});
    api<Enrollment[]>('/sis/enrollments').then(setMine).catch(() => {});
  }, []);
  useEffect(load, [load]);

  async function create(e: FormEvent) {
    e.preventDefault();
    try {
      await api('/sis/courses', { method: 'POST', body: JSON.stringify(form) });
      setMsg({ kind: 'ok', text: `Curso ${form.code} criado.` });
      setForm({ code: '', name: '', credits: 6, capacity: 30 });
      load();
    } catch (err) { setMsg({ kind: 'err', text: err instanceof Error ? err.message : 'Falhou' }); }
  }
  async function enroll(c: Course) {
    try { await api('/sis/enrollments', { method: 'POST', body: JSON.stringify({ course_id: c.id }) }); setMsg({ kind: 'ok', text: `Matriculado em ${c.name}.` }); load(); }
    catch (err) { setMsg({ kind: 'err', text: err instanceof Error ? err.message : 'Falhou' }); }
  }
  const enrolledIn = new Set(mine.filter((m) => m.status === 'active').map((m) => m.course_id));

  return (
    <div className="mx-auto max-w-5xl">
      <h1 className="font-display text-3xl font-semibold tracking-tight">Cursos</h1>
      <p className="mt-1 text-sm text-muted">Plugin <span className="font-mono">aos-domain-sis</span> · ano lectivo 2026/2027</p>
      {msg && <p role="status" className={`mt-4 rounded-md border px-3 py-2 text-sm ${msg.kind === 'ok' ? 'border-emerald-200 bg-emerald-50 text-emerald-800' : 'border-red-200 bg-red-50 text-red-700'}`}>{msg.text}</p>}

      <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_320px]">
        <div>
          {courses.length === 0 ? (
            <div className="rounded-lg border border-dashed border-line bg-white p-10 text-center text-sm text-muted">
              Ainda não há cursos. {canCreate ? 'Crie o primeiro no formulário ao lado.' : 'A coordenação ainda não abriu inscrições.'}
            </div>
          ) : (
            <ul className="divide-y divide-slate-100 overflow-hidden rounded-lg border border-line bg-white">
              {courses.map((c) => (
                <li key={c.id} className="flex items-center gap-4 px-5 py-4">
                  <span className="w-20 shrink-0 font-mono text-sm text-action">{c.code}</span>
                  <div className="min-w-0 flex-1">
                    <p className="font-medium">{c.name}</p>
                    <p className="text-xs text-muted">{c.credits} créditos · {c.capacity} vagas</p>
                  </div>
                  {enrolledIn.has(c.id)
                    ? <span className="text-sm text-emerald-700">Inscrito</span>
                    : <button onClick={() => enroll(c)} className="btn-ghost">Inscrever-me</button>}
                </li>
              ))}
            </ul>
          )}
        </div>
        {canCreate && (
          <form onSubmit={create} className="h-fit rounded-lg border border-line bg-white p-5">
            <h2 className="font-display text-sm font-semibold">Novo curso</h2>
            <label className="mt-4 block text-sm" htmlFor="code">Código</label>
            <input id="code" className="field mt-1" placeholder="UX101" value={form.code} onChange={(e) => setForm({ ...form, code: e.target.value.toUpperCase() })} required />
            <label className="mt-3 block text-sm" htmlFor="name">Nome</label>
            <input id="name" className="field mt-1" placeholder="Fundamentos de UX" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            <div className="mt-3 grid grid-cols-2 gap-3">
              <div><label className="block text-sm" htmlFor="credits">Créditos</label><input id="credits" type="number" min={0} className="field mt-1" value={form.credits} onChange={(e) => setForm({ ...form, credits: +e.target.value })} /></div>
              <div><label className="block text-sm" htmlFor="capacity">Vagas</label><input id="capacity" type="number" min={1} className="field mt-1" value={form.capacity} onChange={(e) => setForm({ ...form, capacity: +e.target.value })} /></div>
            </div>
            <button type="submit" className="btn-primary mt-5 w-full">Criar curso</button>
          </form>
        )}
      </div>
    </div>
  );
}
