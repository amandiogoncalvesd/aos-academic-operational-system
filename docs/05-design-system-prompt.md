# 🎨 AOS — G Designer School
## Prompt de Desenvolvimento Completo: UX/UI Design System

**Versão:** 1.0  
**Data:** 10 de Setembro de 2026  
**Destinatário:** Designer / Agente de Criação de Interface  
**Escopo:** Especificação completa de design UX/UI para todo o AOS (Academic Operational System)

---

## 📋 INSTRUÇÕES GERAIS

Você está recebendo a especificação de design mais completa já escrita para um sistema acadêmico. O AOS (Academic Operational System) é o primeiro sistema operacional acadêmico do mundo — uma plataforma unificada que absorve LMS, ERP, SIS, CRM, RH, BI, Comunicação e Biblioteca em um único ecossistema.

**A instituição de referência é a G Designer School** — uma escola de design de elite que exige interfaces de nível mundial. A experiência deve ser comparável ou superior a:
- **Notion** (organização e clareza)
- **Linear** (velocidade e estética)
- **Figma** (colaboração e fluidez)
- **Apple Design** (polimento e acessibilidade)
- **Duolingo** (gamificação e engajamento)
- **Canvas LMS** (funcionalidade acadêmica)

**Diretrizes absolutas:**
- Mobile-first, mas desktop-optimized
- Dark mode e light mode nativos
- Acessibilidade WCAG 2.1 AAA
- RTL (Right-to-Left) ready para árabe/hebraico
- i18n completo (PT, EN, ES, FR, DE, IT, ZH, JA, AR, RU)
- Design system tokenizado (cores, espaçamento, tipografia, sombras, bordas)
- Micro-interactions em TODAS as ações
- Skeleton screens para todos os estados de loading
- Empty states ilustrados e contextualizados
- Error states com soluções proativas
- Zero clutter — cada pixel deve ter propósito

---

## 1. 🎨 DESIGN SYSTEM FOUNDATION

### 1.1 Tokens de Design (Design Tokens)

Crie um arquivo `design-tokens.json` ou `tokens.css` com:

```
📁 design-system/
├── tokens/
│   ├── colors.json          (100+ tokens de cor)
│   ├── spacing.json         (8px base scale)
│   ├── typography.json      (Inter + JetBrains Mono)
│   ├── shadows.json         (elevação 0-5)
│   ├── borders.json         (radius, width)
│   ├── animations.json      (duração, easing)
│   └── breakpoints.json     (mobile, tablet, desktop, wide)
├── components/
│   └── (todos os componentes base)
└── patterns/
    └── (padrões de layout reutilizáveis)
```

**Cores (Light Mode):**
- Primary: `#0F172A` (slate-900) — confiança, autoridade acadêmica
- Primary Hover: `#1E293B` (slate-800)
- Secondary: `#3B82F6` (blue-500) — ação, links, interação
- Accent: `#F59E0B` (amber-500) — destaque, gamificação, alertas positivos
- Success: `#10B981` (emerald-500)
- Warning: `#F59E0B` (amber-500)
- Error: `#EF4444` (red-500)
- Info: `#3B82F6` (blue-500)
- Background: `#F8FAFC` (slate-50)
- Surface: `#FFFFFF` (white)
- Surface Elevated: `#FFFFFF` + shadow
- Text Primary: `#0F172A` (slate-900)
- Text Secondary: `#64748B` (slate-500)
- Text Tertiary: `#94A3B8` (slate-400)
- Border: `#E2E8F0` (slate-200)
- Divider: `#F1F5F9` (slate-100)

**Cores (Dark Mode):**
- Background: `#0A0F1C` (custom dark)
- Surface: `#111827` (gray-900)
- Surface Elevated: `#1F2937` (gray-800)
- Text Primary: `#F8FAFC` (slate-50)
- Text Secondary: `#94A3B8` (slate-400)
- Text Tertiary: `#64748B` (slate-500)
- Border: `#374151` (gray-700)
- Divider: `#1F2937` (gray-800)

**Tipografia:**
- Font Family: `Inter` (Google Fonts) — weights 300, 400, 500, 600, 700
- Font Family Mono: `JetBrains Mono` — para código, IDs, timestamps
- Font Family Display: `Plus Jakarta Sans` — para títulos grandes
- Scale: 12px, 14px, 16px (base), 18px, 20px, 24px, 30px, 36px, 48px, 60px, 72px
- Line Height: 1.25 (headings), 1.5 (body), 1.75 (long-form)
- Letter Spacing: -0.02em (display), -0.01em (headings), 0 (body), 0.05em (labels/caps)

**Espaçamento (8px grid):**
- 0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128px

**Bordas:**
- Radius: 0, 4, 6, 8, 12, 16, 20, 24, 9999px (full)
- Width: 0, 1, 2px

**Sombras (Light):**
- sm: `0 1px 2px 0 rgb(0 0 0 / 0.05)`
- md: `0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)`
- lg: `0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)`
- xl: `0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)`
- 2xl: `0 25px 50px -12px rgb(0 0 0 / 0.25)`

**Animações:**
- Duration Fast: 150ms
- Duration Normal: 250ms
- Duration Slow: 350ms
- Easing Default: `cubic-bezier(0.4, 0, 0.2, 1)`
- Easing Enter: `cubic-bezier(0, 0, 0.2, 1)`
- Easing Exit: `cubic-bezier(0.4, 0, 1, 1)`
- Easing Bounce: `cubic-bezier(0.34, 1.56, 0.64, 1)`

### 1.2 Componentes Base (Design System)

Cada componente deve ter variants para: default, hover, active, focus, disabled, loading, error, success.

