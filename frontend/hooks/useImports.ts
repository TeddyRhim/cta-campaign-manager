"use client";

import { getImports } from "@/services/import.service";
import { usePaginatedList } from "./usePaginatedList";


export function useImports() {
    const list = usePaginatedList(getImports, "Impossible de charger les imports");

    return { ...list, imports: list.items };
}
