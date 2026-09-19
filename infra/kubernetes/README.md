# Kubernetes (produção)

Manifests/Helm chart a criar na fase de produção. Referência: `AOS_Infraestrutura_Hospedagem.md`.
Componentes: `core` Deployment (HPA), `workers` (Celery), Postgres (operator), Redis, Kafka (Strimzi), Ingress + cert-manager.
