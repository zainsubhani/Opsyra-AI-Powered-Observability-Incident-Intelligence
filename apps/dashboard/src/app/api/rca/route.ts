import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  const payload = await request.json();
  const baseUrl =
    process.env.AI_RCA_SERVICE_INTERNAL_URL ?? "http://localhost:8004";
  const apiKey = process.env.API_KEY ?? "";

  const response = await fetch(`${baseUrl}/api/v1/rca/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": apiKey,
    },
    body: JSON.stringify(payload),
    cache: "no-store",
  });

  const data = await response.json();
  return NextResponse.json(data, { status: response.status });
}
