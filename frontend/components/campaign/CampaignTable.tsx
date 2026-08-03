import { Campaign } from "@/types/campaign";
import StatusBadge from "./StatusBadge";
import Link from "next/link";


interface Props {
    campaigns: Campaign[];
}


export default function CampaignTable({
    campaigns
}: Props) {

    return (
        <div className="bg-white border rounded-xl shadow-sm overflow-hidden">
            <table className="w-full">
                <thead className="bg-gray-50 border-b">
                    <tr>
                        <th className="text-left p-4 text-sm font-medium text-gray-500">
                            Nom
                        </th>
                        <th className="text-left p-4 text-sm font-medium text-gray-500">
                            Description
                        </th>
                        <th className="text-left p-4 text-sm font-medium text-gray-500">
                            Statut
                        </th>
                        <th className="text-left p-4 text-sm font-medium text-gray-500">
                            Créée le
                        </th>
                        <th className="p-4 text-left text-sm font-medium text-gray-500">
                            Action
                        </th>
                    </tr>
                </thead>

                <tbody>
                    {campaigns.map((campaign) => (
                        <tr
                            key={campaign.id}
                            className="border-b hover:bg-gray-50"
                        >
                            <td className="p-4 font-medium">
                                {campaign.title}
                            </td>
                            <td className="p-4 text-gray-600">
                                {campaign.description}
                            </td>
                            <td className="p-4">
                                <StatusBadge
                                    status={campaign.status}
                                />
                            </td>
                            <td className="p-4 text-gray-500">
                                {new Date(
                                    campaign.created_at
                                ).toLocaleDateString()}
                            </td>
                            <td className="p-4">
                                <Link
                                        href={`/campaigns/${campaign.id}`}
                                        className="px-3 py-2 rounded-lg bg-blue-50 text-blue-600 text-sm hover:bg-blue-100"
                                    >
                                        Voir
                                </Link>
                            </td>
                        </tr>

                    ))}
                </tbody>
            </table>
        </div>
    );
}