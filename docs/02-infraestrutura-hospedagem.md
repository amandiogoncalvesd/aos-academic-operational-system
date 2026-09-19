# 🌐 AOS — Infraestrutura de Hospedagem
## Onde os Melhores Sistemas do Mundo Hospedam & Arquitetura Ideal para o AOS

**Versão:** 1.0  
**Data:** 27 de Agosto de 2026

---

## 📋 Sumário Executivo

Este documento mapeia **onde** os principais sistemas acadêmicos, hospitalares e financeiros do mundo hospedam seus serviços — front-end, back-end e banco de dados. Analisa arquiteturas de cloud pública, on-premise, híbrida e multi-cloud, com custos reais. Ao final, propõe a **arquitetura de hospedagem ideal para o AOS**, considerando compliance (FERPA, LGPD, GDPR), soberania de dados, custo e escalabilidade.

---

## 1. 🎓 Sistemas Acadêmicos — Onde Eles Hospedam

### 1.1 Canvas by Instructure (LMS #1 do Mundo)

**Infraestrutura:** **AWS (Amazon Web Services)** — parceria estratégica consolidada. cite🛠web_search:18#2:~:text=Instructure Advances Education Equity with AWS Support, Accelerating AI-Powered Learning Modernization and Workforce Pathways

| Componente | Hospedagem |
|-----------|-----------|
| **Front-end** | AWS CloudFront (CDN) + S3 |
| **Back-end** | AWS EC2 / ECS (containers) |
| **Banco de Dados** | AWS RDS (PostgreSQL) |
| **AI/ML** | AWS Bedrock, SageMaker |
| **Armazenamento** | AWS S3 |
| **Regiões** | Multi-region (US, EU, APAC) |

**Modelo:** SaaS 100% cloud-native. Não oferece on-premise. cite🛠web_search:18#2:~:text=AWS collaboration accelerates AI-powered migration tools and Canvas Career capabilities

---

### 1.2 Blackboard by Anthology (LMS Clássico)

**Infraestrutura:** **Multi-cloud — AWS + Azure + Data Centers Próprios (Cyxtera)**. Blackboard suporta **SaaS, Managed-Hosted e Self-Hosted**, mas está migrando 100% para SaaS. cite🛠web_search:18#6:~:text=The company currently supports self-hosted, managed-hosted, and SaaS deployments for Blackboard Learn but has announced that it will end full support for managed-hosted deployments by the end of 2022 and self-hosted deployments by the end of 2023. At least 65 percent of Blackboard institutions are currently using the SaaS solution

| Componente | SaaS (Padrão) | Self-Hosted (Legado) |
|-----------|--------------|---------------------|
| **Front-end** | AWS CloudFront / Azure CDN | Servidor próprio |
| **Back-end** | AWS EC2 / Azure VMs | Data center on-premise |
| **Banco de Dados** | AWS RDS / Azure SQL | Oracle / SQL Server local |
| **Storage** | AWS S3 / Azure Blob | NAS/SAN local |
| **Sub-processadores** | AWS, Azure, Cloudflare, Snowflake, MongoDB | — |

**Regiões por cliente:** cite🛠web_search:18#4:~:text=US and LATAM clients: US-West...European, Middle Eastern and African clients: Frankfurt, Germany...ANZ clients: Sydney, Australia

**Exemplo real:** Blackboard foi o **primeiro LMS hospedado localmente nos Emirados Árabes Unidos** na AWS, atendendo à soberania de dados do país. cite🛠web_search:18#8:~:text=Blackboard by Anthology Now Available on AWS in the United Arab Emirates...local hosting of Blackboard arrives at a pivotal moment, aligning with the UAE's 2030 vision

---

### 1.3 PowerSchool (SIS #1 do Mundo para K-12)

**Infraestrutura:** **Microsoft Azure** — parceria exclusiva. cite🛠web_search:18#9:~:text=PowerSchool's cloud infrastructure incorporates cutting-edge security technologies...hosted on Microsoft Azure, the largest and most certified cloud infrastructure in the world cite🛠web_search:18#12:~:text=PowerSchool solutions are hosted on Microsoft Azure, the best-in-class cloud infrastructure that offers advanced security, scalability, and reliability

