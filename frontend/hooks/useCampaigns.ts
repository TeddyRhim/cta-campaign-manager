"use client";

import { useEffect, useState } from "react";
import { Campaign } from "@/types/campaign";
import { getCampaigns } from "@/services/campaign.service";


export function useCampaigns() {

    const [campaigns, setCampaigns] = useState<Campaign[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    useEffect(() => {

        async function fetchCampaigns() {

            try {

                const data = await getCampaigns();

                setCampaigns(data);

            } catch(error) {

                console.error(
                    "Erreur chargement campaigns :",
                    error
                );
                setError(
                    "Impossible de charger les campagnes"
                );

            } finally {

                setLoading(false);

            }

        }


        fetchCampaigns();

    }, []);


    return {
        campaigns,
        loading,
        error
    };
}