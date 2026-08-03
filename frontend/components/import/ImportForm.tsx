"use client";

import { useState } from "react";
import { uploadImport } from "@/services/import.service";


export default function ImportForm() {

    const [file, setFile] = useState<File | null>(null);
    const [message, setMessage] = useState("");
    const [campaignId, setCampaignId] = useState("");


    async function handleSubmit(e: React.FormEvent) {

        e.preventDefault();

        if (!file) return;

        try {
            await uploadImport(
                file,
                Number(campaignId)
            );
            setMessage("Import réussi");
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