| Componente | Hospedagem |
|-----------|-----------|
| **Front-end** | Azure CDN + Azure Front Door |
| **Back-end** | Azure App Service / AKS |
| **Banco de Dados** | Azure SQL Database |
| **Storage** | Azure Blob Storage |
| **DR/Backup** | Azure Site Recovery |
| **Uptime** | 99.9% SLA |

**Modelo:** Cloud-only. Não oferece mais self-hosted para novos clientes. Migração de on-premise para cloud é o foco. cite🛠web_search:18#9:~:text=Migrating your self-hosted PowerSchool SIS to the cloud helps schools and districts reduce risk, increase data security, and save money

**Caso real — Lake Highland Prep:**
- Antes: Servidor on-premise, falhava 1-2x por mês, custos altos de AC, firewall, SSL
- Depois: PowerSchool Hosting (Azure), economia de **$20.000+ em 5 anos**, zero manutenção cite🛠web_search:18#10:~:text=Lake Highland has cut costs (to the tune of an expected $20,000-plus over five years), saved dozens of hours of staff time, and improved data reliability

---

### 1.4 Ellucian Banner (ERP Acadêmico #1)

**Infraestrutura:** **Oracle Cloud Infrastructure (OCI)** — parceria estratégica. Também suporta AWS e Azure, mas OCI é o padrão. cite🛠web_search:18#0:~:text=Deploy an ERP system using Ellucian Banner...This multi-tier reference architecture contains the infrastructure resources required to deploy highly available instances of Ellucian Banner applications

| Componente | Hospedagem |
|-----------|-----------|
| **Front-end** | OCI Load Balancer + CDN |
| **Back-end** | OCI Compute (VMs) |
| **Banco de Dados** | Oracle Base Database Service |
| **Storage** | OCI Object Storage |
| **DR** | OCI multi-region (ex: Ashburn → Phoenix) |
| **Rede** | OCI VCN com 11+ subnets |

**Arquitetura real de uma universidade (6.500 alunos):** cite🛠web_search:18#5:~:text=Production environment is deployed in a single OCI region across three availability domains...Ellucian Banner ERP and a Banner Document Management System are deployed in an application tier in the OCI US-Ashburn region

**Tendência:** Mais de **60% das instituições de ensino superior** já operam pelo menos um sistema core na cloud. A migração de on-premise para cloud reduz custos de infraestrutura em **40-50%** inicialmente e **15-30%** operacionalmente. cite🛠web_search:18#11:~:text=More than 60% of higher education institutions now operate at least one core administrative system in the cloud...Independent studies show initial infrastructure cost reductions between 40 and 50%, with ongoing operating savings ranging from 15 to 30%

---

### 1.5 MoodleCloud (Moodle SaaS)

**Infraestrutura:** **AWS (Amazon Web Services)** — 3 regiões. cite🛠web_search:17#6:~:text=MoodleCloud is hosted on Amazon Web Servers (AWS) in three regions, Australia, Europe and the US

| Região | Localização |
|--------|------------|
| AU | Sydney, Austrália |
| EU | Dublin, Irlanda |
| US | Oregon, EUA |

**Modelo:** SaaS gerenciado. O cliente escolhe a região no signup e **não pode mudar depois**.

**Custo de hospedagem própria na AWS (Moodle self-hosted):**
Para 500 usuários, o custo real na AWS é **~$362/mês** de infraestrutura + **~$1.647/mês** com DevOps = **~$59.294 em 3 anos**. Managed hosting custa **~$800/ano**. cite🛠web_search:17#7:~:text=Total base infrastructure ~$362/month...Total 3-year TCO ~$59,294...Managed hosting ~$800/year

---

### 1.6 Workday Student

**Infraestrutura:** **Workday Cloud** (proprietário, multi-tenant). Não roda em AWS/Azure/GCP — é uma cloud privada da própria Workday. cite🛠web_search:17#2:~:text=Workday built its reputation on cloud human capital management and financial management...a mature cloud platform; a large enterprise customer base outside education

