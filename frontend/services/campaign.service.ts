import api from "./api";
import { Page, PageQuery } from "@/types/pagination";
import { Campaign } from "@/types/campaign";
import { getToken } from "@/lib/token";


export async function getCampaigns(query: PageQuery) {

    const token = getToken();

    const response = await api.get<Page<Campaign>>(
        "/campaigns/",
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

export async function getCampaignById(
    id: number
) {

    const token = getToken();

    const response = await api.get<Campaign>(
        `/campaigns/${id}`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    return response.data;
}