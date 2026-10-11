"use client";

import { useRouter } from "next/navigation";
import { logout } from "@/services/auth.service";
import { useAuth } from "@/hooks/useAuth";


export default function Navbar() {

    const router = useRouter();

    const { user } = useAuth();


    function handleLogout() {

        logout();

        router.push("/login");
    }


    return (
        <header className="h-16 bg-white border-b flex items-center justify-between px-6">
            <h1 className="text-lg font-semibold">
                CTA Manager
            </h1>

            <div className="flex items-center gap-4">
                <div className="text-right">
                    <p className="text-sm font-medium">
                        {user?.email}
                    </p>

                    <p className="text-xs text-gray-500">
                        {user && (user.role === "ADMIN" ? "Administrateur" : "Opérateur")}
                    </p>
                </div>

                <button
                    onClick={handleLogout}
                    className="px-3 py-2 rounded-lg text-sm text-gray-600 hover:bg-gray-100 transition"
                >
                    Déconnexion
                </button>
            </div>
        </header>
    );
}