# 🎓 AOS — Academic Operational System
## Blueprint Arquitetural: O Primeiro Sistema Operacional Acadêmico do Mundo

**Versão:** 1.0  
**Data:** 27 de Agosto de 2026  
**Conceito:** Unificação de LMS, ERP, CRM, CIS, RH, BI, Comunicação e mais, em uma única plataforma extensível via plugins.

---

## 📋 Sumário Executivo

O **AOS** é uma plataforma unificada que transcende a simples integração entre sistemas acadêmicos. Em vez de conectar LMS + ERP + CRM + SIS + RH via APIs pontuais, o AOS os **absorve arquiteturalmente** como **módulos nativos** dentro de um único ecossistema operacional, onde cada funcionalidade é um **plugin** que pode ser ativado, desativado ou substituido sem afetar o core.

A analogia perfeita: se o Windows é um OS para computadores e o Android é um OS para smartphones, o **AOS é o OS para instituições de ensino**.

---

## 1. 🏛️ Visão Arquitetural Geral

### 1.1 Filosofia de Design

O AOS segue cinco princípios fundamentais:

1. **Plugin-First:** Toda funcionalidade — inclusive as nativas — é um plugin. O core é apenas o motor de execução.
2. **Domain-Driven Design (DDD):** Cada domínio acadêmico é um "Bounded Context" com linguagem ubíqua própria.
3. **Event-Driven Core:** O sistema inteiro comunica-se via eventos, garantindo desacoplamento total entre módulos.
4. **Headless by Default:** Backend e frontend são separados. Qualquer interface pode ser construída sobre o AOS.
5. **API-First:** Tudo é uma API. Tudo é documentado. Tudo é testável.

### 1.2 Arquitetura Híbrida: Modular Monolith → Microservices

O AOS adota uma arquitetura **híbrida inteligente**:

