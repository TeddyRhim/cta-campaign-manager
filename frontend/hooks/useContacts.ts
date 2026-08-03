"use client";

import { useEffect, useState } from "react";
import { Contact } from "@/types/contact";
import { getContacts } from "@/services/contact.service";


export function useContacts() {
    const [contacts, setContacts] = useState<Contact[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    useEffect(() => {
        async function fetchContacts() {
            try {
                const data = await getContacts();

                setContacts(data);
            } catch(error) {
                console.error(
                    "Erreur chargement contacts :",
                    error
                );

                setError(
                    "Impossible de charger les contacts"
                );
            } finally {
                setLoading(false);
            }
        }


        fetchContacts();
    }, []);


    return {
        contacts,
        loading,
        error
    };
}