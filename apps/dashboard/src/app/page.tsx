import { IncidentRca } from "@/components/incident-rca";

type Incident = {
  incident_id: string;
  service_name: string;
  severity: "low" | "medium" | "high" | "critical";
  status: "open" | "investigating" | "resolved";
  title: string;
};

type IncidentResponse = {
  incidents: Incident[];
  total: number;
};

type ServiceOverview = {
  service_name: string;
  health: "healthy" | "degraded" | "down";
  open_incidents: number;
  p95_latency_ms: number;
  error_rate_percent: number;
};

type ServiceOverviewResponse = {
  services: ServiceOverview[];
  generated_from: string;
};

async function fetchJson<T>(url: string): Promise<T | null> {
  try {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as T;
  } catch {
    return null;
  }
}

function healthClass(health: ServiceOverview["health"]) {
  if (health === "down") return "pill bad";
  if (health === "degraded") return "pill warn";
  return "pill good";
}

function severityClass(severity: Incident["severity"]) {
  if (severity === "critical") return "pill bad";
  if (severity === "high" || severity === "medium") return "pill warn";
  return "pill good";
}

export default async function HomePage() {
  const queryBaseUrl =
    process.env.NEXT_PUBLIC_QUERY_SERVICE_URL ?? "http://localhost:8003";
  const aiBaseUrl =
    process.env.NEXT_PUBLIC_AI_RCA_SERVICE_URL ?? "http://localhost:8004";
  const queryInternalUrl =
    process.env.QUERY_SERVICE_INTERNAL_URL ?? queryBaseUrl;

  const [services, incidents] = await Promise.all([
    fetchJson<ServiceOverviewResponse>(
      `${queryInternalUrl}/api/v1/query/services/overview`,
    ),
    fetchJson<IncidentResponse>(`${queryInternalUrl}/api/v1/query/incidents`),
  ]);

  return (
    <main className="page-shell">
      <section className="hero">
        <div className="label">Opsyra Dashboard</div>
        <h1>Observe the blast radius before it becomes the outage.</h1>
        <p>
          A live observability surface for telemetry intake, anomaly processing,
          incident review, and AI-assisted root cause analysis.
        </p>
        <div className="hero-links">
          <a href={`${queryBaseUrl}/docs`}>Query Swagger</a>
          <a href={`${aiBaseUrl}/docs`}>AI RCA Swagger</a>
          <a href="http://localhost:9090">Prometheus</a>
        </div>
      </section>

      <section className="section-grid">
        <div className="stats-grid">
          <article className="card">
            <div className="label">Tracked services</div>
            <div className="stat-value">{services?.services.length ?? 0}</div>
          </article>
          <article className="card">
            <div className="label">Open incidents</div>
            <div className="stat-value">{incidents?.total ?? 0}</div>
          </article>
          <article className="card">
            <div className="label">Primary data source</div>
            <div className="stat-value" style={{ fontSize: "1.25rem" }}>
              {services?.generated_from ?? "unavailable"}
            </div>
          </article>
        </div>

        <article className="card">
          <h2>Service health</h2>
          <div className="service-grid">
            {services?.services.length ? (
              services.services.map((service) => (
                <div className="service-row" key={service.service_name}>
                  <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                    <strong>{service.service_name}</strong>
                    <span className={healthClass(service.health)}>{service.health}</span>
                  </div>
                  <div className="service-meta">
                    <span>{service.open_incidents} open incidents</span>
                    <span>{service.p95_latency_ms}ms p95 latency</span>
                    <span>{service.error_rate_percent.toFixed(1)}% error rate</span>
                  </div>
                </div>
              ))
            ) : (
              <div className="empty">
                No service snapshots yet. Send telemetry into the ingestion API to populate the
                dashboard.
              </div>
            )}
          </div>
        </article>

        <article className="card">
          <h2>Incident feed</h2>
          <div className="incident-grid">
            {incidents?.incidents.length ? (
              incidents.incidents.map((incident) => (
                <div className="incident-row" key={incident.incident_id}>
                  <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                    <strong>{incident.title}</strong>
                    <span className={severityClass(incident.severity)}>{incident.severity}</span>
                  </div>
                  <div className="incident-meta">
                    <span>{incident.service_name}</span>
                    <span>{incident.status}</span>
                    <span>{incident.incident_id}</span>
                  </div>
                  <IncidentRca incidentId={incident.incident_id} />
                </div>
              ))
            ) : (
              <div className="empty">
                No incidents yet. A warning, error, or critical telemetry message will create one.
              </div>
            )}
          </div>
        </article>
      </section>
    </main>
  );
}