```
┌─────────────────────────────────────────────────────────────────┐
│                     AOS — ACADEMIC OPERATIONAL SYSTEM            │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Micro-      │  │  Micro-      │  │  Micro-      │          │
│  │  Frontend    │  │  Frontend    │  │  Frontend    │          │
│  │  (React)     │  │  (Vue)       │  │  (Mobile)    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                   │
│  ┌──────┴─────────────────┴─────────────────┴───────┐           │
│  │              API GATEWAY (Kong / Traefik)         │           │
│  │     Auth │ Rate Limit │ Routing │ Composition     │           │
│  └──────┬─────────────────┬─────────────────┬───────┘           │
│         │                 │                 │                   │
│  ┌──────┴─────────────────┴─────────────────┴───────┐           │
│  │           AOS CORE — Modular Monolith             │           │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ │           │
│  │  │ Plugin  │ │ Plugin  │ │ Plugin  │ │ Plugin │ │           │
│  │  │ Engine  │ │ Event   │ │ Auth    │ │ Config │ │           │
│  │  │ (Core)  │ │ Bus     │ │ (Core)  │ │ (Core) │ │           │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └───┬────┘ │           │
│  │       │           │           │          │      │           │
│  │  ┌────┴───────────┴───────────┴──────────┴────┐ │           │
│  │  │         PLUGIN MANIFEST & REGISTRY           │ │           │
│  │  └─────────────────────────────────────────────┘ │           │
│  └──────────────────────────────────────────────────┘           │
│         │                 │                 │                   │
│  ┌──────┴─────────────────┴─────────────────┴───────┐           │
│  │              PLUGINS / MÓDULOS NATIVOS            │           │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐  │           │
│  │  │  LMS   │ │  SIS   │ │  ERP   │ │   CRM    │  │           │
│  │  │Plugin  │ │Plugin  │ │Plugin  │ │  Plugin  │  │           │
│  │  └────────┘ └────────┘ └────────┘ └──────────┘  │           │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐  │           │
│  │  │   RH   │ │  BI    │ │Comunic.│ │ Bibliot. │  │           │
│  │  │Plugin  │ │Plugin  │ │Plugin  │ │  Plugin  │  │           │
│  │  └────────┘ └────────┘ └────────┘ └──────────┘  │           │
│  └──────────────────────────────────────────────────┘           │
│         │                 │                 │                   │
│  ┌──────┴─────────────────┴─────────────────┴───────┐           │
│  │              INFRAESTRUTURA DE DADOS              │           │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐  │           │
│  │  │PostgreSQL│ │  Kafka │ │  Redis │ │   S3    │  │           │
│  │  │ (Write) │ │(Events)│ │(Cache) │ │(Files)  │  │           │
│  │  └────────┘ └────────┘ └────────┘ └──────────┘  │           │
│  │  ┌────────┐ ┌────────┐ ┌────────┐              │           │
│  │  │Elastic- │ │Click-  │ │MongoDB │              │           │
│  │  │ search  │ │ House  │ │(Logs)  │              │           │
│  │  └────────┘ └────────┘ └────────┘              │           │
│  └──────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

**Por que Modular Monolith + Plugins e não Microservices puros?**

- **Custo operacional:** Um monólito modular custa ~$1.100-2.300/mês vs. $4.200-8.500/mês para microservices
- **Simplicidade de debug:** Uma única codebase, um único deploy
- **Escalabilidade seletiva:** Plugins críticos (ex: exames online) podem ser extraídos para microservices independentes quando necessário
- **Conway's Law:** Times menores trabalham melhor em um monólito bem modularizado

---

## 2. 🧩 Sistema de Plugins: O Coração do AOS

### 2.1 Conceito: "Tudo é Plugin"

Inspirado no **Odoo** (onde cada app é um módulo independente que opera dentro do core) e no **WordPress** (onde hooks actions/filters permitem extensão sem tocar no core), o AOS implementa um **Plugin Engine** que torna TODA funcionalidade um plugin.

**Plugins Nativos (incluídos no core):**
- `aos-core-auth` — Autenticação e autorização
- `aos-core-eventbus` — Barramento de eventos
- `aos-core-config` — Gestão de configurações
- `aos-core-api` — Gateway e composição de APIs
- `aos-core-audit` — Auditoria e logs
- `aos-core-i18n` — Internacionalização
- `aos-core-notify` — Sistema de notificações

**Plugins de Domínio (ativáveis pela instituição):**
- `aos-domain-lms` — Learning Management System
- `aos-domain-sis` — Student Information System
- `aos-domain-erp` — Enterprise Resource Planning (financeiro, tesouraria)
- `aos-domain-crm` — Customer Relationship Management (candidatos, alumni)
- `aos-domain-hr` — Recursos Humanos (docentes, funcionários)
- `aos-domain-bi` — Business Intelligence e dashboards
- `aos-domain-library` — Gestão de biblioteca
- `aos-domain-communication` — SMS, e-mail, push notifications
- `aos-domain-exam` — Exames e avaliações (com OMR)
- `aos-domain-portal` — Portal do aluno/encarregado
- `aos-domain-mobile` — App móvel unificado

### 2.2 Estrutura de um Plugin AOS

Cada plugin segue um contrato estrito:

```
plugin-name/
├── manifest.json          # Metadados, dependências, versão, hooks
├── config/
│   └── settings.yaml      # Configurações default do plugin
├── src/
│   ├── models/            # Entidades DDD (ORM)
│   ├── services/          # Lógica de negócio (Domain Services)
│   ├── repositories/      # Acesso a dados
│   ├── controllers/       # REST API endpoints
│   ├── events/            # Eventos que este plugin emite
│   ├── listeners/         # Eventos que este plugin escuta
│   ├── hooks/             # Hooks do Plugin Engine (actions/filters)
│   ├── policies/          # Regras de autorização
│   └── migrations/        # Migrações de banco de dados
├── frontend/
│   ├── micro-frontend/    # MFE independente (React/Vue/Angular)
│   └── widgets/           # Widgets embeddáveis no dashboard
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
│   └── README.md
└── assets/                # Ícones, imagens, templates
```

### 2.3 Plugin Manifest (manifest.json)

```json
{
  "id": "aos-domain-lms",
  "name": "AOS Learning Management System",
  "version": "3.2.1",
  "author": "AOS Core Team",
  "license": "MIT",
  "type": "domain",
  "dependencies": {
    "core": "^2.0.0",
    "aos-core-auth": "^2.0.0",
    "aos-core-eventbus": "^2.0.0"
  },
  "optional_dependencies": {
    "aos-domain-erp": "^1.5.0"
  },
  "hooks": {
    "actions": [
      "lms.course.created",
      "lms.enrollment.completed",
      "lms.grade.submitted"
    ],
    "filters": [
      "lms.course.content.render",
      "lms.grade.calculation"
    ]
  },
  "events": {
    "publishes": [
      "lms.course.created",
      "lms.enrollment.completed"
    ],
    "subscribes": [
      "auth.user.registered",
      "sis.student.enrolled"
    ]
  },
  "permissions": [
    "lms.course.create",
    "lms.course.edit",
    "lms.grade.manage"
  ],
  "database": {
    "tables": ["lms_courses", "lms_enrollments", "lms_grades"],
    "migrations": "src/migrations/"
  },
  "api": {
    "prefix": "/api/v1/lms",
    "routes": "src/routes.php"
  },
  "frontend": {
    "micro_frontend": {
      "entry": "frontend/micro-frontend/dist/index.js",
      "mount_point": "#aos-lms-app",
      "routes": ["/lms/*"]
    }
  }
}
```

### 2.4 Plugin Engine: Hooks & Event Bus

O AOS implementa um sistema de **hooks** inspirado no WordPress, mas tipado e moderno:

**Actions (Eventos de Notificação):**
```python
# Core emite um evento
aos_event_bus.publish("auth.user.registered", {
    "user_id": 12345,
    "email": "aluno@universidade.ao",
    "role": "student",
    "institution_id": "uan"
})

