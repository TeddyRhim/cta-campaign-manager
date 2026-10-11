"use client";

import { useState } from "react";
import { uploadImport } from "@/services/import.service";


interface Props {
    onImported?: () => void;
}


export default function ImportForm({ onImported }: Props) {

    const [file, setFile] = useState<File | null>(null);
    const [message, setMessage] = useState("");
    const [campaignId, setCampaignId] = useState("");


    async function handleSubmit(e: React.FormEvent) {

        e.preventDefault();

        if (!file) return;

        try {
            const result = await uploadImport(
                file,
                Number(campaignId)
            );

            if (result.success_count === 0 && result.error_count > 0) {
                setMessage(
                    `Import échoué : aucune ligne valide (${result.error_count} en erreur)`
                );
            } else if (result.error_count > 0) {
                setMessage(
                    `Import partiel : ${result.success_count} ligne(s) importée(s), ${result.error_count} en erreur`
                );
            } else {
                setMessage(
                    `Import réussi : ${result.success_count} ligne(s) importée(s)`
                );
            }

            onImported?.();
        } catch (error) {
            console.error(error);
            setMessage("Erreur lors de l'import");
        }
    }

    return (
        <form onSubmit={handleSubmit} className="bg-white border rounded-xl p-5 space-y-4">
            <h2 className="font-semibold">
                Nouvel import
            </h2>
            <input
                type="file"
                onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            />
            <input
                type="number"
                placeholder="ID campagne"
                value={campaignId}
                onChange={(e) => setCampaignId(e.target.value)}
                className="border rounded-lg px-3 py-2"
            />
            <button
                type="submit"
                className="px-4 py-2 rounded-lg bg-blue-600 text-white"
            >
                Importer
            </button>

            {message && <p>{message}</p>}
        </form>
    );
}