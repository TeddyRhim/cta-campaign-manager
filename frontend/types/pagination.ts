export interface Page<T> {
    items: T[];
    total: number;
    page: number;
    page_size: number;
}

export interface PageQuery {
    page: number;
    pageSize: number;
    search?: string;
}
