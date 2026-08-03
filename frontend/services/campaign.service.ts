import api from "./api";
import { Campaign } from "@/types/campaign";
import { getToken } from "@/lib/token";


export async function getCampaigns() {

    const token = getToken();

    const response = await api.get<Campaign[]>(
        "/campaigns/",
        {
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