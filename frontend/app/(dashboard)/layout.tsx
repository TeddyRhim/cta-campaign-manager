"use client";

import { ReactNode, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/token";

import Navbar from "@/components/layout/Navbar";
import Sidebar from "@/components/layout/Sidebar";


export default function DashboardLayout({
    children,
}: {
    children: ReactNode;
}) {

    const router = useRouter();

    const [checked, setChecked] = useState(false);


    useEffect(() => {

        const token = getToken();

        if (!token) {
            router.push("/login");
            return;
        }

        setChecked(true);

    }, [router]);


    if (!checked) {
        return <p>Chargement...</p>;
    }


    return (
        <div className="min-h-screen bg-gray-100">
            <Navbar />
            <div className="flex">
                <Sidebar />
                <main className="flex-1 p-6">
                    {children}
                </main>
            </div>
        </div>
    );
}