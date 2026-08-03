"use client";

import { useState } from "react";
import { useImports } from "@/hooks/useImports";
import ImportTable from "@/components/import/ImportTable";
import ImportForm from "@/components/import/ImportForm";
import Card from "@/components/ui/Card";
import EmptyState from "@/components/ui/EmptyState";
import Loader from "@/components/ui/Loader";

export default function ImportsPage() {

    const { imports, loading, error } = useImports();
    const [search, setSearch] = useState("");


    const filteredImports = imports.filter((item) =>
        item.filename
            .toLowerCase()
            .includes(search.toLowerCase())
    );


    if (loading) return <Loader />;

    if (error) return <p>{error}</p>;


    return (
        <main className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">
                    Imports
                </h1>
                <p className="text-gray-500">
                    Historique des imports
                </p>
            </div>

            <ImportForm />

            <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Rechercher un fichier..."
                className="w-full bg-white border rounded-lg px-4 py-3"
            />
            filteredImports.length ? (
                <ImportTable imports={filteredImports} />
            ) : (
                <EmptyState message="Aucun import trouvé" />
            )
        </main>
    );
}