"use client";

import { useEffect, useState } from "react";
import { Import } from "@/types/import";
import { getImports } from "@/services/import.service";


export function useImports() {
    const [imports, setImports] = useState<Import[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [version, setVersion] = useState(0);


    useEffect(() => {
        async function fetchImports() {
            try {
                const data = await getImports();

                setImports(data);
                setError("");
            } catch(error) {
                console.error(
                    "Erreur chargement imports :",
                    error
                );

                setError(
                    "Impossible de charger les imports"
                );
            } finally {
                setLoading(false);
            }
        }


        fetchImports();
    }, [version]);


    function refetch() {
        setVersion((current) => current + 1);
    }


    return {
        imports,
        loading,
        error,
        refetch
    };
}
