import api from "./api";
import { getToken } from "@/lib/token";
import { Import } from "@/types/import";


export async function getImports() {
    const token = getToken();

    const response = await api.get<Import[]>(
        "/imports/",
        {
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

    const response = await api.post(
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