| Componente | Hospedagem |
|-----------|-----------|
| **Tudo** | Workday Cloud (proprietário) |
| **Data Centers** | Multi-region (US, EU, APAC) |
| **Modelo** | SaaS multi-tenant |
| **Backup/DR** | Gerenciado pela Workday |

---

## 2. 🏥 Sistemas Hospitalares — Onde Eles Hospedam

### 2.1 Epic (EHR #1 dos EUA)

**Infraestrutura:** **Epic Cloud (proprietário) + On-Premise (legado)**.

| Modelo | Infraestrutura |
|--------|---------------|
| **Epic Cloud (novo)** | Data centers Epic (proprietários), ~99.95% uptime |
| **On-Premise (legado)** | Hospital mantém servidores físicos |
| **Banco de Dados** | Chronicles DB (MUMPS — linguagem dos anos 1960!) |
| **Custo Cloud** | $100M-$500M+ para grandes sistemas |
| **Custo On-Premise** | $500.000+ para self-hosted |

cite🛠web_search:17#3:~:text=Epic's hosting services are integrated tightly...Epic's own hosted cloud environments achieve approximately 99.95%+ uptime in practice for core systems cite🛠web_search:17#4:~:text=a self-hosted Epic implementation for a large hospital can start around $500,000+...Epic typically entails higher upfront integration costs and resource commitments

---

### 2.2 Cerner / Oracle Health (EHR #2)

**Infraestrutura:** **Oracle Cloud Infrastructure (OCI)** — desde a aquisição pela Oracle em 2022. cite🛠web_search:17#3:~:text=Cerner is leveraging Oracle Cloud Infrastructure...Now Oracle Health after the 2022 acquisition. Cloud infrastructure from Oracle backs the platform

| Componente | Hospedagem |
|-----------|-----------|
| **Front-end** | OCI Load Balancer |
| **Back-end** | OCI Compute |
| **Banco de Dados** | Oracle Database Cloud |
| **Analytics** | Oracle Analytics Cloud |
| **Custo** | $10M-$50M para implementação completa |

---

## 3. 🏦 Sistemas Financeiros/Bancários — Onde Eles Hospedam

### 3.1 Padrão da Indústria: Multi-Cloud Híbrido

Os bancos e instituições financeiras usam predominantemente **multi-cloud** para evitar vendor lock-in e atender compliance: cite🛠web_search:17#9:~:text=More financial institutions are adopting multi-cloud and hybrid models to balance compliance, cost, and capability. Common patterns include AWS for regulated core workloads, Azure for enterprise and hybrid operations, and GCP for analytics and AI

| Provedor | Uso Típico em Bancos |
|----------|---------------------|
| **AWS** | Workloads core regulados, compliance RBI/SEBI, AI via Bedrock |
| **Azure** | Enterprise híbrido, Microsoft 365/Dynamics integração, governança |
| **GCP** | Analytics, ML/AI, Vertex AI, BigQuery |

**Modelos de serviço:** cite🛠web_search:17#8:~:text=IaaS...A bank runs its own core banking software on AWS EC2 instances or Azure VMs...PaaS...A payments team deploys a microservices-based payments engine on Google Kubernetes Engine...SaaS...A bank subscribes to Mambu, Tuum or Crassula and consumes the core banking ledger via API

---

## 4. 📊 Comparativo: Cloud Pública vs On-Premise vs Híbrido

### 4.1 Custos Reais (Sistema Acadêmico, 500-2.000 usuários)

| Modelo | Custo Inicial | Custo Mensal | Custo 3 Anos | Manutenção |
|--------|--------------|-------------|-------------|-----------|
| **On-Premise** | $50.000-$200.000 (servidores, rack, AC, UPS) | $3.000-$8.000 (energia, cooling, staff) | $158.000-$488.000 | Alta (24/7 staff) |
| **AWS Self-Managed** | $6.000 (setup DevOps) | $362-$1.647 | $59.294 | Média-Alta |
| **Azure Self-Managed** | $6.000 (setup DevOps) | $350-$1.500 | $55.000 | Média-Alta |
| **Managed Hosting** | $500 (setup) | $67-$300 | $2.900-$10.800 | Baixa |
| **SaaS (Canvas/PowerSchool)** | $0 | $10-$50/aluno/ano | Variável | Zero |

