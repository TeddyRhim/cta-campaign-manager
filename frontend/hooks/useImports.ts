"use client";

import { useEffect, useState } from "react";
import { Import } from "@/types/import";
import { getImports } from "@/services/import.service";


export function useImports() {
    const [imports, setImports] = useState<Import[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    useEffect(() => {
        async function fetchImports() {
            try {
                const data = await getImports();

                setImports(data);
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
    }, []);


    return {
        imports,
        loading,
        error
    };
}