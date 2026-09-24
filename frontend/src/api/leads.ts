import type { LeadAccepted, LeadSubmission } from "../types/lead";

const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim();
const API_BASE_URL = (configuredBaseUrl || "").replace(/\/$/, "");

export class LeadApiError extends Error {
  constructor(message: string, public readonly status?: number) {
    super(message);
    this.name = "LeadApiError";
  }
}

export function createIdempotencyKey(): string {
  if (typeof crypto.randomUUID === "function") return crypto.randomUUID();
  const bytes = crypto.getRandomValues(new Uint8Array(16));
  return `lead-${Array.from(bytes, (byte) => byte.toString(16).padStart(2, "0")).join("")}`;
}

export async function submitLead(lead: LeadSubmission, idempotencyKey: string): Promise<LeadAccepted> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/api/v1/leads`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Idempotency-Key": idempotencyKey },
      body: JSON.stringify(lead),
    });
  } catch {
    throw new LeadApiError("We could not connect right now. Check your connection and try again.");
  }

  const body = await response.json().catch(() => null) as LeadAccepted | { detail?: string | Array<{ msg?: string }> } | null;
  if (!response.ok) {
    const detail = body && "detail" in body ? body.detail : undefined;
    const message = typeof detail === "string" ? detail : Array.isArray(detail) && detail[0]?.msg ? detail[0].msg : "We could not submit your enquiry. Please review the details and try again.";
    throw new LeadApiError(message, response.status);
  }
  if (!body || !("success" in body) || body.success !== true) {
    throw new LeadApiError("The server returned an unexpected response. Please try again.");
  }
  return body;
}
