# Opsyra — Observability & Incident Intelligence

Opsyra ingests telemetry from distributed services, flags incidents, tracks service
health, and produces root-cause analysis with suggested remediation.

**Status: working prototype.** The pipeline runs end to end locally through Docker
Compose. The sections below separate what is implemented today from what is planned,
so the two are never confused.

## What runs today

| Service | Port | Responsibility |
|---|---|---|
| `ingestion-service` | 8001 | Accepts telemetry (logs, metrics, traces) and publishes it to a Redis stream |
| `processing-service` | 8002 | Consumes the stream, flags incidents, maintains service health snapshots |
| `query-service` | 8003 | Read APIs for incidents and service health |
| `ai-rca-service` | 8004 | Root-cause analysis for a given incident |
| `dashboard` | 3000 | Next.js operator UI |

Shared code lives in `shared/opsyra_common`: configuration, database, models,
repository, Redis queue helpers, auth and the RCA provider.

Each FastAPI service exposes versioned REST endpoints under `/api/v1`, a `/healthz`
check, and live Swagger UI at `/docs`. Endpoint details are in
[`docs/api/backend-apis.md`](docs/api/backend-apis.md).

### Incident detection

Detection is **rule-based today**: severity thresholds plus message heuristics
(timeouts, failures, latency patterns). It is deliberately simple and deterministic,
which makes it easy to test. Model-based detection is on the roadmap below.

### Root-cause analysis

`ai-rca-service` calls an OpenAI-compatible Responses API when `OPENAI_API_KEY` is set.
Without a key it falls back to a deterministic rule-based analysis, so the service still
works offline and a demo never depends on a paid API being reachable.

## Stack

- **Backend** — Python, FastAPI, SQLAlchemy, Pydantic Settings
- **Streaming** — Redis Streams
- **Database** — PostgreSQL via psycopg; SQLite by default for local runs
- **Frontend** — Next.js, React, TypeScript
- **Infrastructure** — Docker Compose, a Prometheus scrape config, a local Kubernetes manifest
- **CI** — GitHub Actions, running each service's test suite on every push and pull request

## Running locally

```bash
cp .env.example .env
docker compose up --build
```

- Dashboard — http://localhost:3000
- Swagger per service — http://localhost:8001/docs through http://localhost:8004/docs
- Prometheus — http://localhost:9090

## Tests

```bash
pip install -r requirements.txt
pytest apps/ingestion-service/tests
```

Run one service's suite at a time. All four are named `test_api.py`, so a single
root-level `pytest` cannot collect them together yet.

## Repository layout

```
apps/       the four FastAPI services and the Next.js dashboard
shared/     opsyra_common, imported by every service
infra/      docker, prometheus config, a local kubernetes manifest
docs/       API documentation and project structure notes
```

## Roadmap

Design intentions, **not** current capabilities:

- Kafka in place of Redis Streams, for ingestion at higher throughput
- ClickHouse for time-series storage and OpenSearch for log search
- Grafana dashboards on top of the existing Prometheus configuration
- Terraform definitions and a deployable Kubernetes setup — `infra/terraform` and
  `scripts/` are empty placeholders today
- Model-based anomaly detection, replacing the current rule-based pass
