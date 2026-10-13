import api from "./api";
import { Page, PageQuery } from "@/types/pagination";
import { getToken } from "@/lib/token";
import { Import } from "@/types/import";


export async function getImports(query: PageQuery) {
    const token = getToken();

    const response = await api.get<Page<Import>>(
        "/imports/",
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


export async function uploadImport(
    file: File,
    campaignId: number
) {

    const token = getToken();

    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post<Import>(
        `/imports/?campaign_id=${campaignId}`,
        formData,
        {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "multipart/form-data"
            }
        }
    );

    return response.data;
}