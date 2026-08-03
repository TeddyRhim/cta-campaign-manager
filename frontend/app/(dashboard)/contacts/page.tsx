"use client";

import { useState } from "react";
import { useContacts } from "@/hooks/useContacts";
import ContactTable from "@/components/contact/ContactTable";
import Card from "@/components/ui/Card";
import Loader from "@/components/ui/Loader";
import EmptyState from "@/components/ui/EmptyState";


export default function ContactsPage() {

    const { contacts, loading, error } = useContacts();
    const [search, setSearch] = useState("");


    const filteredContacts = contacts.filter((contact) =>
        `${contact.firstname} ${contact.lastname} ${contact.email}`
            .toLowerCase()
            .includes(search.toLowerCase())
    );


    if (loading) return <Loader />;

    if (error) return <EmptyState message={error} />;

    return (
        <main className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">
                    Contacts
                </h1>
                <p className="text-gray-500">
                    Gestion des contacts
                </p>
            </div>

          <Card>
            <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Rechercher un contact..."
                className="w-full border rounded-lg px-4 py-3"
            />
        </Card>
            {filteredContacts.length ? (
                <Card>
                    <ContactTable contacts={filteredContacts} />
                </Card>
            ) : (
                <EmptyState message="Aucun contact trouvé" />
            )}
        </main>
    );
}