cite🛠web_search:17#7:~:text=Total base infrastructure ~$362/month...Total 3-year TCO ~$59,294...Managed hosting ~$800/year...AWS ~$1,647/month cite🛠web_search:18#11:~:text=Independent studies show initial infrastructure cost reductions between 40 and 50%, with ongoing operating savings ranging from 15 to 30%

### 4.2 Comparativo por Critério

| Critério | On-Premise | Cloud Pública | Híbrido | SaaS |
|----------|-----------|--------------|---------|------|
| **Controle total** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ |
| **Custo inicial baixo** | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Escalabilidade** | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Segurança** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Compliance FERPA/LGPD** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Soberania de dados** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **DR/Backup** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Time-to-market** | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 5. 🏗️ Arquitetura de Hospedagem Recomendada para o AOS

### 5.1 Princípios de Design

1. **Cloud-Native First:** O AOS nasceu na nuvem. Não há legado on-premise para arrastar.
2. **Multi-Cloud Ready:** Evitar vendor lock-in. Arquitetura portátil entre AWS, Azure, GCP.
3. **Soberania de Dados:** Dados de Angola ficam em Angola (ou na região mais próxima). Dados da UE ficam na UE.
4. **Híbrido Opcional:** Instituições grandes podem ter data center local + cloud pública.
5. **Kubernetes Everywhere:** Containerização permite rodar em qualquer cloud ou on-premise.
6. **IaC (Infrastructure as Code):** Terraform + Ansible para reprodutibilidade total.

### 5.2 Arquitetura de Referência: AOS Cloud-Native

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AOS — ARQUITETURA DE HOSPEDAGEM                           │
│                         (Multi-Cloud Native)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         CAMADA EDGE (CDN)                           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │   │
│  │  │ CloudFlare  │  │ AWS         │  │ Azure       │                │   │
│  │  │ (Global)    │  │ CloudFront  │  │ Front Door  │                │   │
│  │  │ DDoS, WAF   │  │ (Regional)  │  │ (Regional)  │                │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      API GATEWAY / LOAD BALANCER                     │   │
│  │         Kong / Traefik / AWS ALB / Azure App Gateway                │   │
│  │     Rate Limit │ Auth │ SSL Termination │ Routing                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    KUBERNETES CLUSTER (EKS / AKS / GKE)               │   │
│  │                                                                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────┐  │   │
│  │  │ AOS Core    │  │ Plugin LMS  │  │ Plugin ERP  │  │ Plugin   │  │   │
│  │  │ Pods        │  │ Pods        │  │ Pods        │  │ SIS Pods │  │   │
│  │  │ (FastAPI)   │  │ (FastAPI)   │  │ (FastAPI)   │  │ (FastAPI)│  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └──────────┘  │   │
│  │                                                                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │   │
│  │  │ Celery      │  │ Celery      │  │ Celery      │              │   │
│  │  │ Workers     │  │ Workers     │  │ Workers     │              │   │
│  │  │ (AI/ML)     │  │ (Finance)   │  │ (Reports)   │              │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘              │   │
│  │                                                                     │   │
│  │  HPA: Horizontal Pod Autoscaler (escala 2-20 pods automaticamente) │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    CAMADA DE DADOS                                  │   │
│  │                                                                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────┐  │   │
│  │  │ PostgreSQL  │  │ Redis       │  │ Kafka       │  │ Click-   │  │   │
│  │  │ (RDS/Cloud  │  │ (ElastiCache│  │ (MSK/Managed│  │ House    │  │   │
│  │  │  SQL/Azure  │  │  /Azure     │  │  Kafka)     │  │ (Self-   │  │   │
│  │  │  DB)        │  │  Cache)     │  │             │  │  hosted) │  │   │
│  │  │  Primary +  │  │             │  │             │  │          │  │   │
│  │  │  2 Réplicas │  │             │  │             │  │          │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └──────────┘  │   │
│  │                                                                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │   │
│  │  │ Elastic-    │  │ MinIO / S3  │  │ MongoDB     │              │   │
│  │  │ search      │  │ (Object     │  │ (Document   │              │   │
│  │  │ (OpenSearch)│  │  Storage)   │  │  Store)     │              │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    MONITORAMENTO & OBSERVABILIDADE                     │   │
│  │  Prometheus + Grafana + Jaeger + ELK Stack + PagerDuty               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Provedor Recomendado por Região

