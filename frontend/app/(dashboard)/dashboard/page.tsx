"use client";

import { useDashboard } from "@/hooks/useDashboard";
import StatCard from "@/components/dashboard/StatCard";


export default function DashboardPage() {

    const {
        stats,
        loading,
        error
    } = useDashboard();


    if (loading) {
        return <p>Chargement...</p>;
    }


    if (error || !stats) {
        return <p>{error}</p>;
    }


    return (
        <main className="space-y-8">
            <div>
                <h1 className="text-2xl font-bold">
                    Dashboard
                </h1>
                <p className="text-gray-500 mt-1">
                    Vue globale de votre activité
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <StatCard
                    title="Campagnes"
                    value={stats.campaigns_count}
                    description="Campagnes créées"
                />
                <StatCard
                    title="Contacts"
                    value={stats.contacts_count}
                    description="Contacts enregistrés"
                />
                <StatCard
                    title="Imports"
                    value={stats.imports_count}
                    description="Imports effectués"
                />

            </div>

            <section className="bg-white border rounded-xl p-6">
                <h2 className="font-semibold mb-4">
                    Activité récente
                </h2>

                <p className="text-gray-500">
                    Aucune activité récente disponible.
                </p>
            </section>
        </main>
    );
}