```
📁 design-system/components/
├── atoms/
│   ├── Button.tsx              (6 variants: primary, secondary, ghost, danger, link, icon)
│   ├── IconButton.tsx          (circular, quadrado)
│   ├── Input.tsx               (text, password, email, number, search, textarea)
│   ├── Select.tsx              (single, multi, searchable, creatable)
│   ├── Checkbox.tsx            (com label, indeterminate state)
│   ├── Radio.tsx               (grupo, com label)
│   ├── Switch.tsx              (toggle, com label)
│   ├── Badge.tsx               (6 variants: default, primary, secondary, success, warning, error)
│   ├── Avatar.tsx              (xs, sm, md, lg, xl, 2xl — com fallback iniciais)
│   ├── AvatarGroup.tsx         (stack com +N overflow)
│   ├── Tag.tsx                 (removable, colored)
│   ├── Chip.tsx                (seleção, filtro)
│   ├── ProgressBar.tsx         (linear, circular, indeterminate)
│   ├── Spinner.tsx             (tamanhos, cores)
│   ├── Skeleton.tsx            (text, circle, rectangle, custom)
│   ├── Tooltip.tsx             (12 posições, delay 300ms)
│   ├── Popover.tsx             (trigger + content, arrow)
│   ├── Modal.tsx               (overlay, focus trap, ESC to close)
│   ├── Drawer.tsx              (4 direções, overlay)
│   ├── Accordion.tsx           (single, multi, animado)
│   ├── Tabs.tsx                (horizontal, vertical, pills, underline)
│   ├── Breadcrumb.tsx          (com separator customizável)
│   ├── Pagination.tsx          (simple, advanced, with page size selector)
│   ├── Stepper.tsx             (horizontal, vertical, com ícones)
│   ├── Slider.tsx              (single, range, with marks)
│   ├── DatePicker.tsx          (single, range, with time)
│   ├── TimePicker.tsx          (12h, 24h)
│   ├── ColorPicker.tsx         (hex, rgb, hsl, preset swatches)
│   ├── FileUpload.tsx          (drag & drop, progress, preview)
│   ├── RichTextEditor.tsx      (toolbar, markdown support)
│   ├── CodeBlock.tsx           (syntax highlighting, copy button)
│   ├── Divider.tsx             (horizontal, vertical, with text)
│   ├── EmptyState.tsx          (ilustração + título + descrição + ação)
│   ├── ErrorState.tsx          (ilustração + título + descrição + retry)
│   ├── LoadingState.tsx        (skeleton + spinner + texto)
│   ├── SearchInput.tsx         (com icon, clear button, loading state)
│   ├── CommandPalette.tsx      (CMD+K, fuzzy search, actions rápidas)
│   ├── NotificationToast.tsx   (4 posições, auto-dismiss, progress bar)
│   ├── Banner.tsx              (info, warning, error, success — dismissible)
│   └── Card.tsx                (default, hoverable, clickable, with header/footer)
│
├── molecules/
│   ├── DataTable.tsx           (sort, filter, paginate, select, expand, actions)
│   ├── KanbanBoard.tsx         (drag & drop, columns, cards)
│   ├── Calendar.tsx            (month, week, day, agenda views)
│   ├── Timeline.tsx            (vertical, horizontal, with icons)
│   ├── ChatBubble.tsx          (sent, received, with avatar, timestamp, status)
│   ├── CommentThread.tsx       (nested, with reply, like, edit, delete)
│   ├── ActivityFeed.tsx        (icon + texto + timestamp + actor)
│   ├── NotificationItem.tsx    (unread, read, with actions)
│   ├── UserMenu.tsx            (avatar + dropdown com perfil, config, logout)
│   ├── AppSwitcher.tsx         (grid de apps/plugins, com busca)
│   ├── GlobalSearch.tsx        (search bar + results + filters + history)
│   ├── FilterBar.tsx           (chips de filtro ativos + botão clear)
│   ├── StatCard.tsx            (título, valor, delta, sparkline, trend)
│   ├── ChartCard.tsx           (título + gráfico + legend + tooltip)
│   ├── FormSection.tsx         (título + descrição + campos + ações)
│   ├── Wizard.tsx              (stepper + conteúdo + navegação)
│   ├── ComparisonTable.tsx     (feature comparison, checkmarks)
│   ├── PricingCard.tsx         (planos, features, CTA, highlight)
│   └── OnboardingStep.tsx      (ilustração + título + descrição + ação)
│
└── organisms/
    ├── Navigation/
    │   ├── Sidebar.tsx         (collapsible, nested, with icons, badges)
    │   ├── TopBar.tsx          (logo, search, notifications, user menu, app switcher)
    │   ├── BottomBar.tsx       (mobile: 5 tabs com ícones + labels)
    │   ├── BreadcrumbNav.tsx   (caminho hierárquico + voltar)
    │   ├── ContextualNav.tsx   (tabs secundárias, filtros contextuais)
    │   └── CommandBar.tsx      (atalhos de teclado, ações rápidas)
    │
    ├── Layout/
    │   ├── AppShell.tsx        (sidebar + topbar + content + footer)
    │   ├── DashboardLayout.tsx (grid de widgets, draggable)
    │   ├── AuthLayout.tsx      (split screen: imagem + formulário)
    │   ├── OnboardingLayout.tsx (progresso + conteúdo + navegação)
    │   ├── SettingsLayout.tsx  (sidebar de config + conteúdo)
    │   ├── EmptyLayout.tsx     (página vazia, centered)
    │   └── PrintLayout.tsx     (otimizado para impressão)
    │
    └── DataDisplay/
        ├── DataGrid.tsx        (tabela avançada com virtualização)
        ├── TreeView.tsx        (hierarquia expansível, drag & drop)
        ├── FileTree.tsx        (explorer-style, com ações)
        ├── MediaGallery.tsx    (grid, masonry, carousel, lightbox)
        └── PDFViewer.tsx       (scroll, zoom, search, annotations)
```

---

## 2. 🏛️ ESTRUTURA DE REPOSITÓRIOS

### 2.1 Arquitetura de Código: Monorepo

O AOS usará **Monorepo** com **Turborepo** (ou Nx). Um único repositório contém todo o código, mas com apps e packages separados.

