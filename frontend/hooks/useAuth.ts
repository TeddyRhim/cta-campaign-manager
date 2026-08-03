"use client";

import { useEffect, useState } from "react";
import { getCurrentUser } from "@/services/auth.service";
import { User } from "@/types/user";


export function useAuth() {

    const [user, setUser] = useState<User | null>(null);

    const [loading, setLoading] = useState(true);


    useEffect(() => {

        async function loadUser() {

            try {

                const currentUser = await getCurrentUser();

                setUser(currentUser);

            } catch (error) {

                console.error(error);

            } finally {

                setLoading(false);

            }

        }


        loadUser();

    }, []);


    return {
        user,
        loading
    };
}