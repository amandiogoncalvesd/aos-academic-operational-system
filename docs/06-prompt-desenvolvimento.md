
# Parte 1 - Introdução e estrutura
part1 = '''# PROMPT DE DESENVOLVIMENTO — AOS (Academic Operational System)
# Sistema Operacional Acadêmico da G Designer School
# Instrução: Execute cada linha deste documento na ordem exata. Não pule nenhuma etapa.

================================================================================
SEÇÃO 0 — DEFINIÇÃO DO SISTEMA
================================================================================

O AOS (Academic Operational System) é o primeiro sistema operacional acadêmico do mundo.
Ele unifica em uma única plataforma: LMS (Learning Management System), SIS (Student Information System),
ERP (Enterprise Resource Planning), CRM (Customer Relationship Management), RH (Recursos Humanos),
BI (Business Intelligence), Comunicação, Biblioteca e Dublagem Automática via IA (S2ST).

Cada funcionalidade do AOS é um plugin independente que se comunica com o core via Event Bus.
O sistema é headless: backend separado do frontend. O frontend é uma Single Page Application (SPA)
com micro-frontends carregados dinamicamente.

Arquitetura técnica:
- Backend: Python 3.12 + FastAPI + SQLAlchemy 2.0 + Celery + Apache Kafka + Redis
- Frontend: Next.js 14 (App Router) + React 18 + TypeScript + Tailwind CSS
- Mobile: Flutter
- Banco de dados: PostgreSQL 16 (primário), Redis (cache/sessões), ClickHouse (analytics)
- Infraestrutura: Docker + Docker Compose (dev) / Kubernetes (prod)
- Repositório: Monorepo com Turborepo

================================================================================
SEÇÃO 1 — ESTRUTURA DE DIRETÓRIOS E ARQUIVOS INICIAIS
================================================================================

ETAPA 1.1 — Criar estrutura raiz do monorepo
--------------------------------------------------------------------------------
Criar os seguintes diretórios vazios na raiz do projeto:

aos/
├── apps/
│   ├── web/
│   ├── mobile/
│   └── docs/
├── packages/
│   ├── ui/
│   ├── config/
│   ├── types/
│   ├── utils/
│   ├── api-client/
│   └── icons/
├── plugins/
│   ├── aos-core-auth/
│   ├── aos-core-eventbus/
│   ├── aos-core-config/
│   ├── aos-core-api/
│   ├── aos-core-audit/
│   ├── aos-core-i18n/
│   ├── aos-core-notify/
│   ├── aos-domain-lms/
│   ├── aos-domain-sis/
│   ├── aos-domain-erp/
│   ├── aos-domain-crm/
│   ├── aos-domain-hr/
│   ├── aos-domain-bi/
│   ├── aos-domain-library/
│   ├── aos-domain-communication/
│   ├── aos-domain-exam/
│   ├── aos-domain-portal/
│   ├── aos-domain-mobile/
│   └── aos-domain-s2st/
├── services/
│   ├── core/
│   ├── gateway/
│   └── workers/
├── infra/
│   ├── terraform/
│   ├── kubernetes/
│   └── docker/
└── docs/

ETAPA 1.2 — Arquivos de configuração raiz
--------------------------------------------------------------------------------
Criar os seguintes arquivos na raiz (aos/):

1. package.json — com scripts: dev, build, lint, test, clean. Dependências: turbo, pnpm-workspace.
2. turbo.json — com pipelines para build, dev, lint, test, com cache habilitado.
3. pnpm-workspace.yaml — listando todos os apps, packages e plugins como workspaces.
4. .gitignore — padrão Node.js + Python + Flutter + Docker + Terraform.
5. README.md — descrição do projeto, instruções de setup, arquitetura.
6. LICENSE — MIT License.
7. .nvmrc — especificando Node.js 20.
8. .python-version — especificando Python 3.12.

ETAPA 1.3 — Configurações compartilhadas (packages/config/)
--------------------------------------------------------------------------------
Criar os seguintes arquivos em packages/config/:

1. packages/config/package.json — nome: @aos/config, versão: 0.0.1, main: index.js.
2. packages/config/eslint/index.js — configuração ESLint para React + TypeScript + Next.js + Prettier.
3. packages/config/prettier/index.js — configuração Prettier: singleQuote: true, semi: true, tabWidth: 2, trailingComma: all.
4. packages/config/tailwind/tailwind.config.ts — configuração Tailwind CSS com content apontando para todos os apps e packages.
5. packages/config/tsconfig/base.json — tsconfig base com strict: true, esModuleInterop: true, skipLibCheck: true.
6. packages/config/tsconfig/nextjs.json — extendendo base.json com jsx: preserve, moduleResolution: bundler.
7. packages/config/tsconfig/react-library.json — extendendo base.json para bibliotecas React.
'''

with open('/mnt/agents/output/AOS_Prompt_Desenvolvimento.md', 'w', encoding='utf-8') as f:
    f.write(part1)

