# Contas de teste (desenvolvimento)

Válidas em **todas as partes da aplicação**: frontend (Vercel, modo simulado ou ligado ao core), API (`/api/v1/auth/login`) e Swagger (`/docs` → Authorize).
Só existem quando `ENVIRONMENT=development|test`. Em produção o seed cria apenas um admin e avisa para alterar a palavra-passe.

| Portal | Papel | Email | Palavra-passe |
|---|---|---|---|
| Administração | `admin` | admin@gdesigner.school | `Admin123!` |
| Coordenação | `coordinator` | coordenacao@gdesigner.school | `Coord123!` |
| Docente | `teacher` | docente@gdesigner.school | `Docente123!` |
| Estudante | `student` | estudante@gdesigner.school | `Aluno123!` |
| Secretaria | `secretary` | secretaria@gdesigner.school | `Secret123!` |
| Biblioteca | `librarian` | biblioteca@gdesigner.school | `Biblio123!` |
| Recursos humanos | `hr` | rh@gdesigner.school | `Rh123!` |
| Encarregado | `parent` | encarregado@gdesigner.school | `Pai123!` |
| Convidado | `guest` | convidado@gdesigner.school | `Guest123!` |

Fonte única: `services/core/src/dev_accounts.py` (espelhada em `apps/web/src/lib/devAccounts.ts`).
A página de login mostra botões para preencher cada conta com um clique.

## Autenticação sem base de dados

1. **Frontend no Vercel sem backend** — modo simulado automático: se a API não responder (ou `NEXT_PUBLIC_MOCK_API=true`), a app usa `apps/web/src/lib/mockApi.ts`: as 9 contas, cursos, matrículas, notificações e barramento de eventos vivem no `localStorage` do browser. Aparece o selo "modo simulado" no dashboard. Para limpar: `localStorage.clear()`.
2. **Core sem Postgres** — `DATABASE_URL=sqlite+aiosqlite:///./aos_dev.db` (ficheiro local, sem servidor). As contas são semeadas no arranque.
3. **Core com Postgres** — Docker Compose; mesmas contas.

### Variáveis no Vercel
| Variável | Valor | Efeito |
|---|---|---|
| `NEXT_PUBLIC_MOCK_API` | `true` | força modo simulado |
| `NEXT_PUBLIC_ALLOW_MOCK_FALLBACK` | `false` | desliga o fallback automático (exige API real) |
| `API_INTERNAL_URL` | `https://api.exemplo.com` | para onde o Next encaminha `/api/*` e `/health` quando houver core publicado |