```
📁 aos/
├── 📁 apps/
│   ├── 📁 web/                    # Next.js 14 — Shell App + Micro-frontends
│   │   ├── src/
│   │   │   ├── app/              # App Router (Next.js 14)
│   │   │   │   ├── (auth)/       # Grupo de rotas: login, register, forgot
│   │   │   │   ├── (dashboard)/  # Grupo de rotas: todas as páginas internas
│   │   │   │   ├── api/          # API Routes (webhooks, auth callbacks)
│   │   │   │   └── layout.tsx    # Root layout (providers, theme, fonts)
│   │   │   ├── components/       # Componentes específicos do web
│   │   │   ├── hooks/            # React hooks customizados
│   │   │   ├── lib/              # Utilitários, fetchers, config
│   │   │   ├── stores/           # Zustand stores
│   │   │   ├── types/            # TypeScript types
│   │   │   └── styles/           # CSS global, Tailwind config
│   │   ├── public/               # Assets estáticos
│   │   └── package.json
│   │
│   ├── 📁 mobile/                 # Flutter — App Nativo
│   │   ├── lib/
│   │   │   ├── main.dart
│   │   │   ├── screens/          # Telas do app
│   │   │   ├── widgets/          # Componentes reutilizáveis
│   │   │   ├── models/           # Models Dart
│   │   │   ├── services/         # API clients
│   │   │   ├── providers/        # State management (Riverpod)
│   │   │   └── utils/            # Utilitários
│   │   ├── assets/               # Imagens, fonts, icons
│   │   └── pubspec.yaml
│   │
│   ├── 📁 docs/                   # Docusaurus — Documentação
│   │   └── src/
│   │
│   └── 📁 admin/                  # Painel Admin separado (se necessário)
│       └── src/
│
├── 📁 packages/
│   ├── 📁 ui/                     # Design System — Componentes React
│   │   ├── src/
│   │   │   ├── components/       # Todos os componentes do design system
│   │   │   ├── tokens/           # Cores, espaçamento, tipografia
│   │   │   ├── hooks/            # Hooks de UI (useTheme, useMediaQuery)
│   │   │   ├── utils/            # Utilitários de UI
│   │   │   └── index.ts          # Exporta tudo
│   │   └── package.json
│   │
│   ├── 📁 config/                 # Configs compartilhadas
│   │   ├── eslint/
│   │   ├── prettier/
│   │   ├── tailwind/
│   │   ├── tsconfig/
│   │   └── package.json
│   │
│   ├── 📁 types/                  # Typescript types compartilhados
│   │   ├── src/
│   │   │   ├── api.ts            # Tipos de API (requests/responses)
│   │   │   ├── entities.ts       # Entidades do domínio
│   │   │   ├── enums.ts          # Enums globais
│   │   │   └── index.ts
│   │   └── package.json
│   │
│   ├── 📁 utils/                  # Utilitários compartilhados
│   │   ├── src/
│   │   │   ├── date.ts           # Formatação de datas
│   │   │   ├── currency.ts       # Formatação de moeda
│   │   │   ├── validation.ts     # Validações (zod schemas)
│   │   │   ├── i18n.ts           # Internacionalização helpers
│   │   │   └── index.ts
│   │   └── package.json
│   │
│   ├── 📁 api-client/             # Cliente HTTP compartilhado
│   │   ├── src/
│   │   │   ├── client.ts         # Axios/Fetch wrapper
│   │   │   ├── interceptors.ts   # Auth, error handling
│   │   │   ├── endpoints/        # Definição de endpoints por domínio
│   │   │   └── index.ts
│   │   └── package.json
│   │
│   └── 📁 icons/                  # Biblioteca de ícones customizados
│       ├── src/
│       └── package.json
│
├── 📁 plugins/                    # Plugins do AOS (cada um é um package)
│   ├── 📁 aos-core-auth/
│   ├── 📁 aos-core-eventbus/
│   ├── 📁 aos-core-config/
│   ├── 📁 aos-domain-lms/
│   ├── 📁 aos-domain-sis/
│   ├── 📁 aos-domain-erp/
│   ├── 📁 aos-domain-crm/
│   ├── 📁 aos-domain-hr/
│   ├── 📁 aos-domain-bi/
│   ├── 📁 aos-domain-library/
│   ├── 📁 aos-domain-communication/
│   ├── 📁 aos-domain-exam/
│   ├── 📁 aos-domain-portal/
│   ├── 📁 aos-domain-mobile/
│   └── 📁 aos-domain-s2st/        # Speech-to-Speech Translation
│
├── 📁 services/                   # Backend services (FastAPI)
│   ├── 📁 core/                   # AOS Core (Plugin Engine, Event Bus, Auth)
│   ├── 📁 gateway/                # API Gateway (Kong/Traefik config)
│   └── 📁 workers/                # Celery workers
│
├── 📁 infra/                      # Infrastructure as Code
│   ├── terraform/
│   ├── kubernetes/
│   └── docker/
│
├── 📁 docs/                       # Documentação geral
├── turbo.json                     # Config do Turborepo
├── package.json                   # Root package.json
└── pnpm-workspace.yaml            # Definição do workspace
```

---

## 3. 🖥️ TELAS E FLUXOS POR PORTAL

### 3.1 Portal do Aluno (Student Portal)

**Objetivo:** Central de comando do aluno. Tudo que ele precisa em um único dashboard.

```
📁 apps/web/src/app/(dashboard)/student/
├── page.tsx                          # Dashboard do Aluno (home)
├── layout.tsx                        # Layout com sidebar de aluno
│
├── 📁 dashboard/
│   ├── page.tsx                      # Overview: próximas aulas, tarefas, notas, financeiro
│   ├── components/
│   │   ├── NextClassCard.tsx         # Próxima aula com countdown
│   │   ├── PendingAssignments.tsx    # Lista de tarefas pendentes
│   │   ├── GradeOverview.tsx         # Média geral + gráfico de desempenho
│   │   ├── AttendanceWidget.tsx      # Frequência mensal (heatmap)
│   │   ├── FinancialStatus.tsx       # Propinas: pago/ pendente / atrasado
│   │   ├── AnnouncementsFeed.tsx     # Avisos da escola
│   │   ├── CalendarMini.tsx          # Calendário mini (próximos eventos)
│   │   └── ProgressTracker.tsx       # Progresso no curso (% concluído)
│   └── loading.tsx                   # Skeleton do dashboard
│
├── 📁 courses/
│   ├── page.tsx                      # Lista de cursos matriculados
│   ├── [courseId]/
│   │   ├── page.tsx                  # Página do curso (overview)
│   │   ├── layout.tsx                # Layout com tabs: Conteúdo, Tarefas, Notas, Fórum
│   │   ├── 📁 content/
│   │   │   ├── page.tsx              # Lista de módulos/aulas
│   │   │   └── [lessonId]/
│   │   │       ├── page.tsx          # Player de vídeo + materiais + quiz
│   │   │       └── components/
│   │   │           ├── VideoPlayer.tsx           # Player com múltiplas faixas de áudio
│   │   │           ├── AudioLanguageSelector.tsx # Seletor de idioma de áudio (S2ST)
│   │   │           ├── TranscriptPanel.tsx       # Transcrição com busca
│   │   │           ├── MaterialsList.tsx         # PDFs, slides, links
│   │   │           ├── QuizInline.tsx            # Quiz embutido no vídeo
│   │   │           ├── NoteTaker.tsx             # Anotações sincronizadas com timestamp
│   │   │           ├── DiscussionPanel.tsx       # Discussão da aula
│   │   │           └── CompletionButton.tsx      # Marcar como concluído
│   │   ├── 📁 assignments/
│   │   │   ├── page.tsx              # Lista de tarefas do curso
│   │   │   └── [assignmentId]/
│   │   │       ├── page.tsx          # Detalhe da tarefa + entrega
│   │   │       └── components/
│   │   │           ├── AssignmentDetails.tsx
│   │   │           ├── FileUploader.tsx
│   │   │           ├── TextEditor.tsx
│   │   │           ├── SubmissionStatus.tsx
│   │   │           ├── GradeFeedback.tsx
│   │   │           └── PlagiarismCheck.tsx
│   │   ├── 📁 grades/
│   │   │   ├── page.tsx              # Notas do curso
│   │   │   └── components/
│   │   │       ├── GradeBook.tsx
│   │   │       ├── GradeChart.tsx
│   │   │       └── GradeHistory.tsx
│   │   ├── 📁 forum/
│   │   │   ├── page.tsx              # Fórum de discussão
│   │   │   └── [topicId]/
│   │   │       └── page.tsx
│   │   └── 📁 classmates/
│   │       └── page.tsx              # Lista de colegas
│   └── loading.tsx
│
├── 📁 schedule/
│   ├── page.tsx                      # Horário semanal (calendário)
│   └── components/
│       ├── WeeklyCalendar.tsx        # Visualização semanal
│       ├── DailyView.tsx             # Visualização diária
│       ├── ClassCard.tsx             # Card de aula com sala, professor
│       └── ExamMarker.tsx            # Marcador de provas
│
├── 📁 grades/
│   ├── page.tsx                      # Boletim completo
│   └── components/
│       ├── GradeReport.tsx           # Pauta oficial
│       ├── TranscriptPreview.tsx     # Preview do histórico
│       ├── GPAChart.tsx              # Gráfico de evolução do GPA
│       └── SubjectBreakdown.tsx      # Detalhamento por disciplina
│
├── 📁 finance/
│   ├── page.tsx                      # Financeiro do aluno
│   └── components/
│       ├── InvoiceList.tsx           # Lista de faturas
│       ├── PaymentMethods.tsx        # Métodos de pagamento
│       ├── PaymentHistory.tsx        # Histórico de pagamentos
│       ├── OutstandingBalance.tsx    # Saldo devedor
│       ├── PaymentButton.tsx         # Botão de pagamento (integração)
│       └── ReceiptDownloader.tsx     # Download de recibos
│
├── 📁 documents/
│   ├── page.tsx                      # Documentos do aluno
│   └── components/
│       ├── DocumentList.tsx          # Atestados, declarações, certificados
│       ├── DocumentRequestForm.tsx   # Solicitação de documentos
│       ├── DigitalCertificate.tsx    # Certificado digital com QR code
│       └── VerificationBadge.tsx     # Badge de verificação
│
├── 📁 messages/
│   ├── page.tsx                      # Mensagens
│   └── components/
│       ├── ChatList.tsx              # Lista de conversas
│       ├── ChatWindow.tsx            # Janela de chat
│       ├── NewMessageModal.tsx       # Nova mensagem
│       └── AttachmentUploader.tsx
│
├── 📁 notifications/
│   ├── page.tsx                      # Central de notificações
│   └── components/
│       ├── NotificationList.tsx      # Lista com filtros (todas, não lidas, importantes)
│       ├── NotificationPreferences.tsx # Preferências de notificação
│       └── NotificationDetail.tsx    # Detalhe da notificação
│
├── 📁 profile/
│   ├── page.tsx                      # Perfil do aluno
│   └── components/
│       ├── ProfileHeader.tsx         # Foto, nome, curso, matrícula
│       ├── PersonalInfoForm.tsx      # Dados pessoais (editável)
│       ├── AcademicInfo.tsx          # Curso, turma, ano
│       ├── EmergencyContacts.tsx     # Contatos de emergência
│       ├── PasswordChange.tsx        # Alterar senha
│       ├── TwoFactorSetup.tsx        # 2FA
│       └── ActivityLog.tsx           # Log de atividades
│
└── 📁 settings/
    ├── page.tsx                      # Configurações gerais
    └── components/
        ├── ThemeToggle.tsx           # Light / Dark / System
        ├── LanguageSelector.tsx      # Idioma da interface
        ├── NotificationSettings.tsx  # Configuração de notificações
        ├── AccessibilitySettings.tsx # Acessibilidade (fonte, contraste, motion)
        └── PrivacySettings.tsx       # Privacidade e dados
```

