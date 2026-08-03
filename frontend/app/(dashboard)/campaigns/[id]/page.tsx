"use client";

import { use } from "react";
import { useCampaign } from "@/hooks/useCampaign";
import StatusBadge from "@/components/campaign/StatusBadge";
import Card from "@/components/ui/Card";
import Loader from "@/components/ui/Loader";
import EmptyState from "@/components/ui/EmptyState";


export default function CampaignDetailPage({
    params
}: {
    params: Promise<{
        id: string
    }>
}) {

    const { id } = use(params);


    const {
        campaign,
        loading,
        error
    } = useCampaign(
        Number(id)
    );


    if (loading) {
        return <Loader />;
    }


    if (error || !campaign) {
        return (
            <EmptyState message={error || "Campagne introuvable"} />
        );
    }


return (
    <main className="space-y-6">
        <div className="flex justify-between items-start">
            <div>
                <h1 className="text-2xl font-bold">
                    {campaign.title}
                </h1>

                <p className="text-gray-500 mt-1">
                    Détails de la campagne
                </p>
            </div>
            <StatusBadge status={campaign.status} />
        </div>

        <section className="bg-white border rounded-xl p-6 shadow-sm space-y-5">
            <div>
                <p className="text-sm text-gray-500">
                    Description
                </p>

                <p className="mt-1">
                    {campaign.description || "Aucune description"}
                </p>
            </div>

            <div className="grid grid-cols-2 gap-6">

                <div>
                    <p className="text-sm text-gray-500">
                        Créée le
                    </p>
                    <p>
                        {new Date(
                            campaign.created_at
                        ).toLocaleDateString()}
                    </p>
                </div>

                <div>
                    <p className="text-sm text-gray-500">
                        Créateur
                    </p>
                    <p>
                        #{campaign.created_by}
                    </p>
                </div>

            </div>
        </section>

        <section className="bg-white border rounded-xl p-6 shadow-sm">
            <h2 className="font-semibold mb-4">
                Contacts associés
            </h2>

            {campaign.contacts?.length ? (
                <p>
                    {campaign.contacts.length} contact(s)
                </p>
            ) : (
                <p className="text-gray-500">
                    Aucun contact associé.
                </p>
            )}
        </section>
    </main>
);
}