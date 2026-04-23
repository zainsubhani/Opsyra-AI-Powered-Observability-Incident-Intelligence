# Opsyra AI-Powered Observability

## Overview

Opsyra is an AI-powered observability and incident intelligence platform designed to help engineering teams detect production issues faster, understand their likely causes, and respond with clearer operational context.

The platform is intended to ingest logs, metrics, and traces from distributed systems, analyze telemetry for anomalies, and surface AI-assisted root cause analysis through operator-friendly APIs and dashboards.

## Core Capabilities

- telemetry ingestion for logs, metrics, and traces
- anomaly detection and signal processing
- incident and service health querying
- AI-assisted root cause analysis and remediation suggestions
- API-first backend services for observability workflows

## Architecture

The repository is structured as a multi-service workspace with dedicated applications for:

- `apps/ingestion-service`
- `apps/processing-service`
- `apps/query-service`
- `apps/ai-rca-service`
- `apps/dashboard`

Supporting documentation and infrastructure live under:

- `docs/`
- `infra/`
- `scripts/`

## Backend APIs

The current backend implementation is built with FastAPI and includes:

- versioned REST endpoints
- typed request and response schemas
- live Swagger UI
- OpenAPI schema generation
- service health endpoints

Detailed API documentation is available in:

- `docs/api/backend-apis.md`

## Technology Direction

The current implementation and project direction align around the following stack:

- Backend: FastAPI
- Frontend: Next.js and TypeScript
- Streaming: Kafka
- Datastores: PostgreSQL and ClickHouse
- Search: OpenSearch or Elasticsearch
- Monitoring: Prometheus and Grafana
- Infrastructure: Docker, Kubernetes, and cloud deployment targets

## Project Goal

The goal of Opsyra is to reduce mean time to detection and investigation by combining observability signals with AI-assisted incident analysis in a single platform-oriented workflow.
