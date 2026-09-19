'use client';
import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import type { Course, Enrollment } from '@/lib/types';
import { formatDate } from '@/lib/utils';

export default function EnrollmentsPage() {
  const [rows, setRows] = useState<Enrollment[]>([]);
  const [courses, setCourses] = useState<Record<string, Course>>({});

  useEffect(() => {
    api<Enrollment[]>('/sis/enrollments').then(setRows).catch(() => {});
    api<Course[]>('/sis/courses').then((cs) => setCourses(Object.fromEntries(cs.map((c) => [c.id, c])))).catch(() => {});
  }, []);

  return (
    <div className="mx-auto max-w-5xl">
      <h1 className="font-display text-3xl font-semibold tracking-tight">Matrículas</h1>
      <p className="mt-1 text-sm text-muted">{rows.length} registo{rows.length === 1 ? '' : 's'} · ano lectivo 2026/2027</p>
      {rows.length === 0 ? (
        <div className="mt-8 rounded-lg border border-dashed border-line bg-white p-10 text-center text-sm text-muted">Ainda não há matrículas.</div>
      ) : (
        <table className="mt-8 w-full overflow-hidden rounded-lg border border-line bg-white text-sm">
          <thead className="text-left text-xs text-muted"><tr>{['Curso', 'Estudante', 'Período', 'Estado', 'Data'].map((h) => <th key={h} className="border-b border-line px-4 py-2.5 font-medium">{h}</th>)}</tr></thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id}>
                <td className="border-b border-slate-100 px-4 py-3"><span className="font-mono text-action">{courses[r.course_id]?.code ?? '—'}</span> {courses[r.course_id]?.name}</td>
                <td className="border-b border-slate-100 px-4 py-3 font-mono text-xs text-muted">{r.student_id.slice(0, 8)}…</td>
                <td className="border-b border-slate-100 px-4 py-3">{r.term}</td>
                <td className="border-b border-slate-100 px-4 py-3">{r.status === 'active' ? <span className="text-emerald-700">activa</span> : <span className="text-muted">{r.status}</span>}</td>
                <td className="border-b border-slate-100 px-4 py-3 text-muted">{formatDate(r.created_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
