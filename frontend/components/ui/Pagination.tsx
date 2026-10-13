interface Props {
    page: number;
    pageCount: number;
    total: number;
    onChange: (page: number) => void;
}


export default function Pagination({
    page,
    pageCount,
    total,
    onChange
}: Props) {

    const buttonClass =
        "px-3 py-2 rounded-lg border bg-white hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed";

    return (
        <nav
            aria-label="Pagination"
            className="flex items-center justify-between text-sm text-gray-600"
        >
            <span>
                {total} résultat{total > 1 ? "s" : ""}
            </span>

            <div className="flex items-center gap-3">
                <button
                    type="button"
                    className={buttonClass}
                    onClick={() => onChange(page - 1)}
                    disabled={page <= 1}
                >
                    Précédent
                </button>

                <span aria-current="page">
                    Page {page} / {pageCount}
                </span>

                <button
                    type="button"
                    className={buttonClass}
                    onClick={() => onChange(page + 1)}
                    disabled={page >= pageCount}
                >
                    Suivant
                </button>
            </div>
        </nav>
    );
}
