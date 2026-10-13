"use client";

import { getCampaigns } from "@/services/campaign.service";
import { usePaginatedList } from "./usePaginatedList";


export function useCampaigns() {
    const list = usePaginatedList(getCampaigns, "Impossible de charger les campagnes");

    return { ...list, campaigns: list.items };
}
