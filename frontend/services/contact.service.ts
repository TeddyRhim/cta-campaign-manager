import api from "./api";
import { Page, PageQuery } from "@/types/pagination";
import { getToken } from "@/lib/token";
import { Contact } from "@/types/contact";


export async function getContacts(query: PageQuery) {
    const token = getToken();

    const response = await api.get<Page<Contact>>(
        "/contacts/",
        {
            params: {
                page: query.page,
                page_size: query.pageSize,
                search: query.search
            },
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    return response.data;
}