print("Parte 1 salva")

part2 = '''
================================================================================
SEÇÃO 2 — BACKEND — AOS CORE
================================================================================

ETAPA 2.1 — Estrutura do backend (services/core/)
--------------------------------------------------------------------------------
Criar os seguintes diretórios em services/core/:

services/core/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── services/
│   ├── dependencies/
│   ├── middleware/
│   ├── utils/
│   └── plugins/
├── tests/
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
├── Dockerfile
├── requirements.txt
└── pyproject.toml

ETAPA 2.2 — Arquivos do backend core (62 arquivos)
--------------------------------------------------------------------------------
Criar os seguintes arquivos em services/core/src/:

1. config.py — classe Settings com pydantic-settings. Variáveis: DATABASE_URL, REDIS_URL, KAFKA_BOOTSTRAP_SERVERS, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, CORS_ORIGINS, ENVIRONMENT.

2. database.py — engine SQLAlchemy async (create_async_engine), AsyncSessionLocal, get_db() dependency, Base declarativa.

3. main.py — aplicação FastAPI com lifespan context manager. Inclui: CORS middleware, rate limiter (SlowAPI), exception handlers, inclusão de routers.

4. models/__init__.py — importa todos os models.
5. models/base.py — Base declarativa com created_at, updated_at, id (UUID).
6. models/user.py — Model User com: id, email, password_hash, first_name, last_name, avatar_url, is_active, is_verified, last_login, role (enum: student, teacher, coordinator, admin, secretary, librarian, hr, parent, guest), institution_id, created_at, updated_at.
7. models/institution.py — Model Institution com: id, name, slug, logo_url, primary_color, secondary_color, domain, settings (JSON), is_active, plan (enum: free, basic, pro, enterprise), created_at, updated_at.
8. models/role.py — Model Role com: id, name, permissions (JSON), institution_id, is_system_role.
9. models/permission.py — Model Permission com: id, resource, action, description.
10. models/session.py — Model Session com: id, user_id, token, refresh_token, ip_address, user_agent, expires_at, created_at.
11. models/audit_log.py — Model AuditLog com: id, user_id, action, resource, resource_id, old_values, new_values, ip_address, user_agent, created_at.
12. models/notification.py — Model Notification com: id, user_id, type, title, message, data (JSON), is_read, read_at, created_at.
13. models/plugin.py — Model Plugin com: id, name, slug, version, description, author, is_active, is_system, config (JSON), permissions (JSON), created_at, updated_at.
14. models/setting.py — Model Setting com: id, key, value, type, institution_id, plugin_id, is_encrypted.
15. schemas/__init__.py — importa todos os schemas.
16. schemas/user.py — Pydantic schemas: UserCreate, UserUpdate, UserResponse, UserLogin, UserPasswordChange, UserPasswordReset.
17. schemas/token.py — Pydantic schemas: Token, TokenPayload, RefreshToken.
18. schemas/institution.py — Pydantic schemas: InstitutionCreate, InstitutionUpdate, InstitutionResponse.
19. schemas/notification.py — Pydantic schemas: NotificationCreate, NotificationUpdate, NotificationResponse.
20. schemas/audit_log.py — Pydantic schemas: AuditLogCreate, AuditLogResponse, AuditLogFilter.
21. schemas/common.py — Pydantic schemas: PaginationParams, PaginatedResponse, ErrorResponse, SuccessResponse.
22. routers/__init__.py — função include_routers(app) que registra todos os routers.
23. routers/auth.py — endpoints: POST /auth/register, POST /auth/login, POST /auth/refresh, POST /auth/logout, POST /auth/forgot-password, POST /auth/reset-password, POST /auth/verify-email, GET /auth/me, PUT /auth/me, POST /auth/change-password.
24. routers/users.py — endpoints: GET /users, GET /users/{id}, PUT /users/{id}, DELETE /users/{id}, POST /users/bulk-import, GET /users/export.
25. routers/institutions.py — endpoints: GET /institutions, POST /institutions, GET /institutions/{id}, PUT /institutions/{id}, DELETE /institutions/{id}, GET /institutions/{id}/settings, PUT /institutions/{id}/settings.
26. routers/roles.py — endpoints: GET /roles, POST /roles, GET /roles/{id}, PUT /roles/{id}, DELETE /roles/{id}, GET /roles/{id}/permissions.
27. routers/notifications.py — endpoints: GET /notifications, GET /notifications/unread-count, POST /notifications/{id}/read, POST /notifications/read-all, DELETE /notifications/{id}.
28. routers/audit_logs.py — endpoints: GET /audit-logs, GET /audit-logs/{id}, GET /audit-logs/export.
29. routers/plugins.py — endpoints: GET /plugins, POST /plugins/install, POST /plugins/{id}/activate, POST /plugins/{id}/deactivate, DELETE /plugins/{id}, GET /plugins/{id}/config, PUT /plugins/{id}/config.
30. routers/settings.py — endpoints: GET /settings, GET /settings/{key}, PUT /settings/{key}, DELETE /settings/{key}, POST /settings/bulk-update.
31. routers/health.py — endpoints: GET /health, GET /health/db, GET /health/redis, GET /health/kafka.
32. services/__init__.py.
33. services/auth_service.py — funções: register_user, authenticate_user, create_access_token, create_refresh_token, verify_token, revoke_token, reset_password, verify_email.
34. services/user_service.py — funções: get_users, get_user_by_id, create_user, update_user, delete_user, bulk_import_users, export_users.
35. services/notification_service.py — funções: create_notification, get_user_notifications, mark_as_read, mark_all_as_read, delete_notification.
36. services/audit_service.py — funções: log_action, get_audit_logs, export_audit_logs.
37. services/plugin_service.py — funções: get_plugins, install_plugin, activate_plugin, deactivate_plugin, uninstall_plugin, get_plugin_config, update_plugin_config.
38. services/setting_service.py — funções: get_settings, get_setting, set_setting, delete_setting, bulk_update_settings.
39. dependencies/__init__.py.
40. dependencies/auth.py — funções: get_current_user, get_current_active_user, require_role(roles), require_permission(resource, action).
41. dependencies/database.py — função: get_db() -> AsyncSession.
42. dependencies/rate_limit.py — configuração de rate limiting por endpoint.
43. middleware/__init__.py.
44. middleware/correlation.py — middleware que adiciona correlation-id a cada request.
45. middleware/timing.py — middleware que loga tempo de resposta de cada request.
46. middleware/audit.py — middleware que loga automaticamente actions em audit_log.
47. utils/__init__.py.
48. utils/security.py — funções: hash_password, verify_password, generate_random_token, generate_otp.
49. utils/email.py — função: send_email(to, subject, template, context) usando SMTP ou SendGrid.
50. utils/sms.py — função: send_sms(phone, message) usando Twilio ou gateway local.
51. utils/pagination.py — função: paginate(query, page, page_size) -> PaginatedResponse.
52. utils/file.py — funções: save_upload_file, validate_file_type, generate_file_url.
53. utils/i18n.py — funções: get_locale, translate_key, set_locale.
54. plugins/__init__.py — função: load_plugins() que carrega plugins dinamicamente.
55. plugins/engine.py — PluginEngine: add_action, do_action, add_filter, apply_filters.
56. plugins/loader.py — função: discover_plugins(), load_plugin_manifest(), validate_plugin(), register_plugin().
57. plugins/manifest.py — dataclass PluginManifest com: id, name, version, author, dependencies, hooks, events, permissions, database, api, frontend.
58. requirements.txt — listando: fastapi, uvicorn, sqlalchemy[asyncio], asyncpg, alembic, pydantic, pydantic-settings, python-jose, passlib, bcrypt, celery, redis, kafka-python, python-multipart, email-validator, slowapi, httpx, pytest, pytest-asyncio.
59. Dockerfile — imagem Python 3.12 slim, instala dependências, expõe porta 8000, comando: uvicorn src.main:app --host 0.0.0.0 --port 8000.
60. pyproject.toml — configuração do projeto Python com poetry ou setuptools.
61. alembic.ini — configuração do Alembic apontando para services/core/src.
62. alembic/env.py — script de ambiente do Alembic com suporte a async.
'''

