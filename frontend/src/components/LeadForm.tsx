import { FormEvent, useRef, useState } from "react";
import { createIdempotencyKey, submitLead } from "../api/leads";
import type { LeadAccepted, LeadIntent, LeadSubmission } from "../types/lead";

interface Props { onSuccess: (result: LeadAccepted) => void; }
interface FormFields {
  name: string; email: string; phone: string; message: string;
  property_type: string; location: string; bedrooms: string;
  budget: string; intent: LeadIntent | ""; timeline: string;
}
const initialFields: FormFields = { name: "", email: "", phone: "", message: "", property_type: "", location: "", bedrooms: "", budget: "", intent: "", timeline: "" };
const optional = (value: string) => value.trim() || undefined;
function toSubmission(fields: FormFields): LeadSubmission {
  return {
    name: optional(fields.name), email: optional(fields.email), phone: optional(fields.phone),
    message: fields.message.trim(), property_type: optional(fields.property_type),
    location: optional(fields.location), bedrooms: fields.bedrooms ? Number(fields.bedrooms) : undefined,
    budget: fields.budget ? Number(fields.budget) : undefined,
    intent: fields.intent || undefined, timeline: optional(fields.timeline),
  };
}

export function LeadForm({ onSuccess }: Props) {
  const [fields, setFields] = useState(initialFields);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const idempotencyKey = useRef(createIdempotencyKey());
  const updateField = (name: keyof FormFields, value: string) => setFields((current) => ({ ...current, [name]: value }));

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      const result = await submitLead(toSubmission(fields), idempotencyKey.current);
      idempotencyKey.current = createIdempotencyKey();
      setFields(initialFields);
      onSuccess(result);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Something went wrong. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form className="lead-form" onSubmit={handleSubmit} aria-describedby={error ? "form-error" : undefined}>
      <div className="form-heading">
        <p className="eyebrow">Property enquiry</p><h2>Tell us what you’re looking for.</h2>
        <p>Share as much as you know. Only your enquiry is required.</p>
      </div>
      <fieldset>
        <legend>Your contact details</legend>
        <div className="field-grid field-grid-three">
          <label>Name<input name="name" autoComplete="name" maxLength={255} value={fields.name} onChange={(e) => updateField("name", e.target.value)} /></label>
          <label>Email<input name="email" type="email" autoComplete="email" value={fields.email} onChange={(e) => updateField("email", e.target.value)} /></label>
          <label>Phone<input name="phone" type="tel" autoComplete="tel" maxLength={50} value={fields.phone} onChange={(e) => updateField("phone", e.target.value)} /></label>
        </div>
      </fieldset>
      <fieldset>
        <legend>Property preferences</legend>
        <div className="field-grid">
          <label>Intent<select name="intent" value={fields.intent} onChange={(e) => updateField("intent", e.target.value)}><option value="">Select one</option><option value="buy">Buy</option><option value="rent">Rent</option><option value="sell">Sell</option><option value="land">Land</option></select></label>
          <label>Property type<input name="property_type" placeholder="e.g. apartment" maxLength={100} value={fields.property_type} onChange={(e) => updateField("property_type", e.target.value)} /></label>
          <label>Preferred location<input name="location" placeholder="e.g. Lekki, Lagos" maxLength={255} value={fields.location} onChange={(e) => updateField("location", e.target.value)} /></label>
          <label>Bedrooms<input name="bedrooms" type="number" min="1" step="1" inputMode="numeric" value={fields.bedrooms} onChange={(e) => updateField("bedrooms", e.target.value)} /></label>
          <label>Budget (₦)<input name="budget" type="number" min="0" step="1" inputMode="numeric" placeholder="80000000" value={fields.budget} onChange={(e) => updateField("budget", e.target.value)} /></label>
          <label>Timeline<input name="timeline" placeholder="e.g. within 3 months" maxLength={100} value={fields.timeline} onChange={(e) => updateField("timeline", e.target.value)} /></label>
        </div>
      </fieldset>
      <label className="message-field">Describe your request <span aria-hidden="true">*</span>
        <textarea name="message" required maxLength={5000} rows={5} placeholder="I want to buy a 3-bedroom apartment in Lekki within 3 months…" value={fields.message} onChange={(e) => updateField("message", e.target.value)} />
        <small>{fields.message.length.toLocaleString()} / 5,000</small>
      </label>
      {error && <div id="form-error" className="error-banner" role="alert">{error}</div>}
      <button className="primary-button" type="submit" disabled={isSubmitting}>
        {isSubmitting ? <><span className="spinner" aria-hidden="true" /> Sending enquiry…</> : "Send my enquiry"}
      </button>
      <p className="privacy-note">By submitting, you agree that a property adviser may contact you about this enquiry.</p>
    </form>
  );
}
