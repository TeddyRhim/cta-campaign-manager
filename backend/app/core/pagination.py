"""Pagination des listes : paramètres de requête communs et découpage d'une requête SQL."""

from dataclasses import dataclass

from fastapi import Query
from sqlalchemy.orm import Query as SqlQuery

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


@dataclass(frozen=True)
class PageParams:
    page: int
    page_size: int
    search: str | None


def page_params(
    page: int = Query(1, ge=1, description="Numéro de page, à partir de 1"),
    page_size: int = Query(
        DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Éléments par page"
    ),
    search: str | None = Query(None, max_length=100, description="Filtre texte facultatif"),
) -> PageParams:
    cleaned = search.strip() if search else None
    return PageParams(page=page, page_size=page_size, search=cleaned or None)


def paginate(query: SqlQuery, params: PageParams) -> dict:
    """Total et éléments de la page demandée. La requête doit déjà être triée de façon stable."""
    total = query.order_by(None).count()
    items = query.offset((params.page - 1) * params.page_size).limit(params.page_size).all()
    return {
        "items": items,
        "total": total,
        "page": params.page,
        "page_size": params.page_size,
    }
