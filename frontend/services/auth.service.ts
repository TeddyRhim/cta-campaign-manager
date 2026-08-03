import api from "./api";
import { LoginResponse } from "@/types/auth";
import { setToken, getToken, removeToken } from "@/lib/token";
import { User } from "@/types/user";


export async function login(
    email: string,
    password: string
) {
    const response = await api.post<LoginResponse>(
        "/auth/login", 
        {
            email,
            password
        },
        {
            headers: {
                "Content-Type": "application/json"
            }
        }
    )
    const data = response.data;

    setToken(data.access_token);

    return data;
}

export async function getCurrentUser(): Promise<User> {

    const token = getToken();

    const response = await api.get<User>(
        "/auth/me",
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    return response.data;
}

export function logout() {
    removeToken();
}