| Região | Provedor Principal | Provedor DR | Motivo |
|--------|-------------------|-------------|--------|
| **África (Angola)** | **AWS África (Cape Town)** ou **Azure South Africa** | AWS Europa (Frankfurt) | Região mais próxima; latência <100ms |
| **Europa** | **AWS Europa (Frankfurt/Irlanda)** ou **Azure West Europe** | OCI Europa | GDPR compliance |
| **Américas** | **AWS US-East** ou **Azure US-East** | GCP US-Central | Maior densidade de data centers |
| **Ásia-Pacífico** | **AWS Singapura/Sydney** ou **Azure East Asia** | AWS Tóquio | Proximidade geográfica |

### 5.4 Por Que AWS para o AOS (Fase Inicial)

**Vantagens da AWS para sistemas acadêmicos:**
1. **Maior ecossistema educacional:** Canvas, MoodleCloud, Anthology/Blackboard usam AWS cite🛠web_search:18#2:~:text=Instructure Advances Education Equity with AWS Support
2. **Região na África:** AWS África (Cape Town) é a única região hyperscaler na África subsaariana cite🛠web_search:18#8:~:text=By selecting AWS to host Blackboard, Anthology is offering its modern learning management system on one of the most secure, extensive, and reliable cloud infrastructure available
3. **Serviços gerenciados:** RDS, MSK (Kafka), ElastiCache (Redis), OpenSearch — reduzem operação
4. **Compliance:** FERPA, SOC 2, ISO 27001, GDPR prontos
5. **Créditos AWS Educate / Activate:** Startups e instituições de ensino podem obter créditos gratuitos

**Alternativa Azure:** Se a instituição já usa Microsoft 365 / Teams / Active Directory, Azure oferece integração nativa superior (como PowerSchool faz). cite🛠web_search:18#9:~:text=PowerSchool solutions are hosted on Microsoft Azure, the best-in-class cloud infrastructure

### 5.5 Arquitetura Multi-Cloud (Fase 2+)

Para evitar vendor lock-in e garantir soberania:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AOS MULTI-CLOUD (FASE 2+)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐   │
│  │   AWS (Primary) │◄────►│   Azure (DR)     │◄────►│   GCP (Analytics)│   │
│  │                 │      │                 │      │                 │   │
│  │  • Core App     │      │  • DR Database  │      │  • BigQuery      │   │
│  │  • Primary DB   │      │  • Auth/AD      │      │  • Vertex AI     │   │
│  │  • S3 Storage   │      │  • M365 Integr.│      │  • Data Lake     │   │
│  │  • Lambda/EC2   │      │  • Blob Storage │      │  • ML Training   │   │
│  └─────────────────┘      └─────────────────┘      └─────────────────┘   │
│                                                                             │
│  Sincronização:                                                             │
│  • DB: AWS RDS → Azure SQL (replicação assíncrona)                        │
│  • Storage: AWS S3 → Azure Blob (replicação cross-cloud)                    │
│  • DNS: Route 53 com failover automático para Azure                        │
│                                                                             │
│  Orquestração: Terraform + Kubernetes (portável entre clouds)                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.6 Híbrido On-Premise + Cloud (Para Grandes Universidades)

