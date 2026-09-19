import type { Role } from './types';

/** Contas de teste — espelho de services/core/src/dev_accounts.py. Apenas para desenvolvimento. */
export const DEV_ACCOUNTS: { email: string; password: string; first: string; last: string; role: Role }[] = [
  { email: 'admin@gdesigner.school', password: 'Admin123!', first: 'Admin', last: 'AOS', role: 'admin' },
  { email: 'coordenacao@gdesigner.school', password: 'Coord123!', first: 'Marta', last: 'Fernandes', role: 'coordinator' },
  { email: 'docente@gdesigner.school', password: 'Docente123!', first: 'Paulo', last: 'Neto', role: 'teacher' },
  { email: 'estudante@gdesigner.school', password: 'Aluno123!', first: 'Ana', last: 'Kianda', role: 'student' },
  { email: 'secretaria@gdesigner.school', password: 'Secret123!', first: 'Rosa', last: 'Chipenda', role: 'secretary' },
  { email: 'biblioteca@gdesigner.school', password: 'Biblio123!', first: 'João', last: 'Sakala', role: 'librarian' },
  { email: 'rh@gdesigner.school', password: 'Rh123!', first: 'Lúcia', last: 'Mbala', role: 'hr' },
  { email: 'encarregado@gdesigner.school', password: 'Pai123!', first: 'Domingos', last: 'Kianda', role: 'parent' },
  { email: 'convidado@gdesigner.school', password: 'Guest123!', first: 'Visitante', last: 'AOS', role: 'guest' },
];
