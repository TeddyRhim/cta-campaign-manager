export type CampaignStatus =
    | "DRAFT"
    | "ACTIVE"
    | "FINISHED";

export interface Campaign {
    id: number;
    title: string;
    description: string;
    contacts: number[];
    status: CampaignStatus;
    created_by: number;
    created_at: string;
}