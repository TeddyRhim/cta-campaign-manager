import { Import } from "@/types/import";


interface Props {
    imports: Import[];
}


export default function ImportTable({ imports }: Props) {

    return (
        <div className="bg-white border rounded-xl shadow-sm overflow-hidden">
            <table className="w-full">
                <thead className="bg-gray-50 border-b">
                    <tr>
                        <th className="p-4 text-left text-sm text-gray-500">
                            Fichier
                        </th>
                        <th className="p-4 text-left text-sm text-gray-500">
                            Statut
                        </th>
                        <th className="p-4 text-left text-sm text-gray-500">
                            Date
                        </th>
                    </tr>
                </thead>

                <tbody>
                    {imports.map((item) => (
                        <tr
                            key={item.id}
                            className="border-b hover:bg-gray-50"
                        >
                            <td className="p-4 font-medium">
                                {item.filename}
                            </td>
                            <td className="p-4">
                                <span className="px-3 py-1 rounded-full text-sm bg-gray-100">
                                    {item.status}
                                </span>
                            </td>
                            <td className="p-4 text-gray-600">
                                {new Date(
                                    item.created_at
                                ).toLocaleDateString()}
                            </td>

                        </tr>

                    ))}
                </tbody>
            </table>
        </div>
    );
}