with open('/mnt/agents/output/AOS_Prompt_Desenvolvimento.md', 'a', encoding='utf-8') as f:
    f.write(part2)

print("Parte 2 salva")

part3 = '''
================================================================================
SEÇÃO 3 — FRONTEND — NEXT.JS APP (apps/web/)
================================================================================

ETAPA 3.1 — Estrutura do app web
--------------------------------------------------------------------------------
Criar os seguintes diretórios em apps/web/:

apps/web/
├── src/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   ├── stores/
│   ├── types/
│   └── styles/
├── public/
├── tests/
├── .env.local
├── .env.production
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── package.json

ETAPA 3.2 — Configuração do Next.js
--------------------------------------------------------------------------------
Criar os seguintes arquivos em apps/web/:

1. package.json — dependências: next, react, react-dom, typescript, tailwindcss, @aos/ui, @aos/types, @aos/utils, @aos/api-client, zustand, react-query, axios, date-fns, react-hook-form, zod, @hookform/resolvers, clsx, tailwind-merge, lucide-react.
2. next.config.js — configuração com output: standalone, images: { domains: [] }, experimental: { appDir: true }, async redirects() e async rewrites().
3. tailwind.config.ts — extendendo packages/config/tailwind, content apontando para src/**/*.{js,ts,jsx,tsx}.
4. tsconfig.json — extendendo packages/config/tsconfig/nextjs.json.
5. .env.local — variáveis: NEXT_PUBLIC_API_URL=http://localhost:8000, NEXT_PUBLIC_APP_NAME=AOS, NEXT_PUBLIC_APP_VERSION=1.0.0.
6. .env.production — variáveis de produção.

ETAPA 3.3 — App Router e Layouts
--------------------------------------------------------------------------------
Criar os seguintes arquivos em apps/web/src/app/:

1. layout.tsx — RootLayout com: providers (QueryClient, Theme, Auth), fontes (Inter), metadata, html lang="pt".
2. globals.css — Tailwind directives, CSS custom properties, dark mode support.
3. loading.tsx — Root loading com Suspense boundary.
4. error.tsx — Root error boundary.
5. not-found.tsx — Página 404.
6. (auth)/layout.tsx — Layout de autenticação (sem sidebar, centralizado).
7. (auth)/login/page.tsx — Página de login com formulário: email, password, lembrar-me, link esqueci senha, link registrar, botões de login social (Google, Microsoft).
8. (auth)/login/loading.tsx — Skeleton da página de login.
9. (auth)/register/page.tsx — Página de registro com formulário: first_name, last_name, email, password, confirm_password, institution_code (opcional), checkbox termos.
10. (auth)/forgot-password/page.tsx — Página de recuperação de senha com campo email.
11. (auth)/reset-password/[token]/page.tsx — Página de redefinição de senha com campos nova senha e confirmação.
12. (auth)/verify-email/[token]/page.tsx — Página de verificação de email.
13. (auth)/mfa/page.tsx — Página de verificação 2FA com campo código.
14. (dashboard)/layout.tsx — Layout do dashboard com: Sidebar, TopBar, BottomBar (mobile), Content area, CommandPalette (CMD+K).
15. (dashboard)/loading.tsx — Skeleton do dashboard.
16. (dashboard)/page.tsx — Página raiz do dashboard que redireciona para /dashboard/{role} baseado no papel do usuário autenticado.

ETAPA 3.4 — Portal do Aluno (apps/web/src/app/(dashboard)/student/)
--------------------------------------------------------------------------------
Criar os seguintes arquivos:

1. layout.tsx — Layout do portal do aluno com sidebar específica.
2. page.tsx — Dashboard do aluno. Deve conter: saudação personalizada, próxima aula (com horário e sala), tarefas pendentes (contador e lista), média geral atual, frequência mensal (percentual), resumo financeiro (propinas pendentes), avisos recentes, mini calendário com eventos, progresso no curso (percentual concluído).
3. loading.tsx — Skeleton do dashboard do aluno.
4. courses/page.tsx — Lista de cursos matriculados. Cada card deve mostrar: nome do curso, professor, progresso (%), próxima aula, nota atual, status (ativo, concluído, trancado).
5. courses/loading.tsx — Skeleton da lista de cursos.
6. courses/[courseId]/page.tsx — Página do curso. Tabs: Visão Geral, Conteúdo, Tarefas, Notas, Fórum, Colegas. Visão Geral mostra: descrição, professor, carga horária, datas, progresso.
7. courses/[courseId]/layout.tsx — Layout com tabs de navegação do curso.
8. courses/[courseId]/content/page.tsx — Lista de módulos e aulas. Cada aula mostra: título, duração, tipo (vídeo, pdf, quiz), status (concluído, pendente, bloqueado).
9. courses/[courseId]/content/[lessonId]/page.tsx — Página da aula. Deve conter: player de vídeo, seletor de idioma de áudio, transcrição com busca, lista de materiais (PDFs, links), quiz inline (se houver), área de anotações sincronizadas com timestamp, discussão da aula, botão "Marcar como concluído".
10. courses/[courseId]/assignments/page.tsx — Lista de tarefas do curso. Cada tarefa mostra: título, data de entrega, status (pendente, entregue, atrasado), nota (se avaliada).
11. courses/[courseId]/assignments/[assignmentId]/page.tsx — Detalhe da tarefa. Deve conter: descrição, critérios de avaliação, anexos do professor, área de entrega (upload de arquivo ou editor de texto), status da entrega, nota e feedback (se publicado).
12. courses/[courseId]/grades/page.tsx — Notas do curso. Tabela com: avaliação, nota, peso, data, média da turma. Gráfico de evolução.
13. courses/[courseId]/forum/page.tsx — Fórum de discussão do curso. Lista de tópicos com: título, autor, respostas, última atividade, fixado (pinned).
14. courses/[courseId]/forum/[topicId]/page.tsx — Tópico do fórum. Mostra: título, conteúdo, autor, respostas aninhadas, botão responder, curtir.
15. courses/[courseId]/classmates/page.tsx — Lista de colegas de turma. Card com: foto, nome, email (se permitido), botão mensagem.
16. schedule/page.tsx — Horário semanal do aluno. Visualização em calendário (segunda a sábado). Cada aula mostra: disciplina, professor, sala, horário. Marcadores de provas e eventos.
17. grades/page.tsx — Boletim completo. Tabela com todas as disciplinas do semestre. Colunas: disciplina, T1, T2, T3, Média, Status. Gráfico de evolução do GPA. Botão download histórico.
18. finance/page.tsx — Financeiro do aluno. Lista de faturas com: referência, valor, vencimento, status (pago, pendente, atrasado), método de pagamento. Botão pagar (integração). Histórico de pagamentos.
19. documents/page.tsx — Documentos do aluno. Lista com: tipo (atestado, declaração, certificado), data de emissão, status, botão download. Formulário de solicitação de novo documento.
20. messages/page.tsx — Mensagens. Lista de conversas à esquerda. Janela de chat à direita. Campo de nova mensagem. Upload de anexo.
21. messages/[conversationId]/page.tsx — Conversa específica.
22. notifications/page.tsx — Central de notificações. Lista com filtros: todas, não lidas, importantes. Cada notificação mostra: ícone, título, mensagem, data, botão marcar como lida.
23. profile/page.tsx — Perfil do aluno. Seções: informações pessoais (editável), informações acadêmicas (curso, turma, matrícula), contatos de emergência, alterar senha, configuração 2FA, log de atividades.
24. settings/page.tsx — Configurações. Seções: tema (claro/escuro/sistema), idioma da interface, notificações (email, push, sms), acessibilidade (tamanho da fonte, alto contraste, reduzir movimento), privacidade.

ETAPA 3.5 — Portal do Professor (apps/web/src/app/(dashboard)/teacher/)
--------------------------------------------------------------------------------
Criar os seguintes arquivos:

1. layout.tsx — Layout do portal do professor.
2. page.tsx — Dashboard do professor. Widgets: turmas de hoje (com horário e sala), trabalhos para avaliar (contador), resumo de frequência das turmas, mensagens de alunos, horário da semana.
3. classes/page.tsx — Lista de turmas do professor. Card com: nome da turma, disciplina, número de alunos, próxima aula, progresso do conteúdo.
4. classes/[classId]/page.tsx — Página da turma. Tabs: Visão Geral, Alunos, Conteúdo, Notas, Frequência, Fórum, Tarefas.
5. classes/[classId]/students/page.tsx — Lista de alunos da turma. Tabela com: foto, nome, matrícula, email, frequência (%), média, status. Busca e filtros.
6. classes/[classId]/students/[studentId]/page.tsx — Perfil do aluno na turma. Mostra: dados pessoais, frequência detalhada, notas, tarefas entregues, observações do professor.
7. classes/[classId]/content/page.tsx — Gerenciar conteúdo da turma. Lista de módulos/aulas. Botão: criar aula, upload de vídeo, criar quiz, criar tarefa, upload de material. Drag-and-drop para reordenar.
8. classes/[classId]/content/create-lesson/page.tsx — Formulário de criação de aula. Campos: título, descrição, vídeo (upload ou URL), materiais (upload múltiplo), quiz (construtor), visibilidade (imediata ou agendada).
9. classes/[classId]/grades/page.tsx — Lançar notas. Planilha tipo Excel com: aluno (linhas) x avaliações (colunas). Células editáveis inline. Fórmulas automáticas (média ponderada). Color coding (verde >= 10, amarelo 7-9.9, vermelho < 7). Botão "Publicar Notas" com modal de confirmação mostrando preview.
10. classes/[classId]/attendance/page.tsx — Controle de frequência. Grid com: aluno (linhas) x datas (colunas). Cada célula: presente (P), ausente (A), justificado (J). Botão salvar. Calendário de frequência. Relatório de frequência.
11. classes/[classId]/assignments/page.tsx — Tarefas da turma. Lista com: título, data de entrega, submissões (X/Y), status. Botão criar tarefa.
12. classes/[classId]/assignments/[assignmentId]/page.tsx — Submissões dos alunos. Lista com: aluno, data de entrega, status (entregue, atrasado, não entregue), nota (se avaliada), botão avaliar.
13. classes/[classId]/assignments/[assignmentId]/submissions/[submissionId]/page.tsx — Avaliar submissão. Visualizador do arquivo submetido (PDF, imagem, texto). Rubrica de avaliação (critérios e notas). Área de feedback textual. Botão publicar nota.
14. classes/[classId]/forum/page.tsx — Fórum da turma. Mesmo do aluno, mas com poderes de moderação (fixar, deletar, editar).
15. grading/page.tsx — Central de avaliação. Lista de todas as submissões pendentes de avaliação de todas as turmas. Filtros: turma, tarefa, status, data.
16. schedule/page.tsx — Horário do professor. Visualização semanal. Botão definir disponibilidade. Solicitar substituição.
17. messages/page.tsx — Mesmo do aluno.
18. profile/page.tsx — Perfil do professor. Seções: dados pessoais, formação acadêmica, disciplinas lecionadas, carga horária, avaliações de desempenho.
'''

