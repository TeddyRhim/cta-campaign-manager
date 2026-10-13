from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    """Une page de résultats : `total` permet au client de calculer le nombre de pages."""

    items: list[T]
    total: int
    page: int
    page_size: int
