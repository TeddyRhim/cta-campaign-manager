"use client";

import { useImports } from "@/hooks/useImports";
import ImportTable from "@/components/import/ImportTable";
import ImportForm from "@/components/import/ImportForm";
import EmptyState from "@/components/ui/EmptyState";
import Loader from "@/components/ui/Loader";
import Pagination from "@/components/ui/Pagination";

export default function ImportsPage() {

    // La recherche et la pagination sont faites par l'API, sur tous les imports.
    const {
        imports, loading, error, refetch, search, setSearch, page, pageCount, total, setPage
    } = useImports();


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

            <ImportForm onImported={refetch} />

            <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Rechercher un fichier..."
                className="w-full bg-white border rounded-lg px-4 py-3"
            />
            {imports.length ? (
                <>
                    <ImportTable imports={imports} />
                    <Pagination page={page} pageCount={pageCount} total={total} onChange={setPage} />
                </>
            ) : (
                <EmptyState message="Aucun import trouvé" />
            )}
        </main>
    );
}