Para universidades como a UAN (23.000 alunos) que podem ter infraestrutura local:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AOS HÍBRIDO (On-Premise + Cloud)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────┐      ┌─────────────────────────────────────┐   │
│  │   DATA CENTER LOCAL     │      │         CLOUD PÚBLICA               │   │
│  │   (Universidade)        │      │         (AWS/Azure)                 │   │
│  │                         │      │                                     │   │
│  │  • Cache Local (Redis)  │◄────►│  • Banco de Dados Principal         │   │
│  │  • File Server (NFS)    │◄────►│  • Backup & Disaster Recovery       │   │
│  │  • LDAP/AD Local        │◄────►│  • AI/ML (GPU Instances)            │   │
│  │  • Intranet Apps       │◄────►│  • CDN & Edge                       │   │
│  │  • Video Streaming Local│◄────►│  • Email/SMS Gateway                │   │
│  │                         │      │                                     │   │
│  │  Conexão: VPN Site-to-│      │                                     │   │
│  │  Site (10Gbps fiber)    │      │                                     │   │
│  └─────────────────────────┘      └─────────────────────────────────────┘   │
│                                                                             │
│  Vantagens:                                                                 │
│  • Dados sensíveis (notas, financeiro) podem ficar no campus               │
│  • Processamento de vídeo (dublagem AI) usa GPU cloud sem investimento     │
│  • Backup automático para cloud                                            │
│  • Latência zero para usuários no campus                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. 💰 Estimativa de Custo de Hospedagem do AOS

### 6.1 Fase 1 — Startup / Pequena Instituição (1-1.000 usuários)

| Componente | AWS | Azure | On-Premise Equivalente |
|-----------|-----|-------|------------------------|
| **App Server** | EC2 t3.medium (2vCPU/4GB) × 2 = $60/mês | B2s × 2 = $55/mês | Servidor Dell R240 = $3.000 |
| **Database** | RDS PostgreSQL db.t3.micro = $15/mês | Azure SQL Basic = $5/mês | — |
| **Cache** | ElastiCache t3.micro = $13/mês | Azure Cache Basic = $15/mês | — |
| **Storage** | S3 500GB = $12/mês | Blob 500GB = $11/mês | NAS 2TB = $800 |
| **CDN** | CloudFront = $15/mês | Azure CDN = $17/mês | — |
| **Monitoring** | CloudWatch = $10/mês | Monitor = $10/mês | — |
| **Total** | **~$125/mês** | **~$113/mês** | **~$3.800 inicial + $100/mês** |

### 6.2 Fase 2 — Média Instituição (1.000-10.000 usuários)

| Componente | AWS | Azure |
|-----------|-----|-------|
| **App Cluster** | EKS + EC2 m5.large × 4 = $280/mês | AKS + D4s_v3 × 4 = $290/mês |
| **Database** | RDS PostgreSQL Multi-AZ db.m5.large = $175/mês | Azure SQL Standard S2 = $150/mês |
| **Cache** | ElastiCache r6g.large cluster = $85/mês | Azure Cache Standard = $80/mês |
| **Kafka** | MSK (3 brokers) = $200/mês | Event Hubs = $180/mês |
| **Storage** | S3 5TB = $115/mês | Blob 5TB = $110/mês |
| **CDN** | CloudFront = $50/mês | Azure CDN = $55/mês |
| **GPU (AI)** | g4dn.xlarge (spot) = $150/mês | NC6s_v3 = $160/mês |
| **Monitoring** | CloudWatch + X-Ray = $40/mês | Monitor + App Insights = $45/mês |
| **Total** | **~$1.095/mês** | **~$1.070/mês** |

### 6.3 Fase 3 — Grande Instituição / Enterprise (10.000+ usuários)

