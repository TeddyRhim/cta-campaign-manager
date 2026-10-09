export interface Contact {
    id: number;
    first_name: string;
    last_name: string;
    email?: string | null;
    phone?: string | null;
    organization?: string | null;
    created_at: string;
}