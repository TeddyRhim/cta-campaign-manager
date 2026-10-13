"use client";

import { getContacts } from "@/services/contact.service";
import { usePaginatedList } from "./usePaginatedList";


export function useContacts() {
    const list = usePaginatedList(getContacts, "Impossible de charger les contacts");

    return { ...list, contacts: list.items };
}