**Dashboard do Aluno — Especificação de Widgets:**

O dashboard deve ser um **grid de 12 colunas** com widgets drag-and-drop (opcional na fase 2). Layout padrão:

```
┌─────────────────────────────────────────────────────────────────┐
│  [Header: "Bom dia, Maria!" + Data + Avisos importantes]       │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Próxima Aula │  │ Tarefas      │  │ Média Geral  │        │
│  │ 09:00 Design │  │ 3 pendentes  │  │ 16.5/20 ⭐   │        │
│  │ [Entrar]     │  │ [Ver todas]  │  │ [Detalhes]   │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
├─────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────┐  ┌──────────────────────────┐ │
│  │ Calendário (Mini)          │  │ Frequência (Heatmap)     │ │
│  │ [Set] [Out] [Nov]          │  │ ████████░░ 85%           │ │
│  │  1  2  3  4  5             │  │ [Ver detalhes]           │ │
│  └────────────────────────────┘  └──────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Avisos Recentes                                          │  │
│  │ • [IMPORTANTE] Prova de Design Thinking — 15/Out        │  │
│  │ • [EVENTO] Palestra com Dieter Rams — 20/Out            │  │
│  │ • [FINANCEIRO] Propina de Outubro vence em 3 dias      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Player de Vídeo — Especificação:**

```
┌─────────────────────────────────────────────────────────────────┐
│  [VÍDEO: Aula 01 — Fundamentos do Design Thinking]            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │                    [PLAYER DE VÍDEO]                    │   │
│  │                                                         │   │
│  │  [▶] [━━━●━━━━━━] [1:24 / 45:00] [⚙] [⛶]             │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  🌐 Áudio: [Português ▼]  📜 Legendas: [Português ▼]         │
├─────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────┐  ┌──────────────────────────┐ │
│  │ Transcrição                │  │ Materiais                │ │
│  │ [Buscar na aula...]        │  │ 📄 Slides da Aula.pdf   │ │
│  │                            │  │ 📄 Leitura Complementar  │ │
│  │ 00:01:24 "...o design      │  │ 🔗 Link externo          │ │
│  │ thinking começa com a      │  │                          │ │
│  │ empatia..."                │  │ 📝 Minhas Anotações      │ │
│  │                            │  │ [Escrever nota...]       │ │
│  │ [Clique para ir ao         │  │                          │ │
│  │  momento do vídeo]         │  │ 💬 Discussão (12)        │ │
│  └────────────────────────────┘  └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

### 3.2 Portal do Professor (Teacher Portal)

**Objetivo:** Gestão de turmas, conteúdo, avaliações e comunicação com alunos.

