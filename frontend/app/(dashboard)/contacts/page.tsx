"use client";

import { useContacts } from "@/hooks/useContacts";
import ContactTable from "@/components/contact/ContactTable";
import Card from "@/components/ui/Card";
import Loader from "@/components/ui/Loader";
import EmptyState from "@/components/ui/EmptyState";
import Pagination from "@/components/ui/Pagination";


export default function ContactsPage() {

    // La recherche et la pagination sont faites par l'API, sur tous les contacts.
    const {
        contacts, loading, error, search, setSearch, page, pageCount, total, setPage
    } = useContacts();


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
            {contacts.length ? (
                <>
                    <Card>
                        <ContactTable contacts={contacts} />
                    </Card>
                    <Pagination page={page} pageCount={pageCount} total={total} onChange={setPage} />
                </>
            ) : (
                <EmptyState message="Aucun contact trouvé" />
            )}
        </main>
    );
}