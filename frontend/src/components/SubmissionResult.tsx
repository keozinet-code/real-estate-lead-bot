import type { LeadAccepted } from "../types/lead";

interface Props { result: LeadAccepted; onStartAnother: () => void; }
const categoryCopy = {
  HOT: "A property adviser will prioritise your request.",
  WARM: "A property adviser will review your requirements.",
  COLD: "We have saved your enquiry and will help you refine it.",
} as const;

export function SubmissionResult({ result, onStartAnother }: Props) {
  return (
    <section className="result-card" aria-live="polite" aria-labelledby="result-title">
      <div className="result-icon" aria-hidden="true">✓</div>
      <p className="eyebrow">Enquiry received</p>
      <h2 id="result-title">Thank you — we’ll take it from here.</h2>
      <p>{result.message}</p>
      <div className="result-summary">
        <div><span>Match readiness</span><strong className={`category category-${result.lead_category.toLowerCase()}`}>{result.lead_category}</strong></div>
        <div><span>Reference</span><strong>{result.lead_id.slice(0, 8).toUpperCase()}</strong></div>
      </div>
      <p className="result-note">{result.duplicate ? "This enquiry was already received, so we did not create a duplicate." : categoryCopy[result.lead_category]}</p>
      <button className="secondary-button" type="button" onClick={onStartAnother}>Submit another enquiry</button>
    </section>
  );
}