```
📁 apps/web/src/app/(dashboard)/teacher/
├── page.tsx                          # Dashboard do Professor
├── layout.tsx                        # Layout com sidebar de professor
│
├── 📁 dashboard/
│   ├── page.tsx
│   └── components/
│       ├── MyClassesWidget.tsx       # Minhas turmas (hoje)
│       ├── PendingGrading.tsx        # Trabalhos para avaliar
│       ├── ClassAttendanceOverview.tsx # Resumo de frequência
│       ├── StudentMessages.tsx       # Mensagens de alunos
│       └── WeeklySchedule.tsx        # Horário da semana
│
├── 📁 classes/
│   ├── page.tsx                      # Lista de turmas
│   └── [classId]/
│       ├── page.tsx                  # Página da turma
│       ├── layout.tsx
│       ├── 📁 students/
│       │   ├── page.tsx              # Lista de alunos
│       │   └── [studentId]/
│       │       └── page.tsx          # Perfil do aluno na turma
│       ├── 📁 content/
│       │   ├── page.tsx              # Gerenciar conteúdo
│       │   └── components/
│       │       ├── LessonCreator.tsx     # Criar aula
│       │       ├── VideoUploader.tsx     # Upload de vídeo
│       │       ├── MaterialUploader.tsx  # Upload de materiais
│       │       ├── QuizBuilder.tsx       # Construtor de quiz
│       │       ├── AssignmentCreator.tsx # Criar tarefa
│       │       └── ContentReorder.tsx    # Reordenar conteúdo
│       ├── 📁 grades/
│       │   ├── page.tsx              # Lançar notas
│       │   └── components/
│       │       ├── GradeSpreadsheet.tsx  # Planilha de notas (Excel-like)
│       │       ├── GradeBulkImport.tsx   # Importar notas (CSV)
│       │       ├── GradeHistory.tsx      # Histórico de alterações
│       │       └── GradeStatistics.tsx   # Estatísticas da turma
│       ├── 📁 attendance/
│       │   ├── page.tsx              # Controle de frequência
│       │   └── components/
│       │       ├── AttendanceGrid.tsx    # Grid de presença/falta
│       │       ├── AttendanceCalendar.tsx # Calendário de frequência
│       │       └── AttendanceReport.tsx   # Relatório de frequência
│       ├── 📁 assignments/
│       │   ├── page.tsx              # Tarefas da turma
│       │   └── [assignmentId]/
│       │       └── page.tsx          # Submissões dos alunos
│       └── 📁 forum/
│           └── page.tsx              # Fórum da turma
│
├── 📁 grading/
│   ├── page.tsx                      # Central de avaliação
│   └── components/
│       ├── SubmissionViewer.tsx      # Visualizar submissão
│       ├── RubricGrader.tsx          # Avaliar por rubrica
│       ├── AnnotationTool.tsx        # Anotações no PDF
│       ├── PlagiarismReport.tsx      # Relatório de plágio
│       ├── FeedbackComposer.tsx      # Compor feedback
│       └── GradePublisher.tsx        # Publicar notas (com confirmação)
│
├── 📁 schedule/
│   ├── page.tsx                      # Meu horário
│   └── components/
│       ├── WeeklySchedule.tsx
│       ├── AvailabilitySetter.tsx    # Definir disponibilidade
│       └── SubstitutionRequest.tsx   # Solicitar substituição
│
├── 📁 messages/
│   └── page.tsx                      # Mensagens (mesmo do aluno)
│
└── 📁 profile/
    └── page.tsx                      # Perfil do professor
```

**Planilha de Notas (Grade Spreadsheet) — Especificação:**

Deve ser uma interface tipo Excel/Google Sheets, com:
- Células editáveis inline (double-click para editar)
- Fórmulas básicas (média, soma, ponderação)
- Color coding (verde = aprovado, vermelho = reprovado, amarelo = exame)
- Filtros e ordenação
- Bulk actions (selecionar múltiplos alunos, aplicar nota)
- Histórico de revisão (quem mudou o quê e quando)
- Botão "Publicar Notas" com modal de confirmação e preview

```
┌─────────────────────────────────────────────────────────────────┐
│  Turma: Design Thinking 2026.1    [📤 Importar] [📊 Estatísticas]│
├─────────────────────────────────────────────────────────────────┤
│  Aluno              │ T1 │ T2 │ T3 │ Média │ Status │ Ações    │
├─────────────────────┼────┼────┼────┼───────┼────────┼──────────┤
│  👤 Maria Silva     │ 18 │ 16 │ 20 │ 18.0  │ 🟢 Aprov│ [✏️]    │
│  👤 João Santos     │ 12 │ 10 │ 14 │ 12.0  │ 🟡 Exame│ [✏️]    │
│  👤 Ana Costa       │ 08 │ 06 │ 10 │ 08.0  │ 🔴 Repro│ [✏️]    │
├─────────────────────┴────┴────┴────┴───────┴────────┴──────────┤
│  [Selecionar Todos]  [Aplicar Fórmula]  [🚀 Publicar Notas]    │
└─────────────────────────────────────────────────────────────────┘
```

---

### 3.3 Portal do Coordenador (Coordinator Portal)

**Objetivo:** Gestão acadêmica de alto nível. Turmas, professores, grades curriculares, relatórios.

```
📁 apps/web/src/app/(dashboard)/coordinator/
├── page.tsx                          # Dashboard do Coordenador
├── layout.tsx
│
├── 📁 dashboard/
│   ├── page.tsx
│   └── components/
│       ├── EnrollmentOverview.tsx    # Visão geral de matrículas
│       ├── TeacherWorkload.tsx       # Carga horária dos professores
│       ├── ClassOccupancy.tsx        # Ocupação das turmas
│       ├── AcademicCalendarWidget.tsx # Calendário acadêmico
│       └── AlertsPanel.tsx           # Alertas: turmas lotadas, conflitos
│
├── 📁 classes/
│   ├── page.tsx                      # Gerenciar turmas
│   └── components/
│       ├── ClassList.tsx             # Lista com filtros
│       ├── ClassCreator.tsx          # Criar turma
│       ├── ClassEditor.tsx           # Editar turma
│       ├── EnrollmentManager.tsx     # Gerenciar matrículas
│       ├── ClassScheduleBuilder.tsx  # Construtor de horários
│       └── ClassCapacityManager.tsx  # Gerenciar vagas
│
├── 📁 teachers/
│   ├── page.tsx                      # Gerenciar professores
│   └── components/
│       ├── TeacherList.tsx
│       ├── TeacherProfile.tsx
│       ├── TeacherAssignment.tsx     # Atribuir disciplinas
│       ├── TeacherScheduleViewer.tsx # Ver horário do professor
│       └── TeacherEvaluation.tsx     # Avaliação de desempenho
│
├── 📁 curriculum/
│   ├── page.tsx                      # Grade curricular
│   └── components/
│       ├── CurriculumBuilder.tsx     # Construtor de grade
│       ├── SubjectManager.tsx        # Gerenciar disciplinas
│       ├── PrerequisiteMapper.tsx    # Mapa de pré-requisitos
│       └── CurriculumTimeline.tsx    # Timeline da grade
│
├── 📁 students/
│   ├── page.tsx                      # Todos os alunos
│   └── components/
│       ├── StudentSearch.tsx         # Busca avançada
│       ├── StudentProfileViewer.tsx  # Ver perfil completo
│       ├── AcademicRecordViewer.tsx  # Histórico acadêmico
│       └── TransferManager.tsx       # Transferências
│
├── 📁 reports/
│   ├── page.tsx                      # Relatórios acadêmicos
│   └── components/
│       ├── EnrollmentReport.tsx
│       ├── PerformanceReport.tsx
│       ├── AttendanceReport.tsx
│       ├── DropoutRiskReport.tsx     # Alunos em risco de evasão
│       ├── GradeDistributionChart.tsx # Distribuição de notas
│       └── ReportExporter.tsx        # Exportar PDF/Excel
│
├── 📁 calendar/
│   ├── page.tsx                      # Calendário acadêmico
│   └── components/
│       ├── AcademicCalendarEditor.tsx
│       ├── EventCreator.tsx
│       ├── ExamScheduler.tsx         # Agendar provas
│       └── HolidayManager.tsx        # Gerenciar feriados
│
└── 📁 settings/
    └── page.tsx                      # Configurações do departamento
```

