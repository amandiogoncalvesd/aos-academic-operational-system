"""Contas de teste (apenas ENVIRONMENT=development|test). Uma por papel.
Mesma lista é espelhada no frontend em apps/web/src/lib/devAccounts.ts."""

DEV_PASSWORD_SUFFIX = "123!"

DEV_ACCOUNTS = [
    # email, first, last, role, password
    ("admin@gdesigner.school", "Admin", "AOS", "admin", "Admin123!"),
    ("coordenacao@gdesigner.school", "Marta", "Fernandes", "coordinator", "Coord123!"),
    ("docente@gdesigner.school", "Paulo", "Neto", "teacher", "Docente123!"),
    ("estudante@gdesigner.school", "Ana", "Kianda", "student", "Aluno123!"),
    ("secretaria@gdesigner.school", "Rosa", "Chipenda", "secretary", "Secret123!"),
    ("biblioteca@gdesigner.school", "João", "Sakala", "librarian", "Biblio123!"),
    ("rh@gdesigner.school", "Lúcia", "Mbala", "hr", "Rh123!"),
    ("encarregado@gdesigner.school", "Domingos", "Kianda", "parent", "Pai123!"),
    ("convidado@gdesigner.school", "Visitante", "AOS", "guest", "Guest123!"),
]
