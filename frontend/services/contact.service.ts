import api from "./api";
import { getToken } from "@/lib/token";
import { Contact } from "@/types/contact";


export async function getContacts() {
    const token = getToken();

    const response = await api.get<Contact[]>(
        "/contacts/",
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    return response.data;
}