# Plugin LMS escuta e reage
@aos_hook.action("auth.user.registered")
def create_lms_profile(event):
    user = event.data
    LMSProfile.create(
        user_id=user.id,
        default_language="pt",
        notification_prefs={"email": True, "push": True}
    )
```

**Filters (Transformação de Dados):**
```python
# Plugin ERP filtra o cálculo de mensalidade
@aos_hook.filter("erp.tuition.calculate")
def apply_scholarship_discount(amount, student):
    if student.has_scholarship:
        return amount * 0.7  # 30% desconto
    return amount
```

**Event Bus (Kafka interno):**
- Todos os eventos cruzam o barramento Kafka
- Plugins podem publicar e subscrever eventos de forma assíncrona
- Eventos são persistentes (event sourcing) para auditoria e replay

---

## 3. 🏗️ Domínios (Bounded Contexts) — DDD

O AOS é modelado usando **Domain-Driven Design**, onde cada domínio acadêmico é um "Bounded Context" independente:

### 3.1 Mapa de Contextos

```
┌─────────────────────────────────────────────────────────────┐
│                    AOS BOUNDED CONTEXTS                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐         ┌─────────────┐                  │
│   │   IDENTITY  │◄───────►│    SIS      │                  │
│   │   & ACCESS  │         │  (Student   │                  │
│   │  (Auth/RBAC)│         │  Info Sys)  │                  │
│   └──────┬──────┘         └──────┬──────┘                  │
│          │                       │                          │
│          │    ┌──────────────────┘                          │
│          │    │                                              │
│          ▼    ▼                                              │
│   ┌─────────────┐         ┌─────────────┐                  │
│   │    LMS      │◄───────►│    ERP      │                  │
│   │ (Learning   │         │ (Finance,   │                  │
│   │  Management)│         │  Treasury)  │                  │
│   └──────┬──────┘         └──────┬──────┘                  │
│          │                       │                          │
│          │    ┌──────────────────┘                          │
│          │    │                                              │
│          ▼    ▼                                              │
│   ┌─────────────┐         ┌─────────────┐                  │
│   │    CRM      │◄───────►│    HR       │                  │
│   │ (Admissions,│         │ (Staff,     │                  │
│   │  Alumni)    │         │  Payroll)   │                  │
│   └──────┬──────┘         └──────┬──────┘                  │
│          │                       │                          │
│          │    ┌──────────────────┘                          │
│          │    │                                              │
│          ▼    ▼                                              │
│   ┌─────────────┐         ┌─────────────┐                  │
│   │    BI       │◄───────►│  COMMUNIC.  │                  │
│   │ (Analytics) │         │ (SMS,Email) │                  │
│   └─────────────┘         └─────────────┘                  │
│                                                             │
│   ┌─────────────┐         ┌─────────────┐                  │
│   │   LIBRARY   │         │   EXAM      │                  │
│   │  (Catalog,  │         │  (OMR,      │                  │
│   │  Lending)   │         │  Grading)   │                  │
│   └─────────────┘         └─────────────┘                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Comunicação Entre Contextos

