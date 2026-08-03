import Link from "next/link";
import { Contact } from "@/types/contact";


interface Props {
    contacts: Contact[];
}


export default function ContactTable({ contacts }: Props) {

    return (
        <div className="bg-white border rounded-xl shadow-sm overflow-hidden">
            <table className="w-full">
                <thead className="bg-gray-50 border-b">
                    <tr>
                        <th className="p-4 text-left text-sm text-gray-500">Nom</th>
                        <th className="p-4 text-left text-sm text-gray-500">Email</th>
                        <th className="p-4 text-left text-sm text-gray-500">Téléphone</th>
                    </tr>
                </thead>

                <tbody>
                    {contacts.map((contact) => (
                        <tr key={contact.id} className="border-b hover:bg-gray-50">
                            <td className="p-4 font-medium">
                                {contact.firstname} {contact.lastname}
                            </td>
                            <td className="p-4 text-gray-600">
                                {contact.email}
                            </td>
                            <td className="p-4 text-gray-600">
                                {contact.phone || "-"}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}