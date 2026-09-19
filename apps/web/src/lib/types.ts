export type Role = 'student' | 'teacher' | 'coordinator' | 'admin' | 'secretary' | 'librarian' | 'hr' | 'parent' | 'guest';

export interface User {
  id: string; email: string; first_name: string; last_name: string; role: Role;
  institution_id: string | null; avatar_url: string | null; is_active: boolean; is_verified: boolean;
  last_login: string | null; created_at: string;
}
export interface Paginated<T> { items: T[]; total: number; page: number; page_size: number; pages: number }
export interface Notification { id: string; type: string; title: string; message: string; is_read: boolean; created_at: string }
export interface Plugin {
  id: string; name: string; slug: string; version: string; description: string | null; author: string | null;
  is_active: boolean; is_system: boolean; config: Record<string, unknown>; permissions: string[];
}
export interface NavItem { label: string; href: string; icon?: string; roles?: Role[]; plugin: string }
export interface Registry {
  plugins: Record<string, { status: string; version: string; error: string | null }>;
  actions: Record<string, string[]>; filters: Record<string, string[]>; events: Record<string, string[]>;
  nav: NavItem[];
}
export interface AOSEvent { id: string; type: string; payload: Record<string, unknown>; metadata: Record<string, unknown>; timestamp: string }
export interface Course { id: string; code: string; name: string; description: string | null; credits: number; capacity: number; is_active: boolean }
export interface Enrollment { id: string; course_id: string; student_id: string; term: string; status: string; created_at: string }
export interface Health { status: string; version: string; environment: string; event_bus: string; plugins: Record<string, string> }
