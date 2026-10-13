import axios from "axios";

const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

api.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            localStorage.removeItem("access_token");

            // Hors composant React (intercepteur Axios) : useRouter() n'est pas disponible ici.
            // eslint-disable-next-line @next/next/no-location-assign-relative-destination
            window.location.href = "/login";
        }

        return Promise.reject(error);
    }
);

export default api;