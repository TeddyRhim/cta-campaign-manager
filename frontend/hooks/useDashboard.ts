"use client";

import { useEffect, useState } from "react";
import { DashboardStats } from "@/types/dashboard";
import { getDashboardStats } from "@/services/dashboard.service";


export function useDashboard() {

    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    useEffect(() => {

        async function fetchStats() {

            try {
                const data = await getDashboardStats();

                setStats(data);

            } catch(error) {

                console.error(
                    "Erreur dashboard :",
                    error
                );

                setError(
                    "Impossible de charger le dashboard"
                );

            } finally {

                setLoading(false);

            }
        }


        fetchStats();

    }, []);


    return {
        stats,
        loading,
        error
    };
}