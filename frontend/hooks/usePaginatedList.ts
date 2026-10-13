"use client";

import { useEffect, useState } from "react";
import { Page, PageQuery } from "@/types/pagination";


const SEARCH_DELAY_MS = 300;


/**
 * Liste paginée côté serveur : page courante, recherche (envoyée après une courte pause
 * de saisie) et rechargement. `loading` ne vaut true qu'au premier chargement, pour que
 * la page (et le champ de recherche) reste affichée pendant les changements de page.
 */
export function usePaginatedList<T>(
    fetchPage: (query: PageQuery) => Promise<Page<T>>,
    errorMessage: string,
    pageSize = 20
) {
    const [items, setItems] = useState<T[]>([]);
    const [total, setTotal] = useState(0);
    const [page, setPage] = useState(1);
    const [search, setSearch] = useState("");
    const [debouncedSearch, setDebouncedSearch] = useState("");
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [error, setError] = useState("");
    const [version, setVersion] = useState(0);


    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedSearch(search.trim());
            setPage(1);
        }, SEARCH_DELAY_MS);

        return () => clearTimeout(timer);
    }, [search]);


    useEffect(() => {
        let cancelled = false;

        async function load() {
            setRefreshing(true);
            try {
                const data = await fetchPage({
                    page,
                    pageSize,
                    search: debouncedSearch || undefined
                });

                if (cancelled) return;
                setItems(data.items);
                setTotal(data.total);
                setError("");
            } catch (err) {
                if (cancelled) return;
                console.error(errorMessage, err);
                setError(errorMessage);
            } finally {
                if (!cancelled) {
                    setLoading(false);
                    setRefreshing(false);
                }
            }
        }

        load();

        // Une réponse arrivée après un changement de page ou de recherche est ignorée.
        return () => {
            cancelled = true;
        };
    }, [fetchPage, errorMessage, page, pageSize, debouncedSearch, version]);


    return {
        items,
        total,
        page,
        pageCount: Math.max(1, Math.ceil(total / pageSize)),
        setPage,
        search,
        setSearch,
        loading,
        refreshing,
        error,
        refetch: () => setVersion((current) => current + 1)
    };
}
