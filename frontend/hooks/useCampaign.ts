"use client";

import { useEffect, useState } from "react";
import { Campaign } from "@/types/campaign";
import { getCampaignById } from "@/services/campaign.service";


export function useCampaign(
    id: number
) {

    const [campaign, setCampaign] = useState<Campaign | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    useEffect(() => {

        async function fetchCampaign() {

            try {

                const data = await getCampaignById(id);

                setCampaign(data);

            } catch(error) {

                console.error(error);

                setError(
                    "Impossible de charger la campagne"
                );

            } finally {

                setLoading(false);

            }

        }


        fetchCampaign();

    }, [id]);


    return {
        campaign,
        loading,
        error
    };
}