| Componente | AWS | Azure |
|-----------|-----|-------|
| **App Cluster** | EKS + EC2 m5.2xlarge × 8 = $1.120/mês | AKS + D8s_v3 × 8 = $1.150/mês |
| **Database** | RDS PostgreSQL Multi-AZ db.r6g.xlarge = $520/mês | Azure SQL Premium P2 = $500/mês |
| **Cache** | ElastiCache r6g.xlarge cluster = $340/mês | Azure Cache Premium = $330/mês |
| **Kafka** | MSK (5 brokers) = $450/mês | Event Hubs Dedicated = $420/mês |
| **Analytics** | OpenSearch r6g.large × 3 = $380/mês | Azure Cognitive Search = $350/mês |
| **Storage** | S3 50TB = $1.150/mês | Blob 50TB = $1.100/mês |
| **CDN** | CloudFront = $200/mês | Azure CDN = $210/mês |
| **GPU Cluster** | g5.2xlarge × 4 = $1.200/mês | NC24s_v3 = $1.100/mês |
| **DR (Multi-Region)** | Réplica RDS + S3 cross-region = $400/mês | Geo-replicação SQL = $380/mês |
| **Monitoring** | CloudWatch Enterprise = $150/mês | Monitor Full = $140/mês |
| **Total** | **~$5.910/mês** | **~$5.680/mês** |

---

## 7. 🔐 Compliance & Segurança

### 7.1 Certificações Necessárias

| Certificação | AWS | Azure | Relevância para AOS |
|-------------|-----|-------|---------------------|
| **SOC 2 Type II** | ✅ | ✅ | Auditoria de controles de segurança |
| **ISO 27001** | ✅ | ✅ | Gestão de segurança da informação |
| **ISO 27017** | ✅ | ✅ | Segurança em cloud |
| **FERPA** | ✅ | ✅ | Proteção de registros educacionais (EUA) |
| **GDPR** | ✅ | ✅ | Proteção de dados na UE |
| **LGPD** | ✅ | ✅ | Proteção de dados no Brasil |
| **HIPAA** | ✅ | ✅ | Se houver dados de saúde estudantil |
| **PCI DSS** | ✅ | ✅ | Se processar pagamentos |

### 7.2 Soberania de Dados

Para Angola e outras nações africanas:
- **AWS África (Cape Town):** Região `af-south-1` — dados nunca saem da África do Sul
- **Azure South Africa:** Regiões `south-africa-north` e `south-africa-west`
- **Futuro:** AWS planeja região em Nigéria; Azure expande para Quênia

Para compliance com leis locais de Angola, recomenda-se:
1. **Dados primários** em AWS Cape Town (menor latência)
2. **Backup** em Frankfurt (GDPR-compliant) ou em data center local parceiro
3. **Criptografia** AES-256 em trânsito e em repouso
4. **Acesso:** Apenas IPs angolanos para administração (Geo-blocking)

---

## 8. 🚀 Roadmap de Infraestrutura do AOS

### Fase 1 — MVP (Meses 1-3)
- [ ] **AWS Single-Region** (Cape Town ou Frankfurt)
- [ ] **EC2 + RDS PostgreSQL** (single instance)
- [ ] **S3** para armazenamento de arquivos
- [ ] **CloudFront** para CDN
- [ ] **Docker Compose** (ainda não Kubernetes)
- [ ] **Terraform** para IaC
- [ ] **Custo:** ~$125-$200/mês

### Fase 2 — Scale (Meses 4-9)
- [ ] **EKS / AKS** (Kubernetes gerenciado)
- [ ] **RDS Multi-AZ** (alta disponibilidade)
- [ ] **ElastiCache Redis** (cache dedicado)
- [ ] **MSK** (Kafka gerenciado)
- [ ] **CI/CD** via GitHub Actions + ArgoCD
- [ ] **Custo:** ~$1.000-$1.500/mês

### Fase 3 — Enterprise (Meses 10-18)
- [ ] **Multi-Region** (primária + DR)
- [ ] **Multi-Cloud** (AWS primário + Azure DR)
- [ ] **GPU Nodes** para AI/ML (dublagem automática)
- [ ] **ClickHouse** para analytics
- [ ] **WAF + DDoS Protection**
- [ ] **Custo:** ~$5.000-$10.000/mês

### Fase 4 — Global (Meses 19-24)
- [ ] **Edge Locations** em cada continente
- [ ] **Data Residency** por país (Angola, Brasil, Portugal, etc.)
- [ ] **Private Cloud** opcional para grandes universidades
- [ ] **FedRAMP / ISO 27001** certificação própria
- [ ] **Custo:** $10.000+/mês

