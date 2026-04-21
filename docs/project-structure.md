# Project Structure

This repository is organized as a multi-app workspace with a frontend dashboard and multiple backend services.

## Applications

- `apps/dashboard`: Next.js frontend for observability dashboards, incidents, and AI insights
- `apps/ingestion-service`: Handles incoming logs, metrics, and traces
- `apps/processing-service`: Processes events, enriches telemetry, and runs anomaly detection pipelines
- `apps/query-service`: Serves dashboard queries, search, and analytics APIs
- `apps/ai-rca-service`: Generates AI-based root cause analysis and remediation guidance

## Frontend Structure

- `src/app`: App Router pages and layouts
- `src/components`: Shared UI components
- `src/features`: Feature modules such as alerts, incidents, and services
- `src/hooks`: Reusable React hooks
- `src/lib`: Utilities, API clients, and shared helpers
- `src/styles`: Global styling and design tokens
- `src/types`: Shared TypeScript types
- `public`: Static assets

## Backend Service Structure

Each backend service follows the same internal layout:

- `app/api/v1`: API routes
- `app/core`: Configuration, settings, and shared internals
- `app/models`: Database models
- `app/schemas`: Request and response schemas
- `app/services`: Business logic
- `app/workers`: Background jobs, Kafka consumers, and async processing
- `tests`: Service tests

## Supporting Folders

- `docs/architecture`: Architecture decisions and system diagrams
- `docs/api`: API contracts and endpoint notes
- `docs/runbooks`: Incident handling and operational guides
- `infra/docker`: Dockerfiles and local container setup
- `infra/kubernetes`: Kubernetes manifests and Helm-related assets
- `infra/monitoring`: Prometheus, Grafana, and observability configs
- `infra/terraform`: Cloud infrastructure as code
- `scripts/dev`: Local development scripts
- `scripts/setup`: Bootstrap and environment setup scripts
- `scripts/deploy`: Deployment automation
