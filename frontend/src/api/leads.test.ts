import { afterEach, describe, expect, it, vi } from "vitest";
import { LeadApiError, submitLead } from "./leads";

afterEach(() => vi.restoreAllMocks());
describe("submitLead", () => {
  it("sends the stable idempotency key and returns a lead", async () => {
    const result = { success: true, lead_id: "12345678-abcd", status: "qualified", message: "Received", lead_score: 100, lead_category: "HOT", duplicate: false } as const;
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify(result), { status: 201, headers: { "Content-Type": "application/json" } }));
    await expect(submitLead({ message: "3-bedroom in Lekki" }, "fixed-key-123")).resolves.toEqual(result);
    expect(fetchMock).toHaveBeenCalledWith("/api/v1/leads", expect.objectContaining({ headers: expect.objectContaining({ "Idempotency-Key": "fixed-key-123" }) }));
  });
  it("surfaces a safe API error", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({ detail: "Workflow temporarily unavailable" }), { status: 503 }));
    await expect(submitLead({ message: "Land in Ibadan" }, "fixed-key-456")).rejects.toEqual(expect.objectContaining<Partial<LeadApiError>>({ message: "Workflow temporarily unavailable", status: 503 }));
  });
});
