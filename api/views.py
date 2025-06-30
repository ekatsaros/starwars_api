from typing import List

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.authentication import BaseAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CharacterSerializer, FilmSerializer, StarshipSerializer, VoteSerializer

from .exceptions import UniqueConstraintError
from .fetch_db_data_service import DatabaseServiceException, FetchDBDataService


class FilmApiView(APIView):
    """API view to list all films."""

    authentication_classes: List[BaseAuthentication] = []  # No authentication required for fetching films
    permission_classes: List[BasePermission] = [AllowAny]  # Allow any user to fetch films

    @extend_schema(
        description="List all films",
        request=None,
        responses={200: FilmSerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name="page", type=int, description="Page number for pagination", required=False, default=1
            ),
            OpenApiParameter(name="search", type=str, description="Search query for film titles", required=False),
        ],
    )
    def get(self, request: Request) -> Response:
        """List all films with pagination and optional search."""
        try:
            # Get query parameters
            page = int(request.query_params.get("page", 1))
            search_query = request.query_params.get("search", None)

            # Get paginated films data from service
            films_data = FetchDBDataService.get_films(page=page, search_query=search_query)

            # Serialize the film instances
            serializer = FilmSerializer(films_data["items"], many=True)

            return Response(
                {
                    "films": serializer.data,
                    "pagination": {
                        "total_pages": films_data["total_pages"],
                        "current_page": films_data["current_page"],
                        "total_items": films_data["total_items"],
                    },
                }
            )

        except DatabaseServiceException as e:
            return Response({"error": f"Database error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            return Response({"error": f"Invalid page number {e}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StarshipApiView(APIView):
    """API view to list all starships."""

    authentication_classes: List[BaseAuthentication] = []  # No authentication required for fetching starships
    permission_classes: List[BasePermission] = [AllowAny]  # Allow any user to fetch starships

    @extend_schema(
        description="List all starships",
        request=None,
        responses={200: StarshipSerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name="page", type=int, description="Page number for pagination", required=False, default=1
            ),
            OpenApiParameter(name="search", type=str, description="Search query for starship names", required=False),
        ],
    )
    def get(self, request: Request) -> Response:
        """List all starships with pagination and optional search."""
        try:
            # Get query parameters
            page = int(request.query_params.get("page", 1))
            search_query = request.query_params.get("search", None)

            # Get paginated starships data from service
            starships_data = FetchDBDataService.get_starships(page=page, search_query=search_query)

            # Serialize the starship instances
            serializer = StarshipSerializer(starships_data["items"], many=True)

            return Response(
                {
                    "starships": serializer.data,
                    "pagination": {
                        "total_pages": starships_data["total_pages"],
                        "current_page": starships_data["current_page"],
                        "total_items": starships_data["total_items"],
                    },
                }
            )

        except DatabaseServiceException as e:
            return Response({"error": f"Database error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            return Response({"error": f"Invalid page number {e}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CharacterApiView(APIView):
    """API view to list all characters."""

    authentication_classes: List[BaseAuthentication] = []  # No authentication required for fetching characters
    permission_classes: List[BasePermission] = [AllowAny]  # Allow any user to fetch characters

    @extend_schema(
        description="List all characters",
        request=None,
        responses={200: CharacterSerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name="page", type=int, description="Page number for pagination", required=False, default=1
            ),
            OpenApiParameter(name="search", type=str, description="Search query for character names", required=False),
        ],
    )
    def get(self, request: Request) -> Response:
        """List all characters with pagination and optional search."""
        try:
            # Get query parameters
            page = int(request.query_params.get("page", 1))
            search_query = request.query_params.get("search", None)

            # Get paginated characters data from service
            characters_data = FetchDBDataService.get_characters(page=page, search_query=search_query)

            # Serialize the character instances
            serializer = CharacterSerializer(characters_data["items"], many=True)

            return Response(
                {
                    "characters": serializer.data,
                    "pagination": {
                        "total_pages": characters_data["total_pages"],
                        "current_page": characters_data["current_page"],
                        "total_items": characters_data["total_items"],
                    },
                }
            )

        except DatabaseServiceException as e:
            return Response({"error": f"Database error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            return Response({"error": f"Invalid page number {e}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VoteApiView(APIView):
    """API view for voting on Films, Characters, or Starships."""

    authentication_classes: List[BaseAuthentication] = [TokenAuthentication]
    permission_classes: List[BasePermission] = [IsAuthenticated]

    @extend_schema(
        description="Vote for a Film, Character, or Starship",
        request=VoteSerializer,
        responses={201: VoteSerializer},
    )
    def post(self, request: Request) -> Response:
        """Create a vote for a specific item."""
        try:
            serializer = VoteSerializer(data=request.data)
            if serializer.is_valid():
                # Set the user from the authenticated request
                serializer.validated_data["user"] = request.user
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UniqueConstraintError as e:
            return Response(
                {"error": "You have already voted for an item.", "detail": str(e)}, status=status.HTTP_409_CONFLICT
            )
        except DatabaseServiceException as e:
            return Response({"error": f"Database error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
