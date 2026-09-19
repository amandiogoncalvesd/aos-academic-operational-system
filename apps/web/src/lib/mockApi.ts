/**
 * Backend simulado em memória (localStorage) para desenvolvimento sem API real.
 * Activo quando NEXT_PUBLIC_MOCK_API=true ou quando o core não responde.
 * Reproduz o mesmo contrato dos endpoints do core usados pelo frontend.
 */
import { DEV_ACCOUNTS } from './devAccounts';
import { ApiError } from './api';
import type { AOSEvent, Course, Enrollment, Notification, Plugin, Registry, User } from './types';

const KEY = 'aos.mock.state';
const uid = () => (crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).slice(2) + Date.now().toString(36));
const now = () => new Date().toISOString();

interface State { users: (User & { password: string })[]; courses: Course[]; enrollments: Enrollment[]; notifications: Notification[]; events: AOSEvent[]; plugins: Plugin[] }

function fresh(): State {
  const users = DEV_ACCOUNTS.map((a) => ({
    id: uid(), email: a.email, first_name: a.first, last_name: a.last, role: a.role, institution_id: 'gds',
    avatar_url: null, is_active: true, is_verified: true, last_login: null, created_at: now(), password: a.password,
  }));
  const s: State = {
    users, courses: [], enrollments: [], notifications: [], events: [],
    plugins: [
      { id: 'p1', name: 'AOS Notifications', slug: 'aos-core-notify', version: '0.1.0', description: 'Converte eventos do barramento em notificações in-app.', author: 'AOS Core Team', is_active: true, is_system: true, config: {}, permissions: ['notify.send'] },
      { id: 'p2', name: 'AOS Student Information System', slug: 'aos-domain-sis', version: '0.1.0', description: 'Cursos, turmas e matrículas.', author: 'AOS Core Team', is_active: true, is_system: false, config: {}, permissions: ['sis.course.create', 'sis.course.read', 'sis.enrollment.manage'] },
    ],
  };
  publish(s, 'core.started', { version: '0.1.0-mock', plugins: s.plugins.map((p) => p.slug) });
  return s;
}
function publish(s: State, type: string, payload: Record<string, unknown>) {
  s.events.unshift({ id: uid(), type, payload, metadata: { source: 'mock' }, timestamp: now() });
  s.events = s.events.slice(0, 200);
}
function load(): State {
  if (typeof window === 'undefined') return fresh();
  const raw = localStorage.getItem(KEY);
  return raw ? (JSON.parse(raw) as State) : fresh();
}
function save(s: State) { if (typeof window !== 'undefined') localStorage.setItem(KEY, JSON.stringify(s)); }

const SESSION = 'aos.mock.session';
function me(s: State): User {
  const id = typeof window !== 'undefined' ? localStorage.getItem(SESSION) : null;
  const u = s.users.find((x) => x.id === id);
  if (!u) throw new ApiError(401, 'Sessão inválida');
  return u;
}
const pub = ({ password: _p, ...u }: User & { password: string }): User => u;
const q = (path: string) => Object.fromEntries(new URL('http://x' + path).searchParams);
const p = (path: string) => path.split('?')[0] ?? path;