- **Sincrona (dentro do mesmo request):** Via API Gateway composition para leituras que precisam de dados de múltiplos domínios
- **Assíncrona (event-driven):** Via Event Bus (Kafka) para operações que alteram estado

**Exemplo de fluxo cross-domain:**

```
1. Aluno se matricula no SIS
   → SIS publica: "sis.student.enrolled"

2. LMS escuta e cria perfil de aprendizagem
   → LMS publica: "lms.profile.created"

3. ERP escuta e gera fatura de propina
   → ERP publica: "erp.invoice.generated"

4. Communication escuta e envia e-mail de boas-vindas + fatura
   → Communication publica: "communication.email.sent"

5. BI escuta todos os eventos e atualiza dashboards em tempo real
```

---

## 4. ⚡ Arquitetura de Eventos (Event-Driven + CQRS)

### 4.1 Por que Event-Driven?

O AOS usa **Event-Driven Architecture (EDA)** como backbone porque:
- Desacopla totalmente os plugins entre si
- Permite audit trail completo (toda ação é um evento registrado)
- Facilita integrações com sistemas externos
- Suporta processamento assíncrono (ex: geração de relatórios pesados)

### 4.2 CQRS — Command Query Responsibility Segregation

O AOS implementa **CQRS** para separar operações de leitura e escrita:

```
┌─────────────────────────────────────────────────────────────┐
│                        CQRS NO AOS                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐         ┌─────────────┐                  │
│   │   COMMAND   │         │    QUERY    │                  │
│   │    SIDE     │         │    SIDE     │                  │
│   │  (Escrita)  │         │  (Leitura)  │                  │
│   └──────┬──────┘         └──────┬──────┘                  │
│          │                       │                          │
│          ▼                       ▼                          │
│   ┌─────────────┐         ┌─────────────┐                  │
│   │   Event     │         │  Materialized│                  │
│   │   Store     │◄────────│    Views     │                  │
│   │  (Kafka)    │  (sync) │ (PostgreSQL/ │                  │
│   │             │         │  ClickHouse) │                  │
│   └─────────────┘         └─────────────┘                  │
│                                                             │
│   Fluxo de Escrita:                                         │
│   Command → Validação → Evento → Kafka → Event Store        │
│                                                             │
│   Fluxo de Leitura:                                         │
│   Query → Materialized View → Resposta rápida               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Vantagens no contexto acadêmico:**
- **Notas:** Um professor submete notas (command). O aluno consulta o boletim (query) — separados, o query é instantâneo mesmo com milhões de registros.
- **Financeiro:** Pagamentos são commands. Extratos e relatórios são queries sobre views materializadas.
- **Audit:** Todo command gera um evento. O histórico completo de "quem mudou o quê e quando" é reconstruível replayando eventos.

---

## 5. 🎨 Frontend: Micro-Frontends

### 5.1 Arquitetura de Micro-Frontends

Cada plugin de domínio pode trazer seu próprio **micro-frontend**, que é carregado dinamicamente no shell principal:

```
┌─────────────────────────────────────────────────────────────┐
│              AOS SHELL (Host Application)                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Header │ Sidebar │  [Dynamic Content Area]        │   │
│  │         │         │                                │   │
│  │         │         │  ┌────────────────────────┐   │   │
│  │  Auth   │  LMS    │  │  Micro-Frontend        │   │   │
│  │  (Core) │  (MFE)  │  │  do Plugin Ativo       │   │   │
│  │         │         │  │                        │   │   │
│  │  ERP    │  SIS    │  │  React / Vue / Angular │   │   │
│  │  (MFE)  │  (MFE)  │  │  carregado via Module  │   │   │
│  │         │         │  │  Federation / single-spa│   │   │
│  │  CRM    │  BI     │  └────────────────────────┘   │   │
│  │  (MFE)  │  (MFE)  │                                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Tecnologias:**
- **Module Federation 2.0** (Next.js / Webpack) para carregamento runtime
- **single-spa** como meta-framework alternativo
- **Shared Design System:** Componentes UI unificados (botões, tabelas, formulários, modais) compartilhados entre todos os MFEs
- **State compartilhado:** Event Bus no frontend (RxJS ou Zustand) para comunicação entre MFEs

