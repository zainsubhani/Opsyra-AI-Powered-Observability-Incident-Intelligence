"use client";

import { useState } from "react";

type RCAResponse = {
  incident_id: string;
  provider: string;
  model_name: string;
  probable_cause: string;
  confidence: number;
  remediation_steps: string[];
  executive_summary: string;
};

export function IncidentRca({
  incidentId,
}: {
  incidentId: string;
}) {
  const [data, setData] = useState<RCAResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleGenerate() {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/rca", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ incident_id: incidentId }),
      });
      if (!response.ok) {
        throw new Error(`Request failed with ${response.status}`);
      }
      const payload = (await response.json()) as RCAResponse;
      setData(payload);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "RCA generation failed.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <button className="rca-button" disabled={loading} onClick={handleGenerate}>
        {loading ? "Generating RCA..." : "Generate RCA"}
      </button>
      {error ? <div className="rca-box">{error}</div> : null}
      {data ? (
        <div className="rca-box">
          <div className="label">
            {data.provider} / {data.model_name}
          </div>
          <p>{data.executive_summary}</p>
          <p>
            <strong>Probable cause:</strong> {data.probable_cause}
          </p>
          <p>
            <strong>Confidence:</strong> {(data.confidence * 100).toFixed(0)}%
          </p>
          <ul>
            {data.remediation_steps.map((step) => (
              <li key={step}>{step}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
