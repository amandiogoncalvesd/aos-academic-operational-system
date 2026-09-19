'use client';
import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';
import { useAuthStore } from '@/stores/authStore';
import { Logo } from '@/components/Logo';
import { DEV_ACCOUNTS } from '@/lib/devAccounts';
import { ROLE_LABEL } from '@/lib/constants';

export default function LoginPage() {
  const login = useAuthStore((s) => s.login);
  const router = useRouter();
  const [email, setEmail] = useState('admin@gdesigner.school');
  const [password, setPassword] = useState('Admin123!');
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setBusy(true); setError(null);
    try { await login(email, password); router.replace('/dashboard'); }
    catch (err) { setError(err instanceof Error ? err.message : 'Não foi possível entrar'); }
    finally { setBusy(false); }
  }

  return (
    <div className="grid min-h-screen lg:grid-cols-[1.1fr_1fr]">
      <section className="hidden bg-ink p-12 text-white lg:flex lg:flex-col">
        <Logo />
        <div className="my-auto max-w-md">
          <h1 className="font-display text-[44px] font-semibold leading-[1.05] tracking-tight">
            Uma escola inteira,<br />um único sistema.
          </h1>
          <p className="mt-6 text-[15px] leading-relaxed text-slate-300">
            Matrículas, aulas, notas, propinas, biblioteca e comunicação ligados por um barramento de eventos.
            Cada função é um plugin; a instituição decide o que liga.
          </p>
        </div>
        <dl className="grid grid-cols-3 gap-6 text-sm">
          <div><dt className="text-slate-400">Núcleo</dt><dd className="mt-1 font-medium">FastAPI + Postgres</dd></div>
          <div><dt className="text-slate-400">Domínios</dt><dd className="mt-1 font-medium">SIS · LMS · ERP · CRM · RH</dd></div>
          <div><dt className="text-slate-400">Ano lectivo</dt><dd className="mt-1 font-medium">2026/2027</dd></div>
        </dl>
      </section>
      <section className="flex items-center justify-center px-6 py-12">
        <form onSubmit={onSubmit} className="w-full max-w-sm">
          <div className="lg:hidden"><Logo /></div>
          <h2 className="mt-6 font-display text-2xl font-semibold tracking-tight lg:mt-0">Entrar</h2>
          <p className="mt-1 text-sm text-muted">G Designer School · Huambo</p>
          <label className="mt-8 block text-sm font-medium" htmlFor="email">Email</label>
          <input id="email" type="email" autoComplete="username" className="field mt-1.5" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <label className="mt-4 block text-sm font-medium" htmlFor="password">Palavra-passe</label>
          <input id="password" type="password" autoComplete="current-password" className="field mt-1.5" value={password} onChange={(e) => setPassword(e.target.value)} required />
          {error && <p role="alert" className="mt-4 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
          <button type="submit" disabled={busy} className="btn-primary mt-6 w-full">{busy ? 'A entrar…' : 'Entrar'}</button>
          <fieldset className="mt-8 border-t border-line pt-5">
            <legend className="pr-3 text-xs text-muted">Contas de teste (desenvolvimento)</legend>
            <div className="mt-2 grid grid-cols-3 gap-1.5">
              {DEV_ACCOUNTS.map((a) => (
                <button key={a.email} type="button" onClick={() => { setEmail(a.email); setPassword(a.password); }}
                  className={`rounded-md border px-2 py-1.5 text-left text-xs ${email === a.email ? 'border-ink bg-ink text-white' : 'border-line bg-white text-ink hover:bg-slate-50'}`}>
                  {ROLE_LABEL[a.role]}
                </button>
              ))}
            </div>
            <p className="mt-3 font-mono text-[11px] text-faint">{email} · {password}</p>
          </fieldset>
        </form>
      </section>
    </div>
  );
}