### 5.2 Shell App Responsabilidades

- Autenticação unificada (SSO)
- Menu dinâmico baseado nos plugins ativos e permissões do usuário
- Carregamento lazy de MFEs
- Gestão de tema e i18n global
- Notificações cross-plugin

---

## 6. 🔐 API Gateway

O **API Gateway** é a porta de entrada única para todo o AOS:

**Responsabilidades:**
- **Routing:** Direciona /api/v1/lms/* → Plugin LMS, /api/v1/erp/* → Plugin ERP
- **Authentication:** Valida JWT, verifica sessão, refresh tokens
- **Authorization:** Verifica permissões do RBAC antes de encaminhar
- **Rate Limiting:** Protege contra abuso (ex: 100 req/min por aluno)
- **API Composition:** Agrega dados de múltiplos plugins em uma única resposta
- **Request/Response Transformation:** Converte formatos entre versões de API
- **Caching:** Cache de respostas frequentes (ex: grade curricular)
- **Observability:** Logging, métricas, distributed tracing

**Tecnologias recomendadas:** Kong, Traefik, ou APISIX (open source e de alta performance).

---

## 7. 🗄️ Stack Tecnológico Recomendado

### 7.1 Backend — Core & Plugins

| Camada | Tecnologia | Justificativa |
|--------|-----------|---------------|
| **Linguagem** | Python 3.12+ | Legibilidade, ecossistema vasto, IA/ML nativo |
| **Framework** | FastAPI | Performance (async), auto-documentação OpenAPI, tipagem |
| **ORM** | SQLAlchemy 2.0 | Abstração de banco, suporte a múltiplos DBs |
| **Task Queue** | Celery + Redis | Processamento assíncrono (relatórios, e-mails) |
| **Event Bus** | Apache Kafka | Durabilidade, replay, alta vazão de eventos |
| **Cache** | Redis | Sessões, cache de queries, rate limiting |
| **Search** | Elasticsearch | Busca full-text em cursos, alunos, documentos |
| **Analytics** | ClickHouse | OLAP para dashboards e relatórios em tempo real |
| **Files** | MinIO (S3-compatível) | Armazenamento de documentos, vídeos, provas |

**Alternativa em PHP (para desenvolvedores PHP):**
- Laravel 11 + Filament (admin) + Laravel Modules (plugin system) + Laravel Horizon (queues)
- Inspirado no LAVSMS e no Moodle (ambos PHP)

**Alternativa em Java (para universidades enterprise):**
- Spring Boot + Spring Modulith (modular monolith) + Spring Cloud Gateway

### 7.2 Frontend

| Camada | Tecnologia |
|--------|-----------|
| **Shell** | Next.js 14 (App Router) |
| **MFEs** | React 18 + Module Federation |
| **Mobile** | Flutter (app nativo unificado) |
| **Design System** | Tailwind CSS + shadcn/ui |
| **State Management** | Zustand (shell) + React Query (MFEs) |
| **Charts** | Apache ECharts |

### 7.3 Banco de Dados

| Tipo | Tecnologia | Uso |
|------|-----------|-----|
| **Relacional (Write)** | PostgreSQL 16 | Dados transacionais, event store |
| **Relacional (Read)** | PostgreSQL 16 (réplicas) | Views materializadas, queries |
| **Documentos** | MongoDB | Logs, configs dinâmicas, schemas flexíveis |
| **Time-Series** | ClickHouse | Analytics, métricas, eventos agregados |
| **Search** | Elasticsearch | Busca em conteúdo, alunos, documentos |
| **Cache** | Redis | Sessões, cache, pub/sub real-time |

### 7.4 DevOps & Infraestrutura

| Componente | Tecnologia |
|-----------|-----------|
| **Container** | Docker + Docker Compose (dev) / Kubernetes (prod) |
| **CI/CD** | GitHub Actions / GitLab CI |
| **Monitoramento** | Prometheus + Grafana |
| **Logging** | ELK Stack (Elasticsearch, Logstash, Kibana) |
| **Tracing** | Jaeger / OpenTelemetry |
| **Docs API** | OpenAPI 3.0 + Swagger UI (auto-gerado pelo FastAPI) |

---

## 8. 🧬 Padrões de Design Críticos

### 8.1 Plugin Engine — Hook System (WordPress-style, tipado)

```python
# Core: Plugin Engine
class AOSPluginEngine:
    def __init__(self):
        self._actions: dict[str, list[Callable]] = {}
        self._filters: dict[str, list[Callable]] = {}

    def add_action(self, hook: str, callback: Callable, priority: int = 10):
        self._actions.setdefault(hook, []).append((priority, callback))
        self._actions[hook].sort(key=lambda x: x[0])

    def do_action(self, hook: str, *args, **kwargs):
        for priority, callback in self._actions.get(hook, []):
            callback(*args, **kwargs)

    def add_filter(self, hook: str, callback: Callable, priority: int = 10):
        self._filters.setdefault(hook, []).append((priority, callback))
        self._filters[hook].sort(key=lambda x: x[0])

    def apply_filters(self, hook: str, value, *args, **kwargs):
        for priority, callback in self._filters.get(hook, []):
            value = callback(value, *args, **kwargs)
        return value

# Uso em um Plugin
engine = AOSPluginEngine()

# Plugin LMS registra uma ação
engine.add_action("auth.user.registered", create_lms_profile, priority=10)

# Plugin ERP registra um filtro
engine.add_filter("erp.tuition.calculate", apply_discount, priority=5)
```

### 8.2 Event Bus — Pub/Sub com Kafka

```python
# Core: Event Bus
class AOSEventBus:
    def publish(self, event_type: str, payload: dict, metadata: dict = None):
        event = AOSEvent(
            id=uuid4(),
            type=event_type,
            payload=payload,
            metadata=metadata or {},
            timestamp=datetime.utcnow(),
            version="1.0"
        )
        kafka_producer.send("aos.events", event.to_json())

    def subscribe(self, event_types: list[str], handler: Callable):
        consumer = kafka_consumer.subscribe("aos.events")
        for msg in consumer:
            event = AOSEvent.from_json(msg.value)
            if event.type in event_types:
                handler(event)

# Plugin SIS publica
bus.publish("sis.student.enrolled", {
    "student_id": "STU-2026-001",
    "course_id": "CS-101",
    "semester": "2026.1"
})

# Plugin ERP escuta e reage
@bus.subscribe(["sis.student.enrolled"])
def generate_invoice(event):
    student = event.payload["student_id"]
    course = event.payload["course_id"]
    InvoiceService.generate(student, course)
```

### 8.3 CQRS — Separando Command e Query

```python
# COMMAND SIDE (Escrita)
class EnrollStudentCommand:
    student_id: str
    course_id: str
    semester: str

class EnrollStudentHandler:
    def handle(self, cmd: EnrollStudentCommand):
        # Validações de negócio
        if not self._can_enroll(cmd.student_id, cmd.course_id):
            raise DomainError("Pré-requisitos não atendidos")

        # Cria evento
        event = StudentEnrolledEvent(
            student_id=cmd.student_id,
            course_id=cmd.course_id,
            semester=cmd.semester,
            enrolled_at=datetime.utcnow()
        )

        # Persiste no Event Store
        self.event_store.append(event)

        # Publica no bus
        self.event_bus.publish("sis.student.enrolled", event.to_dict())

# QUERY SIDE (Leitura)
class StudentEnrollmentQuery:
    def get_enrollments(self, student_id: str) -> list[EnrollmentView]:
        # Lê diretamente da Materialized View (PostgreSQL réplica)
        return self.read_db.query(
            "SELECT course_id, semester, status, enrolled_at "
            "FROM mv_student_enrollments WHERE student_id = %s",
            student_id
        )
```

### 8.4 Micro-Frontend — Module Federation

```javascript
// Shell App (Next.js) — webpack.config.js
const { NextFederationPlugin } = require("@module-federation/nextjs-mf");

module.exports = {
  webpack(config, options) {
    config.plugins.push(
      new NextFederationPlugin({
        name: "aos_shell",
        remotes: {
          lms: "aos_lms@https://lms.universidade.ao/_next/static/chunks/remoteEntry.js",
          erp: "aos_erp@https://erp.universidade.ao/_next/static/chunks/remoteEntry.js",
          sis: "aos_sis@https://sis.universidade.ao/_next/static/chunks/remoteEntry.js",
        },
        shared: ["react", "react-dom", "tailwindcss"],
      })
    );
    return config;
  },
};

// Shell App — pages/lms/[...slug].tsx
import dynamic from "next/dynamic";

const LMSApp = dynamic(() => import("lms/App"), { ssr: false });

export default function LMSPage() {
  return <LMSApp />;
}
```

---

## 9. 📦 Exemplo de Plugin Completo: aos-domain-exam

Este plugin implementa o sistema de exames com correção OMR (inspirado no SIGA de Angola):

```
aos-domain-exam/
├── manifest.json
├── src/
│   ├── models/
│   │   ├── exam.py              # Entidade: Prova
│   │   ├── question.py          # Entidade: Questão
│   │   ├── answer_sheet.py      # Entidade: Folha de Resposta
│   │   └── grade.py             # Entidade: Nota
│   ├── services/
│   │   ├── exam_service.py      # Criar provas, agendar
│   │   ├── omr_service.py       # Leitura óptica de folhas
│   │   └── grading_service.py   # Cálculo de notas
│   ├── events/
│   │   ├── exam_scheduled.py
│   │   ├── answer_sheet_scanned.py
│   │   └── grade_published.py
│   ├── listeners/
│   │   └── on_student_enrolled.py  # Auto-inscreve em provas obrigatórias
│   ├── hooks/
│   │   └── filters.py           # Filtros: cálculo de nota, critérios
│   ├── controllers/
│   │   └── exam_controller.py   # REST API
│   └── migrations/
│       └── 001_create_exams.py
├── frontend/
│   ├── micro-frontend/
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── ExamBuilder.tsx
│   │   │   │   ├── OMRScanner.tsx
│   │   │   │   └── GradeDashboard.tsx
│   │   │   └── App.tsx
│   │   └── package.json
│   └── widgets/
│       └── upcoming-exams.tsx   # Widget para o dashboard
└── tests/
    └── test_omr_service.py
```

**Eventos emitidos:**
- `exam.scheduled` → BI atualiza calendário, Communication envia lembrete
- `answer_sheet.scanned` → OMR processa, Grade calcula, SIS registra
- `grade.published` → Portal do Aluno notifica, ERP verifica inadimplência

---

## 10. 🚀 Roadmap de Desenvolvimento (18 meses)

### Fase 1 — Fundação (Meses 1-3)
- [ ] AOS Core: Plugin Engine, Event Bus, Auth, Config
- [ ] API Gateway com routing dinâmico por plugin
- [ ] Shell App com carregamento de MFEs
- [ ] Plugin `aos-domain-auth` (SSO, RBAC, LDAP, OAuth2, SAML)
- [ ] Plugin `aos-domain-sis` (cadastro de alunos, matrículas, turmas)
- [ ] Plugin `aos-domain-portal` (portal do aluno básico)

### Fase 2 — Domínios Core (Meses 4-7)
- [ ] Plugin `aos-domain-lms` (cursos, conteúdo, entrega, SCORM/xAPI)
- [ ] Plugin `aos-domain-erp` (propinas, mensalidades, boletos, contas)
- [ ] Plugin `aos-domain-exam` (provas, OMR, pautas, certificados)
- [ ] Plugin `aos-domain-hr` (docentes, funcionários, folha)
- [ ] Plugin `aos-domain-communication` (SMS, e-mail, push)

### Fase 3 — Expansão (Meses 8-12)
- [ ] Plugin `aos-domain-crm` (admissões, candidatos, alumni)
- [ ] Plugin `aos-domain-bi` (dashboards, relatórios, analytics)
- [ ] Plugin `aos-domain-library` (biblioteca, repositório digital)
- [ ] Plugin `aos-domain-mobile` (app nativo Flutter)
- [ ] Plugin `aos-domain-event` (concursos, inscrições com pagamento)

### Fase 4 — Escala & Ecosistema (Meses 13-18)
- [ ] Marketplace de Plugins (instalação 1-clique)
- [ ] AI Plugin: Tutor virtual, correção automática, predição de evasão
- [ ] Blockchain Plugin: Certificação digital verificável
- [ ] Extração de plugins críticos para microservices independentes
- [ ] Certificações de segurança (ISO 27001, LGPD/GDPR)

---

## 11. 💰 Estimativa de Custo de Infraestrutura

### Fase Inicial (até 1.000 usuários simultâneos)

| Componente | Especificação | Custo Mensal |
|-----------|--------------|-------------|
| App Server | 2x VPS 8vCPU/16GB | $200 |
| Database | PostgreSQL 16 managed | $150 |
| Kafka | 3x nodes managed | $200 |
| Redis | Managed cache | $50 |
| Storage | 500GB S3-compatible | $25 |
| Monitoring | Prometheus + Grafana | $50 |
| **Total** | | **~$675/mês** |

### Escala Média (5.000-10.000 usuários)

| Componente | Especificação | Custo Mensal |
|-----------|--------------|-------------|
| App Cluster | 4x VPS 16vCPU/32GB + LB | $800 |
| Database | PostgreSQL HA (primary + 2 réplicas) | $600 |
| Kafka | 5x nodes | $500 |
| Redis | Cluster 3x | $150 |
| Elasticsearch | 3x nodes | $400 |
| ClickHouse | 2x nodes | $300 |
| Storage | 5TB | $100 |
| CDN | Cloudflare Pro | $20 |
| **Total** | | **~$2.870/mês** |

---

## 12. 🎯 Diferenciais Competitivos do AOS

1. **Plugin-First:** Nenhum outro sistema acadêmico no mundo é 100% plugin-based. O Odoo é modular, mas não é acadêmico. O Moodle tem plugins, mas não é unificado.
2. **Event Sourcing Nativo:** Todo histórico é reconstruível. Auditoria completa desde o primeiro dia.
3. **Headless + Micro-Frontends:** Cada instituição pode ter uma UI 100% customizada sem tocar no backend.
4. **CQRS:** Leituras instantâneas mesmo com milhões de registros.
5. **Unificação Real:** LMS, SIS, ERP, CRM, RH, BI, Comunicação — tudo nativo, não integrado.
6. **Código Aberto:** Core open source, com plugins comerciais opcionais (modelo Odoo/WordPress).
7. **Mobile-Native:** App único para todas as instituições que usam o AOS (modelo SIGA mobile).
8. **IA-Native:** Arquitetura preparada para LLMs desde o início (RAG, agentes, predição).

---

## 13. 📚 Referências Arquiteturais

- **Odoo Modular Architecture:** Cada módulo opera independentemente, mas integra-se nativamente
- **WordPress Hook System:** Event-driven architecture com actions e filters para extensibilidade máxima
- **Salesforce Metadata-Driven:** Abstração via metadados permite extensão sem reescrever o core
- **OpenEdX Plugin Architecture:** Django apps como plugins com `plugin_app` dict
- **Modular Monolith:** Shopify prova que monolitos modulares escalam a bilhões de transações
- **CQRS + Event Sourcing:** Padrão Microsoft Azure para audit trail e reconstrução de estado
- **Micro-Frontends:** Module Federation 2.0 permite carregar apps independentes em runtime

---

## 14. 🏁 Conclusão

O **AOS** não é apenas mais um sistema de gestão acadêmica. É uma **nova categoria de software** — o primeiro **Sistema Operacional Acadêmico** do mundo. Ao unificar LMS, ERP, SIS, CRM, RH, BI e Comunicação em uma única plataforma nativamente extensível via plugins, o AOS elimina a fragmentação que assola as instituições de ensino há décadas.

A arquitetura híbrida (modular monolith + event-driven + CQRS + micro-frontends) oferece o equilíbrio perfeito entre simplicidade operacional, escalabilidade futura e extensibilidade ilimitada. Cada instituição ativa apenas os plugins que precisa, paga apenas pelo que usa, e pode estender o sistema sem limites.

**O AOS é o Android do ensino.**
