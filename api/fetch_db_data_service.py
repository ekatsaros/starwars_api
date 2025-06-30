from typing import Any, Dict, Optional, Type, TypeVar

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import DatabaseError
from django.db.models import Model

from api.models import Character, Film, Starship

T = TypeVar("T", bound=Model)


class DatabaseServiceException(Exception):
    """Base exception for database service errors."""

    pass


class FetchDBDataService:
    PAGE_SIZE = 10

    @staticmethod
    def get_paginated_data(model_class: Type[T], page: int = 1, search_query: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve paginated data for the given model with optional search.
        """
        try:
            queryset = model_class.objects.all()
            if search_query:
                search_field = "name" if model_class == Character else "title" if model_class == Film else "name"
                queryset = queryset.filter(**{f"{search_field}__icontains": search_query})

            paginator = Paginator(queryset, FetchDBDataService.PAGE_SIZE)
            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)

            return {
                "items": list(page_obj),
                "total_pages": paginator.num_pages,
                "current_page": page_obj.number,
                "total_items": paginator.count,
            }

        except DatabaseError as e:
            raise DatabaseServiceException(f"Database error occurred: {str(e)}")

    @classmethod
    def get_characters(cls, page: int = 1, search_query: Optional[str] = None) -> Dict[str, Any]:
        """Get paginated characters with optional search."""
        return cls.get_paginated_data(Character, page, search_query)

    @classmethod
    def get_films(cls, page: int = 1, search_query: Optional[str] = None) -> Dict[str, Any]:
        """Get paginated films with optional search."""
        return cls.get_paginated_data(Film, page, search_query)

    @classmethod
    def get_starships(cls, page: int = 1, search_query: Optional[str] = None) -> Dict[str, Any]:
        """Get paginated starships with optional search."""
        return cls.get_paginated_data(Starship, page, search_query)
