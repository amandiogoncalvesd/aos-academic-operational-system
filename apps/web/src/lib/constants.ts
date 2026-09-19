export const APP_NAME = 'AOS';
export const APP_FULL_NAME = 'Academic Operational System';
export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? '/api/v1';
export const ROLE_LABEL: Record<string, string> = {
  student: 'Estudante', teacher: 'Docente', coordinator: 'Coordenação', admin: 'Administração',
  secretary: 'Secretaria', librarian: 'Biblioteca', hr: 'Recursos humanos', parent: 'Encarregado', guest: 'Convidado',
};