---

### 3.4 Portal Administrativo (Admin Portal)

**Objetivo:** Controle total do sistema. Usuários, permissões, configurações, plugins, financeiro.

```
📁 apps/web/src/app/(dashboard)/admin/
├── page.tsx                          # Dashboard Administrativo
├── layout.tsx                        # Layout com sidebar admin (mais compacta)
│
├── 📁 dashboard/
│   ├── page.tsx
│   └── components/
│       ├── SystemHealthWidget.tsx    # Status dos serviços (CPU, RAM, DB)
│       ├── UserStatsWidget.tsx       # Total de usuários ativos
│       ├── RevenueWidget.tsx         # Receita mensal
│       ├── ActivePluginsWidget.tsx   # Plugins ativos
│       ├── RecentActivityFeed.tsx    # Log de atividades recentes
│       └── AlertsSystem.tsx          # Alertas críticos do sistema
│
├── 📁 users/
│   ├── page.tsx                      # Gerenciar usuários
│   └── components/
│       ├── UserTable.tsx             # Tabela avançada com filtros
│       ├── UserCreator.tsx           # Criar usuário
│       ├── UserImporter.tsx          # Importar usuários (CSV)
│       ├── RoleManager.tsx           # Gerenciar papéis (RBAC)
│       ├── PermissionMatrix.tsx      # Matriz de permissões
│       └── UserActivityLog.tsx       # Log de atividades por usuário
│
├── 📁 plugins/
│   ├── page.tsx                      # Gerenciar plugins
│   └── components/
│       ├── PluginMarketplace.tsx     # Marketplace de plugins
│       ├── PluginCard.tsx            # Card de plugin (instalar/ativar/desativar)
│       ├── PluginConfigPanel.tsx     # Painel de configuração do plugin
│       ├── PluginPermissions.tsx     # Permissões do plugin
│       └── PluginUpdateManager.tsx   # Gerenciar atualizações
│
├── 📁 settings/
│   ├── page.tsx                      # Configurações globais
│   └── components/
│       ├── GeneralSettings.tsx       # Nome da escola, logo, favicon
│       ├── AcademicSettings.tsx      # Ano letivo, períodos, notas mínimas
│       ├── EmailSettings.tsx         # SMTP, templates de e-mail
│       ├── SMSSettings.tsx           # Gateway SMS
│       ├── PaymentSettings.tsx       # Gateways de pagamento
│       ├── NotificationSettings.tsx  # Templates de notificação
│       ├── ThemeSettings.tsx         # Cores, fontes, logo
│       ├── LanguageSettings.tsx      # Idiomas ativos, idioma padrão
│       ├── BackupSettings.tsx        # Configuração de backup
│       ├── SecuritySettings.tsx      # 2FA, sessão, senhas
│       └── IntegrationSettings.tsx   # APIs, webhooks, LDAP
│
├── 📁 finance/
│   ├── page.tsx                      # Financeiro institucional
│   └── components/
│       ├── RevenueDashboard.tsx
│       ├── InvoiceManager.tsx
│       ├── PaymentTracker.tsx
│       ├── ScholarshipManager.tsx    # Bolsas e descontos
│       ├── PayrollViewer.tsx         # Folha de pagamento (integração RH)
│       └── FinancialReports.tsx
│
├── 📁 analytics/
│   ├── page.tsx                      # Analytics e BI
│   └── components/
│       ├── EnrollmentTrendsChart.tsx
│       ├── RetentionRateChart.tsx
│       ├── RevenueForecastChart.tsx
│       ├── UserEngagementHeatmap.tsx
│       ├── CustomReportBuilder.tsx   # Construtor de relatórios customizados
│       └── DataExportTool.tsx        # Exportar dados
│
├── 📁 logs/
│   ├── page.tsx                      # Logs do sistema
│   └── components/
│       ├── SystemLogsViewer.tsx      # Logs técnicos
│       ├── AuditTrailViewer.tsx      # Auditoria (quem fez o quê)
│       ├── ErrorLogViewer.tsx        # Logs de erro
│       └── SecurityLogViewer.tsx     # Logs de segurança
│
└── 📁 support/
    ├── page.tsx                      # Suporte e tickets
    └── components/
        ├── TicketList.tsx
        ├── TicketDetail.tsx
        ├── KnowledgeBaseManager.tsx  # Base de conhecimento
        └── FAQManager.tsx            # Gerenciar FAQs
```

**Plugin Marketplace — Especificação:**

```
┌─────────────────────────────────────────────────────────────────┐
│  🔌 Plugin Marketplace                              [🔍 Buscar] │
├─────────────────────────────────────────────────────────────────┤
│  Categorias: [Todos] [Acadêmico] [Financeiro] [Comunicação]   │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  📊 BI Analytics Plugin          v2.1.0    [✅ Ativo]   │  │
│  │  Dashboards avançados e relatórios personalizados        │  │
│  │  [⚙️ Configurar]  [⬆️ Atualizar]  [❌ Desativar]        │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  📚 Biblioteca Digital           v1.5.2    [⬇️ Instalar]│  │
│  │  Gestão de acervo, empréstimos e repositório digital     │  │
│  │  [📖 Detalhes]  [⭐ 4.8]  [💬 120 reviews]               │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  🎙️ S2ST Dublagem AI            v3.0.1    [⬇️ Instalar]│  │
│  │  Dublagem automática de videoaulas com IA                │  │
│  │  [📖 Detalhes]  [⭐ 5.0]  [💬 89 reviews]                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 3.5 Portal do Encarregado (Parent/Guardian Portal)

**Objetivo:** Acompanhamento do filho/aluno. Notas, frequência, financeiro, comunicação.

```
📁 apps/web/src/app/(dashboard)/guardian/
├── page.tsx                          # Dashboard do Encarregado
├── layout.tsx
│
├── 📁 dashboard/
│   ├── page.tsx
│   └── components/
│       ├── ChildSelector.tsx         # Seletor de filho (se múltiplos)
│       ├── ChildOverviewCard.tsx     # Resumo do filho
│       ├── AcademicProgressWidget.tsx # Progresso acadêmico
│       ├── AttendanceSummary.tsx     # Resumo de frequência
│       ├── UpcomingAssignments.tsx   # Tarefas pendentes
│       ├── FinancialSummary.tsx      # Resumo financeiro
│       └── RecentGradesWidget.tsx    # Notas recentes
│
├── 📁 child/
│   └── [studentId]/
│       ├── page.tsx                  # Perfil do filho
│       ├── 📁 grades/
│       │   └── page.tsx              # Notas do filho
│       ├── 📁 attendance/
│       │   └── page.tsx              # Frequência do filho
│       ├── 📁 schedule/
│       │   └── page.tsx              # Horário do filho
│       └── 📁 behavior/
│           └── page.tsx              # Comportamento/disciplina
│
├── 📁 finance/
│   ├── page.tsx                      # Financeiro
│   └── components/
│       ├── InvoiceList.tsx
│       ├── PaymentButton.tsx
│       └── PaymentHistory.tsx
│
├── 📁 messages/
│   └── page.tsx                      # Comunicação com escola
│
└── 📁 documents/
    └── page.tsx                      # Documentos do filho
