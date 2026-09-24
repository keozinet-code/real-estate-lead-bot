export type LeadIntent = "buy" | "rent" | "sell" | "land";
export type LeadCategory = "HOT" | "WARM" | "COLD";

export interface LeadSubmission {
  name?: string;
  email?: string;
  phone?: string;
  message: string;
  property_type?: string;
  location?: string;
  bedrooms?: number;
  budget?: number;
  intent?: LeadIntent;
  timeline?: string;
}

export interface LeadAccepted {
  success: true;
  lead_id: string;
  status: string;
  message: string;
  lead_score: number;
  lead_category: LeadCategory;
  duplicate: boolean;
}
