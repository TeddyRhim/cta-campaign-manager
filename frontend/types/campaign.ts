import { Contact } from "@/types/contact";

export type CampaignStatus =
    | "DRAFT"
    | "ACTIVE"
    | "PAUSED"
    | "FINISHED";

export interface Campaign {
    id: number;
    title: string;
    description: string | null;
    contacts: Contact[];
    status: CampaignStatus;
    created_by: number;
    created_at: string;
}