```

---

### 3.6 Portal do Bibliotecário (Librarian Portal)

```
📁 apps/web/src/app/(dashboard)/librarian/
├── page.tsx                          # Dashboard da Biblioteca
├── layout.tsx
│
├── 📁 dashboard/
│   ├── page.tsx
│   └── components/
│       ├── CatalogStatsWidget.tsx    # Estatísticas do acervo
│       ├── LoansOverviewWidget.tsx   # Empréstimos ativos
│       ├── OverdueLoansWidget.tsx    # Atrasos
│       ├── NewArrivalsWidget.tsx     # Novas aquisições
│       └── ReservationQueueWidget.tsx # Fila de reservas
│
├── 📁 catalog/
│   ├── page.tsx                      # Catálogo
│   └── components/
│       ├── BookSearch.tsx            # Busca avançada
│       ├── BookDetail.tsx            # Detalhe do livro
│       ├── BookAdder.tsx             # Adicionar livro
│       ├── BookEditor.tsx            # Editar livro
│       ├── BarcodeScanner.tsx        # Scanner de código de barras
│       └── DigitalRepository.tsx     # Repositório digital
│
├── 📁 loans/
│   ├── page.tsx                      # Empréstimos
│   └── components/
│       ├── LoanManager.tsx           # Gerenciar empréstimos
│       ├── ReturnProcessor.tsx       # Processar devolução
│       ├── OverdueManager.tsx        # Gerenciar atrasos
│       └── LoanHistory.tsx           # Histórico
│
├── 📁 users/
│   └── page.tsx                      # Usuários da biblioteca
│
└── 📁 reports/
    └── page.tsx                      # Relatórios da biblioteca
```

---

### 3.7 Portal do RH (HR Portal)

```
📁 apps/web/src/app/(dashboard)/hr/
├── page.tsx                          # Dashboard de RH
├── layout.tsx
│
├── 📁 dashboard/
│   ├── page.tsx
│   └── components/
│       ├── EmployeeCountWidget.tsx
│       ├── PayrollOverviewWidget.tsx
│       ├── LeaveRequestsWidget.tsx
│       └── RecruitmentPipelineWidget.tsx
│
├── 📁 employees/
│   ├── page.tsx
│   └── components/
│       ├── EmployeeList.tsx
│       ├── EmployeeProfile.tsx
│       ├── EmployeeOnboarding.tsx
│       └── EmployeeOffboarding.tsx
│
├── 📁 payroll/
│   ├── page.tsx
│   └── components/
│       ├── PayrollProcessor.tsx
│       ├── PayslipGenerator.tsx
│       └── PayrollReports.tsx
│
├── 📁 recruitment/
│   ├── page.tsx
│   └── components/
│       ├── JobPostingManager.tsx
│       ├── ApplicantTracker.tsx
│       └── InterviewScheduler.tsx
│
├── 📁 leave/
│   ├── page.tsx
│   └── components/
│       ├── LeaveRequestManager.tsx
│       ├── LeaveBalanceViewer.tsx
│       └── LeaveCalendar.tsx
│
└── 📁 performance/
    ├── page.tsx
    └── components/
        ├── PerformanceReviewCycle.tsx
        ├── EvaluationFormBuilder.tsx
        └── PerformanceReports.tsx
```

---

## 4. 🔐 FLUXOS DE AUTENTICAÇÃO

### 4.1 Login

```
📁 apps/web/src/app/(auth)/
├── layout.tsx                        # Layout de auth (sem sidebar)
│
├── login/
│   ├── page.tsx
│   └── components/
│       ├── LoginForm.tsx             # Email + Senha + Lembrar-me
│       ├── SocialLoginButtons.tsx    # Google, Microsoft, Apple
│       ├── SSOButton.tsx             # Login via SSO institucional
│       ├── ForgotPasswordLink.tsx
│       └── RegisterLink.tsx
│
├── register/
│   ├── page.tsx
│   └── components/
│       ├── RegistrationForm.tsx      # Dados pessoais + validação
│       ├── EmailVerification.tsx     # Verificação de e-mail
│       └── SuccessMessage.tsx
│
├── forgot-password/
│   ├── page.tsx
│   └── components/
│       ├── EmailInputForm.tsx
│       ├── ResetLinkSent.tsx
│       └── BackToLoginLink.tsx
│
├── reset-password/
│   └── [token]/
│       └── page.tsx
│           └── components/
│               ├── NewPasswordForm.tsx
│               └── PasswordStrengthMeter.tsx
│
├── verify-email/
│   └── [token]/
│       └── page.tsx
│
└── mfa/
    └── page.tsx
        └── components/
            ├── TOTPSetup.tsx         # QR Code + código
            ├── TOTPVerify.tsx        # Inserir código 2FA
            ├── BackupCodes.tsx       # Códigos de backup
            └── SMSVerify.tsx         # Verificação SMS
```

**Tela de Login — Especificação:**

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌────────────────────────┐    ┌────────────────────────────┐  │
│  │                        │    │                            │  │
│  │   [ILUSTRAÇÃO/VIDEO    │    │   Bem-vindo à G Designer   │  │
│  │    DE DESIGN]          │    │   School                   │  │
│  │                        │    │                            │  │
│  │   "Design your future" │    │   [📧 E-mail]              │  │
│  │                        │    │   [🔒 Senha]               │  │
│  │                        │    │   [☑️] Lembrar-me          │  │
│  │                        │    │                            │  │
│  │                        │    │   [🔵 Entrar]              │  │
│  │                        │    │                            │  │
│  │                        │    │   ─── ou ───               │  │
│  │                        │    │                            │  │
│  │                        │    │   [🔴 Google]  [🔵 Microsoft]│  │
│  │                        │    │                            │  │
│  │                        │    │   Esqueceu a senha?        │  │
│  │                        │    │   Não tem conta? Registre-se│  │
│  │                        │    │                            │  │
│  └────────────────────────┘    └────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. 📱 MOBILE APP (Flutter)

### 5.1 Estrutura de Telas

```
📁 apps/mobile/lib/screens/
├── splash_screen.dart
├── onboarding_screen.dart
│
├── auth/
│   ├── login_screen.dart
│   ├── register_screen.dart
│   └── forgot_password_screen.dart
│
├── student/
│   ├── student_dashboard.dart
│   ├── course_list_screen.dart
│   ├── course_detail_screen.dart
│   ├── lesson_player_screen.dart      # Player de vídeo nativo
│   ├── assignment_list_screen.dart
│   ├── assignment_detail_screen.dart
│   ├── grade_report_screen.dart
│   ├── schedule_screen.dart
│   ├── finance_screen.dart
│   ├── document_list_screen.dart
│   ├── message_list_screen.dart
│   ├── chat_screen.dart
│   ├── notification_screen.dart
│   └── profile_screen.dart
│
├── teacher/
│   ├── teacher_dashboard.dart
│   ├── class_list_screen.dart
│   ├── class_detail_screen.dart
│   ├── grade_entry_screen.dart
│   ├── attendance_screen.dart
│   └── submission_list_screen.dart
│
├── shared/
│   ├── search_screen.dart
│   ├── settings_screen.dart
│   └── help_screen.dart
│
└── widgets/
    ├── aos_app_bar.dart
    ├── aos_bottom_nav.dart
    ├── aos_card.dart
    ├── aos_button.dart
    ├── aos_input.dart
    ├── aos_avatar.dart
    ├── aos_badge.dart
    ├── aos_skeleton.dart
    ├── aos_empty_state.dart
    ├── aos_error_state.dart
    └── aos_pull_to_refresh.dart