export async function mockApi<T>(path: string, init: RequestInit = {}): Promise<T> {
  const s = load();
  const method = (init.method ?? 'GET').toUpperCase();
  const body = init.body ? JSON.parse(init.body as string) : {};
  const route = p(path);
  const r = <T,>(v: unknown) => { save(s); return v as T; };

  if (route === '/auth/login/json' && method === 'POST') {
    const u = s.users.find((x) => x.email === body.email && x.password === body.password);
    if (!u) throw new ApiError(401, 'Credenciais inválidas');
    u.last_login = now(); localStorage.setItem(SESSION, u.id);
    publish(s, 'auth.user.logged_in', { user_id: u.id, ip: 'mock' });
    return r({ access_token: 'mock.' + u.id, refresh_token: 'mock-r.' + u.id, expires_in: 3600 });
  }
  if (route === '/auth/logout') { localStorage.removeItem(SESSION); return r({ success: true }); }
  if (route === '/auth/me') return r(pub(me(s) as User & { password: string }));
  const user = me(s);

  if (route === '/plugins/registry') {
    const reg: Registry = {
      plugins: Object.fromEntries(s.plugins.map((x) => [x.slug, { status: x.is_active ? 'active' : 'inactive', version: x.version, error: null }])),
      actions: {}, filters: { 'sis.enrollment.validate': ['aos-domain-sis'] },
      events: { 'auth.user.registered': ['welcome', 'on_user'], 'sis.student.enrolled': ['enrolled'] },
      nav: s.plugins.find((x) => x.slug === 'aos-domain-sis')?.is_active ? [
        { label: 'Cursos', href: '/sis/courses', icon: 'book-open', roles: ['admin', 'coordinator', 'teacher', 'student'], plugin: 'aos-domain-sis' },
        { label: 'Matrículas', href: '/sis/enrollments', icon: 'clipboard-list', roles: ['admin', 'coordinator', 'secretary'], plugin: 'aos-domain-sis' },
      ] : [],
    };
    return r(reg);
  }
  if (route === '/plugins') return r(s.plugins);
  const tog = route.match(/^\/plugins\/(\w+)\/(activate|deactivate)$/);
  if (tog) { const pl = s.plugins.find((x) => x.id === tog[1])!; if (pl.is_system && tog[2] === 'deactivate') throw new ApiError(400, 'Plugins de sistema não podem ser desactivados'); pl.is_active = tog[2] === 'activate'; publish(s, `core.plugin.${tog[2]}d`, { plugin: pl.slug }); return r(pl); }

  if (route === '/notifications/unread-count') return r({ count: s.notifications.filter((n) => !n.is_read && (n as Notification & { user_id: string }).user_id === user.id).length });
  if (route === '/notifications') { const items = s.notifications.filter((n) => (n as Notification & { user_id: string }).user_id === user.id); return r({ items, total: items.length, page: 1, page_size: 20, pages: 1 }); }
  if (route === '/users') { const items = s.users.map(pub); return r({ items: items.slice(0, +(q(path).page_size ?? 20)), total: items.length, page: 1, page_size: 20, pages: 1 }); }
  if (route === '/events/recent') return r(s.events.slice(0, +(q(path).limit ?? 50)));

  if (route === '/sis/courses' && method === 'GET') return r(s.courses.filter((c) => c.is_active));
  if (route === '/sis/courses' && method === 'POST') {
    if (!['admin', 'coordinator'].includes(user.role)) throw new ApiError(403, 'Apenas coordenação pode criar cursos');
    if (s.courses.some((c) => c.code === body.code)) throw new ApiError(409, 'Código de curso já existe');
    const c: Course = { id: uid(), code: body.code, name: body.name, description: body.description ?? null, credits: body.credits ?? 0, capacity: body.capacity ?? 30, is_active: true };
    s.courses.push(c); publish(s, 'sis.course.created', { course_id: c.id, code: c.code, name: c.name }); return r(c);
  }
  if (route === '/sis/enrollments' && method === 'GET') return r(user.role === 'student' ? s.enrollments.filter((e) => e.student_id === user.id) : s.enrollments);
  if (route === '/sis/enrollments' && method === 'POST') {
    const c = s.courses.find((x) => x.id === body.course_id); if (!c) throw new ApiError(404, 'Curso não encontrado');
    const sid = body.student_id ?? user.id;
    const taken = s.enrollments.filter((e) => e.course_id === c.id && e.status === 'active').length;
    if (taken >= c.capacity) throw new ApiError(400, 'Turma lotada');
    if (s.enrollments.some((e) => e.course_id === c.id && e.student_id === sid)) throw new ApiError(409, 'Já matriculado');
    const e: Enrollment = { id: uid(), course_id: c.id, student_id: sid, term: '2026/2027', status: 'active', created_at: now() };
    s.enrollments.push(e);
    publish(s, 'sis.student.enrolled', { enrollment_id: e.id, user_id: sid, course_code: c.code, course_name: c.name });
    s.notifications.unshift({ id: uid(), type: 'info', title: 'Matrícula confirmada', message: `Está inscrito em ${c.name}.`, is_read: false, created_at: now(), user_id: sid } as Notification);
    return r(e);
  }
  throw new ApiError(404, `mock: rota não implementada ${method} ${route}`);
}

export const mockHealth = () => ({ status: 'ok', version: '0.1.0-mock', environment: 'mock', event_bus: 'localStorage', plugins: { 'aos-core-notify': 'active', 'aos-domain-sis': 'active' } });
