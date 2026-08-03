import api from "./api";
import { getToken } from "@/lib/token";
import { DashboardStats } from "@/types/dashboard";


export async function getDashboardStats() {
    const token = getToken();

    const response = await api.get<DashboardStats>(
        "/dashboard/stats",
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    return response.data;
}