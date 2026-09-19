# Desenvolver um plugin AOS

Um plugin é um directório em `plugins/` com um `manifest.json` e um módulo Python com `register(ctx)`.

```
plugins/aos-domain-exemplo/
├── manifest.json
├── __init__.py
├── src/
│   ├── __init__.py
│   ├── plugin.py      # register(ctx)
│   ├── models.py      # SQLAlchemy (herdar de src.models.base.BaseModel)
│   ├── schemas.py     # Pydantic
│   └── routes.py      # APIRouter
├── frontend/          # micro-frontend (opcional)
└── tests/
```

## `register(ctx)` — o contrato

```python
def register(ctx):
    ctx.add_models(Course, Enrollment)     # tabelas entram no metadata → create_all / alembic
    ctx.add_router(router)                 # montado em {API_PREFIX}{manifest.api.prefix}

    @ctx.on_event("auth.user.registered")  # subscrever eventos do Event Bus (wildcards: "sis.*")
    async def handler(event): ...

    @ctx.action("sis.enrollment.after_create")   # hook de notificação
    async def after(enrollment): ...

    @ctx.filter("sis.enrollment.validate", priority=5)  # hook de transformação/veto
    def validate(verdict, course, student_id): return verdict
```

## Convenções
- Eventos: `dominio.entidade.accao` em passado (`sis.student.enrolled`).
- Tabelas: prefixo do domínio (`sis_courses`, `lms_lessons`).
- Permissões: `dominio.recurso.accao` (`lms.grade.manage`), declaradas no manifest.
- Um plugin com erro é marcado `error` e **nunca** derruba o core.
- Dependências entre plugins são resolvidas topologicamente (`dependencies` no manifest).

## Event Bus
`EVENT_BUS_BACKEND=memory|redis|kafka`. Em memória (dev/test) os eventos ficam num mini event-store consultável em
`GET /api/v1/events/recent`; `GET /api/v1/events/stream` expõe SSE para o frontend.