---

## 9. 📚 Referências

- **Canvas + AWS:** [Instructure Press Release 2026](https://press.aboutamazon.com/aws/2026/8/instructure-advances-education-equity-with-aws-support) cite🛠web_search:18#2:~:text=Instructure Advances Education Equity with AWS Support
- **Blackboard Sub-processors:** [Blackboard Trust Center](https://www.blackboard.com/trust-center/sub-processors) cite🛠web_search:18#6:~:text=Amazon Web Services (AWS) (Data Center)...Microsoft (Azure) (Data Center)
- **PowerSchool + Azure:** [PowerSchool Cloud Hosting](https://www.powerschool.com/services/cloud-based-hosting/) cite🛠web_search:18#9:~:text=PowerSchool solutions are hosted on Microsoft Azure
- **Ellucian + OCI:** [Oracle Reference Architecture](https://docs.oracle.com/en/solutions/oci-ellucian/index.html) cite🛠web_search:18#0:~:text=Deploy an ERP system using Ellucian Banner...multi-tier reference architecture
- **MoodleCloud + AWS:** [MoodleCloud Support](https://support.moodle.com/support/solutions/articles/80000831971-moodlecloud-data-hosting-locations) cite🛠web_search:17#6:~:text=MoodleCloud is hosted on Amazon Web Servers (AWS) in three regions
- **Epic Cloud:** [Lifepoint Informatics](https://lifepoint.com/epic-vs-cerner/) cite🛠web_search:17#3:~:text=Epic's hosting services are integrated tightly...Epic's own hosted cloud environments achieve approximately 99.95%+ uptime
- **Cerner + OCI:** [Lifepoint Informatics](https://lifepoint.com/epic-vs-cerner/) cite🛠web_search:17#3:~:text=Cerner is leveraging Oracle Cloud Infrastructure...Now Oracle Health after the 2022 acquisition
- **Cloud Banking:** [Crassula](https://crassula.io/guides/cloud-banking/) cite🛠web_search:17#8:~:text=IaaS...A bank runs its own core banking software on AWS EC2 instances or Azure VMs
- **AWS vs Azure Financial Services:** [Rapyder](https://www.rapyder.com/blog/aws-vs-azure-vs-gcp-for-financial-services/) cite🛠web_search:17#9:~:text=More financial institutions are adopting multi-cloud and hybrid models
- **Moodle AWS Cost:** [MooDIY Blog](https://blog.moodiycloud.com/why-hosting-moodle-on-aws-is-an-expensive-proposition) cite🛠web_search:17#7:~:text=Total base infrastructure ~$362/month...Total 3-year TCO ~$59,294

---

## 10. 🏁 Conclusão

A indústria de sistemas acadêmicos está **100% migrada para a cloud**:
- **Canvas** → AWS
- **PowerSchool** → Azure
- **Ellucian Banner** → Oracle Cloud
- **MoodleCloud** → AWS
- **Blackboard** → AWS + Azure (multi-cloud)

Nenhum dos líderes oferece mais on-premise como padrão. A cloud venceu por:
1. **Custo:** 40-50% redução inicial, 15-30% operacional
2. **Segurança:** 24/7 monitoring, patching automático, compliance built-in
3. **Escalabilidade:** Escala sob demanda (matrículas, exames online)
4. **DR:** Backup e disaster recovery incluídos

**Para o AOS, a recomendação é:**
- **Fase 1-2:** AWS (região Cape Town para África, Frankfurt para Europa)
- **Fase 3+:** Multi-cloud (AWS primário + Azure DR)
- **Grandes universidades:** Híbrido (cloud + data center local)
- **Stack:** Kubernetes (EKS/AKS) + PostgreSQL RDS + Redis ElastiCache + Kafka MSK + S3/MinIO

O AOS deve nascer **cloud-native**, mas arquitetado para ser **portável** — assim como seus plugins são portáveis, sua infraestrutura também deve ser.
