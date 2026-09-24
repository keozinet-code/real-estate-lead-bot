import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { LeadForm } from "./LeadForm";

afterEach(() => vi.restoreAllMocks());
describe("LeadForm", () => {
  it("submits the required message and reports success", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({ success: true, lead_id: "12345678-abcd", status: "qualified", message: "Received", lead_score: 65, lead_category: "WARM", duplicate: false }), { status: 201 }));
    const onSuccess = vi.fn();
    render(<LeadForm onSuccess={onSuccess} />);
    fireEvent.change(screen.getByLabelText(/Describe your request/i), { target: { value: "I want to rent a 2-bedroom flat in Ikeja." } });
    fireEvent.click(screen.getByRole("button", { name: /Send my enquiry/i }));
    await waitFor(() => expect(onSuccess).toHaveBeenCalledOnce());
  });
  it("keeps entered data visible and announces request failures", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockRejectedValue(new TypeError("offline"));
    render(<LeadForm onSuccess={vi.fn()} />);
    fireEvent.change(screen.getByLabelText(/Describe your request/i), { target: { value: "I need land." } });
    fireEvent.click(screen.getByRole("button", { name: /Send my enquiry/i }));
    expect(await screen.findByRole("alert")).toHaveTextContent(/could not connect/i);
    expect(screen.getByLabelText(/Describe your request/i)).toHaveValue("I need land.");
    fireEvent.click(screen.getByRole("button", { name: /Send my enquiry/i }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const firstHeaders = (fetchMock.mock.calls[0][1] as RequestInit).headers;
    const retryHeaders = (fetchMock.mock.calls[1][1] as RequestInit).headers;
    expect(retryHeaders).toEqual(firstHeaders);
  });
});