```

### 5.2 Bottom Navigation (5 Tabs)

```dart
// apps/mobile/lib/widgets/aos_bottom_nav.dart

BottomNavigationBar(
  items: [
    BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Início'),
    BottomNavigationBarItem(icon: Icon(Icons.school), label: 'Cursos'),
    BottomNavigationBarItem(icon: Icon(Icons.calendar_today), label: 'Agenda'),
    BottomNavigationBarItem(icon: Icon(Icons.message), label: 'Mensagens'),
    BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Perfil'),
  ],
)
```

---

## 6. 🎨 PÁGINAS ESPECIAIS E ESTADOS

### 6.1 Empty States

Cada lista vazia deve ter:
- Ilustração customizada (SVG, animada se possível)
- Título claro (ex: "Nenhuma tarefa pendente")
- Descrição contextual (ex: "Você está em dia! Novas tarefas aparecerão aqui.")
- Ação primária (ex: "[Explorar Cursos]") — quando relevante

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    [ILUSTRAÇÃO: 📚 + ✨]                        │
│                                                                 │
│              Nenhuma tarefa pendente                            │
│                                                                 │
│     Você está em dia! Novas tarefas aparecerão aqui.          │
│                                                                 │
│              [🎯 Explorar Cursos]                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Error States

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    [ILUSTRAÇÃO: 🔧 + 😕]                        │
│                                                                 │
│              Algo deu errado                                    │
│                                                                 │
│     Não foi possível carregar suas notas.                     │
│     Tente novamente ou entre em contato com o suporte.        │
│                                                                 │
│              [🔄 Tentar Novamente]  [💬 Suporte]                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3 Loading States

- **Skeleton screens** para todo conteúdo dinâmico
- **Shimmer effect** nos skeletons
- **Progressive loading** — carregar texto primeiro, imagens depois
- **Spinner** apenas para ações de botão (não para página inteira)

### 6.4 Onboarding

```
📁 apps/web/src/app/(auth)/onboarding/
├── page.tsx
└── components/
    ├── OnboardingStep1.tsx           # Bem-vindo + apresentação
    ├── OnboardingStep2.tsx           # Configurar perfil
    ├── OnboardingStep3.tsx           # Escolher idioma e tema
    ├── OnboardingStep4.tsx           # Tour guiado (spotlight)
    ├── OnboardingProgress.tsx        # Barra de progresso
    └── OnboardingNavigator.tsx       # Próximo / Pular / Anterior
```

---

## 7. 🌐 COMPONENTES DE I18N E ACESSIBILIDADE

### 7.1 Seletor de Idioma

Deve estar sempre visível no TopBar (ou no footer mobile). Dropdown com bandeiras + nome do idioma.

### 7.2 Acessibilidade

- **Teclado:** Todos os elementos interativos devem ser acessíveis via Tab
- **Screen Reader:** Todos os ícones devem ter `aria-label`
- **Contraste:** Ratio mínimo 4.5:1 para texto normal, 3:1 para grandes
- **Motion:** Respeitar `prefers-reduced-motion`
- **Focus:** Anel de foco visível e estilizado (não padrão do navegador)
- **Skip Link:** Link "Pular para conteúdo" no topo da página
- **Landmarks:** Uso correto de `<main>`, `<nav>`, `<aside>`, `<header>`, `<footer>`

---

## 8. 📋 CHECKLIST DE ENTREGA

O designer deve entregar:

- [ ] **Design Tokens** completos (cores, tipografia, espaçamento, sombras, animações)
- [ ] **Component Library** no Figma/Storybook com todos os estados
- [ ] **Protótipos interativos** dos 5 principais fluxos:
  1. Login → Dashboard do Aluno → Aula → Entrega de Tarefa
  2. Login → Dashboard do Professor → Lançar Notas → Publicar
  3. Login → Dashboard do Admin → Instalar Plugin → Configurar
  4. Mobile: Login → Dashboard → Notificações → Aula
  5. Onboarding completo
- [ ] **Responsive designs** para: 320px, 768px, 1024px, 1440px, 1920px
- [ ] **Dark mode** para todas as telas
- [ ] **Accessibility audit** com checklist WCAG 2.1 AAA
- [ ] **Micro-interactions** documentadas (hover, click, loading, success, error)
- [ ] **Empty states** para todas as listas
- [ ] **Error states** para todas as operações
- [ ] **Loading states** para todas as páginas
- [ ] **Icon library** completa (500+ ícones customizados ou Lucide/Phosphor)
- [ ] **Illustration set** para empty states, onboarding, errors (10+ ilustrações)
- [ ] **Design handoff** com especificações de pixel, cores hex, tokens, e assets exportados

---

## 9. 🎯 PRINCÍPIOS DE DESIGN INQUEBRÁVEIS

1. **Clareza acima de tudo:** O usuário deve entender o que fazer em 3 segundos
2. **Consistência absoluta:** Mesmos padrões em TODOS os módulos
3. **Feedback imediato:** Toda ação tem reação visual em <200ms
4. **Progressive disclosure:** Mostrar apenas o essencial, revelar detalhes sob demanda
5. **Mobile-first:** Se funciona no mobile, funciona no desktop
6. **Performance perceptível:** Transições suaves, nada travado
7. **Acessibilidade universal:** O sistema deve funcionar para TODOS
8. **Delightful details:** Micro-interactions que surpreendem positivamente
9. **Data-driven:** Dashboards e estatísticas sempre visíveis
10. **Context-aware:** A interface muda conforme o papel do usuário

---

## 10. 🏁 CONCLUSÃO

Este prompt especifica **TODA** a interface do AOS. Cada arquivo listado deve ser criado como um componente React (web) ou Widget Flutter (mobile), seguindo o Design System definido. A experiência deve ser tão polida quanto Notion, tão rápida quanto Linear, e tão funcional quanto Canvas — tudo em uma única plataforma unificada.

**A G Designer School merece o melhor design do mundo.**
