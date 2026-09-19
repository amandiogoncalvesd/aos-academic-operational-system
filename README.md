# AOS — Academic Operational System

Sistema Operacional Acadêmico da **G Designer School**: um core headless + plugins (LMS, SIS, ERP, CRM, RH, BI,
Biblioteca, Comunicação, Exames, S2ST) ligados por um Event Bus.

```
aos/
├── apps/            web (Next.js 14) · mobile (Flutter) · docs
├── packages/        config · ui · types · utils · api-client · icons
├── plugins/         aos-core-* (infra) · aos-domain-* (domínios)   ← cada um com manifest.json
├── services/        core (FastAPI) · gateway · workers (Celery)
├── infra/           docker · kubernetes · terraform
└── docs/            blueprint, infra, LMS/S2ST, design system, prompt de desenvolvimento
```

## Estado actual (fase 0 — esqueleto + core)

| Área | Estado |
|---|---|
| Monorepo (Turborepo + pnpm), configs partilhadas | ✅ |
| **Core FastAPI**: auth JWT (access + refresh rotativo), utilizadores, instituições, papéis/permissões, notificações, audit trail, settings, plugins | ✅ |
| **Event Bus** (memory / Redis / Kafka) com event-store e SSE | ✅ |
| **Plugin Engine**: manifest, descoberta, ordenação topológica, actions/filters, isolamento de erros | ✅ |
| Plugins de referência: `aos-core-notify`, `aos-domain-sis` (cursos + matrículas) | ✅ |
| Docker Compose (Postgres 16, Redis 7, Kafka, ClickHouse) | ✅ |
| Testes de integração (httpx + pytest) | ✅ 6/6 |
| Web app shell (Next.js) | ✅ login + dashboard dinâmico por plugins |
| LMS, ERP, CRM, RH, BI, Biblioteca, Exames, S2ST, Mobile | ⏳ próximos plugins |

## Arrancar em 2 minutos (sem Docker)

```bash
cd services/core
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
DATABASE_URL=sqlite+aiosqlite:///./aos_dev.db uvicorn src.main:app --reload --port 8000
# Swagger: http://localhost:8000/docs   |  admin@gdesigner.school / Admin123!
```

## Arrancar com Docker (Postgres + Redis + core)

```bash
cp .env.example .env
docker compose -f infra/docker/docker-compose.yml up -d           # + --profile kafka --profile web
```

## Frontend

```bash
pnpm install
pnpm --filter @aos/web dev      # http://localhost:3000  (NEXT_PUBLIC_API_URL → core)
```

## Testes
```bash
cd services/core && pytest -q
```

## API principal (`/api/v1`)
`/auth/*` · `/users` · `/institutions` · `/roles` · `/notifications` · `/audit-logs` · `/plugins` (+ `/plugins/registry`)
· `/settings` · `/events/{recent,stream,publish}` · `/sis/courses` · `/sis/enrollments` · `/health/{db,redis,kafka}`

## Criar um plugin
Ver [`docs/plugin-development.md`](docs/plugin-development.md) e `plugins/aos-domain-sis` como referência.

Licença MIT.
