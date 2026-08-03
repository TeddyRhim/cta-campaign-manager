"use client";

import { useCampaigns } from "@/hooks/useCampaigns";
import CampaignTable from "@/components/campaign/CampaignTable";
import Card from "@/components/ui/Card";
import Loader from "@/components/ui/Loader";
import EmptyState from "@/components/ui/EmptyState";


export default function CampaignsPage() {

    const { campaigns, loading, error } = useCampaigns();

    if (loading) {
        return <Loader />;
    }

    if (error) {
        return <EmptyState message={error} />;
    }

    return (
        <main className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Campaigns</h1>
                <p className="text-gray-500">Gestion des campagnes</p>
            </div>

            {campaigns.length ? (
                <CampaignTable campaigns={campaigns} />
            ) : (
                <EmptyState message="Aucune campagne disponible" />
            )}
        </main>
    );
}