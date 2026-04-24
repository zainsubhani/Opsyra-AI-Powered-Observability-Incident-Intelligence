# Backend API Documentation

## Overview

The backend is currently implemented as four FastAPI services:

- `ingestion-service`
- `processing-service`
- `query-service`
- `ai-rca-service`

Each service ships with:

- live Swagger UI at `/docs`
- ReDoc at `/redoc`
- OpenAPI schema at `/openapi.json`
- a basic health endpoint at `/healthz`
- optional API key protection for mutating endpoints using `X-API-Key`

FastAPI already provides Swagger integration automatically, and the services are now configured with clearer tags, route descriptions, and example request bodies to make live API testing easier.

## Service Endpoints

### Ingestion Service

Base app directory:

- `apps/ingestion-service`

Main capabilities:

- accept a single telemetry event
- accept a telemetry batch
- expose ingestion pipeline summary

Endpoints:

- `GET /`
- `GET /healthz`
- `POST /api/v1/telemetry/event`
- `POST /api/v1/telemetry/events`
- `GET /api/v1/telemetry/summary`

### Processing Service

Base app directory:

- `apps/processing-service`

Main capabilities:

- analyze metrics against a baseline
- expose pipeline detector status

Endpoints:

- `GET /`
- `GET /healthz`
- `POST /api/v1/processing/analyze`
- `GET /api/v1/processing/status`

### Query Service

Base app directory:

- `apps/query-service`

Main capabilities:

- return incident summaries
- return service health overview data

Endpoints:

- `GET /`
- `GET /healthz`
- `GET /api/v1/query/incidents`
- `GET /api/v1/query/services/overview`

### AI RCA Service

Base app directory:

- `apps/ai-rca-service`

Main capabilities:

- generate root cause analysis summaries

Endpoints:

- `GET /`
- `GET /healthz`
- `POST /api/v1/rca/generate`

## Running A Service Locally

Install dependencies first:

```bash
python3 -m pip install -r requirements.txt
```

Copy the example environment first if you want the full local stack configuration:

```bash
cp .env.example .env
```

Run each service from its own folder because every service uses the package name `app`:

### Ingestion

```bash
cd apps/ingestion-service
uvicorn app.main:app --reload --port 8001
```

Swagger UI:

- `http://127.0.0.1:8001/docs`

### Processing

```bash
cd apps/processing-service
uvicorn app.main:app --reload --port 8002
```

Swagger UI:

- `http://127.0.0.1:8002/docs`

### Query

```bash
cd apps/query-service
uvicorn app.main:app --reload --port 8003
```

Swagger UI:

- `http://127.0.0.1:8003/docs`

### AI RCA

```bash
cd apps/ai-rca-service
uvicorn app.main:app --reload --port 8004
```

Swagger UI:

- `http://127.0.0.1:8004/docs`

## Live Testing With Swagger

Use the Swagger UI for each service to test endpoints interactively:

1. Start the service locally.
2. Open its `/docs` URL.
3. Expand an endpoint.
4. Click `Try it out`.
5. Use the prefilled example payload.
6. Click `Execute`.
7. Inspect the request, response body, headers, and status code.

If `API_KEY` is set in `.env`, include it in Swagger:

- click `Authorize`
- use the `X-API-Key` value from your environment

## Docker Compose

Bring up the local stack with:

```bash
docker compose up --build
```

This starts:

- PostgreSQL
- Redis
- ingestion service
- processing service
- query service
- AI RCA service
- dashboard
- Prometheus

Primary local URLs:

- Dashboard: `http://localhost:3000`
- Ingestion Swagger: `http://localhost:8001/docs`
- Processing Swagger: `http://localhost:8002/docs`
- Query Swagger: `http://localhost:8003/docs`
- AI RCA Swagger: `http://localhost:8004/docs`
- Prometheus: `http://localhost:9090`

## Example Payloads

### Ingestion Event

```json
{
  "service_name": "checkout-service",
  "signal_type": "log",
  "severity": "error",
  "message": "Database timeout while creating order 42.",
  "timestamp": "2026-04-23T12:30:00Z",
  "environment": "production"
}
```

### Processing Analyze Request

```json
{
  "service_name": "payments-service",
  "metric_name": "p95_latency_ms",
  "current_value": 480,
  "baseline_value": 200,
  "sample_window_minutes": 15
}
```

### AI RCA Request

```json
{
  "incident_id": "inc_1001",
  "service_name": "payments-service",
  "signal_summary": "Latency and error rates increased immediately after a deploy.",
  "suspected_component": "postgres-primary",
  "severity": "critical"
}
```

## Notes

- Swagger is already integrated through FastAPI, so no separate Swagger dependency is required.
- The current API layer uses in-memory sample responses and deterministic logic.
- As we move into full implementation, these endpoints should be connected to shared storage, queues, and real model-backed RCA generation.