with open('/mnt/agents/output/AOS_Prompt_Desenvolvimento.md', 'a', encoding='utf-8') as f:
    f.write(part3)

print("Parte 3 salva")

part4 = '''
ETAPA 3.6 — Portal do Coordenador (apps/web/src/app/(dashboard)/coordinator/)
--------------------------------------------------------------------------------
Criar os seguintes arquivos:

1. layout.tsx — Layout do portal do coordenador.
2. page.tsx — Dashboard do coordenador. Widgets: total de matrículas, carga horária dos professores, ocupação das turmas, alertas (turmas lotadas, conflitos de horário), calendário acadêmico.
3. classes/page.tsx — Gerenciar turmas. Tabela com: nome, disciplina, professor, alunos (X/Y), vagas, status. Botão criar turma, editar, excluir.
4. classes/create/page.tsx — Formulário de criação de turma. Campos: nome, disciplina, professor, período, vagas, horário, sala.
5. teachers/page.tsx — Gerenciar professores. Tabela com: nome, disciplinas, carga horária, turmas, status. Botão atribuir disciplina, ver horário, avaliar.
6. curriculum/page.tsx — Grade curricular. Visualização da grade por período. Botão adicionar disciplina, definir pré-requisitos, reordenar.
7. students/page.tsx — Todos os alunos. Busca avançada (nome, matrícula, curso, status). Tabela com resultados. Botão ver perfil completo, ver histórico acadêmico, processar transferência.
8. reports/page.tsx — Relatórios acadêmicos. Lista de relatórios disponíveis: matrículas, desempenho, frequência, evasão, distribuição de notas. Botão gerar, agendar, exportar (PDF/Excel).
9. calendar/page.tsx — Calendário acadêmico. Visualização mensal. Botão adicionar evento, agendar prova, definir feriado.
10. settings/page.tsx — Configurações do departamento. Campos: critérios de aprovação, nota mínima, frequência mínima, períodos letivos.

ETAPA 3.7 — Portal Administrativo (apps/web/src/app/(dashboard)/admin/)
--------------------------------------------------------------------------------
Criar os seguintes arquivos:

1. layout.tsx — Layout do portal admin com sidebar mais compacta.
2. page.tsx — Dashboard administrativo. Widgets: status dos serviços (CPU, RAM, DB, Redis), total de usuários ativos, receita mensal, plugins ativos, feed de atividades recentes, alertas críticos.
3. users/page.tsx — Gerenciar usuários. Tabela avançada com: foto, nome, email, papel, instituição, status, último login. Filtros avançados. Botão criar, editar, desativar, excluir. Importar CSV. Exportar.
4. users/[userId]/page.tsx — Perfil detalhado do usuário. Todas as informações, atividades, sessões ativas, botão impersonate (logar como).
5. plugins/page.tsx — Plugin Marketplace. Grid de cards com: nome, descrição, versão, autor, rating, botão instalar/ativar/desativar/configurar. Aba "Instalados" e "Disponíveis".
6. plugins/[pluginId]/config/page.tsx — Configuração do plugin. Formulário dinâmico baseado no manifest do plugin.
7. settings/page.tsx — Configurações globais. Seções: geral (nome da escola, logo, domínio), acadêmico (ano letivo, períodos, notas mínimas), email (SMTP, templates), SMS (gateway), pagamento (gateways), notificações (templates), tema (cores, fontes), idiomas, backup, segurança (2FA, sessão, senhas), integrações (APIs, webhooks, LDAP).
8. finance/page.tsx — Financeiro institucional. Dashboard de receita. Lista de faturas. Gestão de bolsas e descontos. Folha de pagamento (integração com RH). Relatórios financeiros.
9. analytics/page.tsx — Analytics e BI. Gráficos: tendências de matrícula, taxa de retenção, previsão de receita, engajamento de usuários (heatmap). Construtor de relatórios customizados. Exportar dados.
10. logs/page.tsx — Logs do sistema. Abas: logs técnicos, audit trail (quem fez o quê), logs de erro, logs de segurança. Filtros por data, usuário, ação. Exportar.
11. support/page.tsx — Suporte e tickets. Lista de tickets com: título, autor, status, prioridade, data. Botão atribuir, responder, fechar. Base de conhecimento. FAQs.

ETAPA 3.8 — Portal do Encarregado (apps/web/src/app/(dashboard)/guardian/)
--------------------------------------------------------------------------------
Criar os seguintes arquivos:

1. layout.tsx — Layout do portal do encarregado.
2. page.tsx — Dashboard do encarregado. Seletor de filho (se múltiplos). Widgets: resumo do filho, progresso acadêmico, frequência, tarefas pendentes, notas recentes, financeiro.
3. child/[studentId]/page.tsx — Perfil do filho. Seções: dados acadêmicos, notas detalhadas, frequência, horário, comportamento/disciplina.
4. child/[studentId]/grades/page.tsx — Notas do filho.
5. child/[studentId]/attendance/page.tsx — Frequência do filho.
6. child/[studentId]/schedule/page.tsx — Horário do filho.
7. finance/page.tsx — Financeiro. Faturas relacionadas ao filho. Botão pagar. Histórico.
8. messages/page.tsx — Comunicação com a escola.
9. documents/page.tsx — Documentos do filho.

ETAPA 3.9 — Portal do Bibliotecário (apps/web/src/app/(dashboard)/librarian/)
--------------------------------------------------------------------------------
Criar os seguintes arquivos:

1. layout.tsx — Layout do portal do bibliotecário.
2. page.tsx — Dashboard da biblioteca. Widgets: total de livros, empréstimos ativos, atrasos, novas aquisições, fila de reservas.
3. catalog/page.tsx — Catálogo. Busca avançada (título, autor, ISBN, categoria). Tabela com resultados. Botão adicionar, editar, excluir. Scanner de código de barras.
4. catalog/add/page.tsx — Formulário de adição de livro. Campos: título, autor, ISBN, editora, ano, categoria, quantidade, localização, capa (upload).
5. loans/page.tsx — Empréstimos. Tabela com: livro, usuário, data de empréstimo, data de devolução prevista, status. Botão processar devolução, renovar, registrar atraso.
6. loans/overdue/page.tsx — Atrasos. Lista de empréstimos atrasados com: livro, usuário, dias de atraso, contato. Botão enviar lembrete.
7. users/page.tsx — Usuários da biblioteca. Tabela com: nome, tipo, empréstimos ativos, histórico.
8. reports/page.tsx — Relatórios. Empréstimos por período, livros mais lidos, usuários mais ativos, atrasos.
9. digital/page.tsx — Repositório digital. Upload de documentos digitais. Categorização. Busca.

ETAPA 3.10 — Portal do RH (apps/web/src/app/(dashboard)/hr/)
--------------------------------------------------------------------------------
Criar os seguintes arquivos:

1. layout.tsx — Layout do portal de RH.
2. page.tsx — Dashboard de RH. Widgets: total de funcionários, folha de pagamento do mês, pedidos de férias pendentes, pipeline de recrutamento.
3. employees/page.tsx — Funcionários. Tabela com: foto, nome, cargo, departamento, data de admissão, status. Botão adicionar, editar, desligar.
4. employees/[employeeId]/page.tsx — Perfil do funcionário. Dados pessoais, cargo, salário, histórico, documentos.
5. employees/onboarding/page.tsx — Processo de onboarding. Checklist de tarefas. Envio de documentos. Boas-vindas.
6. payroll/page.tsx — Folha de pagamento. Processamento mensal. Lista de funcionários com salário, descontos, benefícios, líquido. Botão processar, gerar holerites.
7. payroll/payslips/page.tsx — Holerites. Lista por funcionário e mês. Botão download PDF.
8. recruitment/page.tsx — Recrutamento. Vagas abertas. Candidatos por vaga. Tracker de pipeline (triagem, entrevista, oferta, contratação). Agendador de entrevistas.
9. leave/page.tsx — Férias e ausências. Calendário de férias. Pedidos pendentes. Saldo de férias por funcionário. Botão aprovar/rejeitar.
10. performance/page.tsx — Avaliação de desempenho. Ciclos de avaliação. Formulários. Relatórios.

ETAPA 3.11 — Componentes compartilhados (apps/web/src/components/)
--------------------------------------------------------------------------------
Criar os seguintes componentes:

1. Sidebar.tsx — Sidebar colapsável com: logo, menu de navegação (baseado no papel do usuário), botão toggle, footer com usuário logado.
2. TopBar.tsx — Barra superior com: botão toggle sidebar, breadcrumbs, search global, botão notificações (com badge), botão mensagens, user menu (avatar + dropdown).
3. BottomBar.tsx — Barra inferior mobile com 5 tabs: Início, Cursos, Agenda, Mensagens, Perfil.
4. CommandPalette.tsx — Modal CMD+K com fuzzy search. Busca em: páginas, ações, usuários, cursos. Atalhos de teclado.
5. NotificationDropdown.tsx — Dropdown de notificações com: lista, filtro, botão marcar todas como lidas, link ver todas.
6. UserMenu.tsx — Dropdown do usuário com: perfil, configurações, tema, idioma, logout.
7. AppSwitcher.tsx — Grid de apps/plugins disponíveis para o usuário.
8. BreadcrumbNav.tsx — Navegação hierárquica com links clicáveis.
9. DataTable.tsx — Tabela reutilizável com: sort, filter, paginate, select rows, actions dropdown, export.
10. Pagination.tsx — Componente de paginação com: página anterior/próxima, números de página, seletor de itens por página.
11. SearchInput.tsx — Campo de busca com ícone, clear button, loading state.
12. FilterBar.tsx — Barra de filtros com chips ativos e botão limpar.
13. StatCard.tsx — Card de estatística com: título, valor, delta (positivo/negativo), ícone, trend.
14. ChartCard.tsx — Card com gráfico (usando recharts ou similar).
15. Modal.tsx — Modal reutilizável com: overlay, close button, header, body, footer.
16. Drawer.tsx — Drawer reutilizável com 4 direções.
17. Tabs.tsx — Tabs reutilizáveis com variantes: underline, pills, vertical.
18. FormInput.tsx — Input reutilizável com: label, error message, helper text, icon, password toggle.
19. FormSelect.tsx — Select reutilizável com: search, multi-select, clear.
20. FormTextarea.tsx — Textarea reutilizável com contador de caracteres.
21. FormCheckbox.tsx — Checkbox reutilizável com label.
22. FormRadio.tsx — Radio group reutilizável.
23. FormSwitch.tsx — Toggle switch reutilizável.
24. FileUploader.tsx — Upload de arquivo com: drag & drop, preview, progress bar, validação.
25. DatePicker.tsx — Seletor de data.
26. TimePicker.tsx — Seletor de hora.
27. Avatar.tsx — Avatar com fallback de iniciais.
28. AvatarGroup.tsx — Grupo de avatares com overflow.
29. Badge.tsx — Badge com variants.
30. ProgressBar.tsx — Barra de progresso linear e circular.
31. Skeleton.tsx — Skeleton para loading states.
32. EmptyState.tsx — Estado vazio com ilustração, título, descrição, ação.
33. ErrorState.tsx — Estado de erro com ilustração, título, descrição, retry.
34. LoadingState.tsx — Estado de loading com spinner e texto.
35. Toast.tsx — Notificação toast com: tipos (success, error, warning, info), auto-dismiss, progress bar.
36. Tooltip.tsx — Tooltip com 12 posições.
37. Popover.tsx — Popover com trigger e content.
38. Accordion.tsx — Accordion com single/multi expand.
39. Stepper.tsx — Stepper horizontal e vertical.
40. Calendar.tsx — Componente de calendário mensal/semanal/diário.

ETAPA 3.12 — Hooks (apps/web/src/hooks/)
--------------------------------------------------------------------------------
Criar os seguintes hooks:

1. useAuth.ts — retorna: user, isAuthenticated, isLoading, login, logout, register.
2. useUser.ts — retorna: user data, updateUser, refetch.
3. useNotifications.ts — retorna: notifications, unreadCount, markAsRead, markAllAsRead.
4. useCourses.ts — retorna: courses, isLoading, error, refetch.
5. useCourse.ts — retorna: course data, lessons, assignments, grades.
6. useLessons.ts — retorna: lessons, progress, markComplete.
7. useAssignments.ts — retorna: assignments, submit, submissions.
8. useGrades.ts — retorna: grades, statistics, history.
9. useSchedule.ts — retorna: schedule, events, addEvent.
10. useMessages.ts — retorna: conversations, messages, sendMessage.
11. useFinance.ts — retorna: invoices, payments, pay.
12. useDocuments.ts — retorna: documents, request, download.
13. usePlugins.ts — retorna: plugins, install, activate, deactivate, configure.
14. useTheme.ts — retorna: theme, setTheme, toggleTheme.
15. useLocale.ts — retorna: locale, setLocale, t (translate).
16. useMediaQuery.ts — retorna: matches para breakpoints.
17. useDebounce.ts — retorna: debounced value.
18. useLocalStorage.ts — retorna: value, setValue.
19. useOnlineStatus.ts — retorna: isOnline.
20. usePermission.ts — retorna: hasPermission, hasRole.

ETAPA 3.13 — Stores Zustand (apps/web/src/stores/)
--------------------------------------------------------------------------------
Criar os seguintes stores:

1. authStore.ts — state: user, token, isAuthenticated, isLoading. Actions: setUser, setToken, login, logout, updateUser.
2. themeStore.ts — state: theme (light/dark/system). Actions: setTheme, toggleTheme.
3. localeStore.ts — state: locale. Actions: setLocale.
4. sidebarStore.ts — state: isOpen, isCollapsed. Actions: toggle, collapse, expand.
5. notificationStore.ts — state: notifications, unreadCount. Actions: add, remove, markAsRead, markAllAsRead.
6. commandPaletteStore.ts — state: isOpen, query, results. Actions: open, close, setQuery, setResults.
7. pluginStore.ts — state: plugins, activePlugins. Actions: setPlugins, activate, deactivate.

ETAPA 3.14 — Lib e Utilitários (apps/web/src/lib/)
--------------------------------------------------------------------------------
Criar os seguintes arquivos:

1. api.ts — instância axios com: baseURL, interceptors (auth token, refresh token, error handling).
2. queryClient.ts — configuração do React Query.
3. utils.ts — funções: cn (clsx + tailwind-merge), formatDate, formatCurrency, formatNumber, truncate, debounce, throttle.
4. constants.ts — constantes: API_URL, APP_NAME, APP_VERSION, ROLES, PERMISSIONS, ROUTES.
5. routes.ts — definição de todas as rotas do app por papel.
'''

with open('/mnt/agents/output/AOS_Prompt_Desenvolvimento.md', 'a', encoding='utf-8') as f:
    f.write(part4)

print("Parte 4 salva")