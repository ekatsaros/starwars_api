from datetime import datetime
from typing import Dict, List

from django.db import transaction

from api.models import Character, Film, Starship
from clients.swapi_client import SWAPIClient


class SWAPIService:
    def __init__(self) -> None:
        self.client = SWAPIClient(disable_ssl_verification=True)
        self.films_cache: Dict[str, Film] = {}
        self.starships_cache: Dict[str, Starship] = {}

    def _build_films_cache(self) -> None:
        """Build cache mapping SWAPI URLs to Film objects"""
        films = Film.objects.all()
        self.films_cache = {film.swapi_url: film for film in films}

    def _build_starships_cache(self) -> None:
        """Build cache mapping SWAPI URLs to Starship objects"""
        starships = Starship.objects.all()
        self.starships_cache = {starship.swapi_url: starship for starship in starships}

    @transaction.atomic
    def fetch_and_store_films(self) -> List[Film]:
        films_data = self.client.fetch_films()
        stored_films = []

        films_to_create = []
        for film_data in films_data:
            # Parse the release_date from SWAPI format (YYYY-MM-DD) to date object
            release_date = datetime.strptime(film_data["release_date"], "%Y-%m-%d").date()
            films_to_create.append(
                Film(
                    title=film_data["title"],
                    swapi_url=film_data["url"],
                    release_date=release_date,
                    data=film_data,
                )
            )
        stored_films = Film.objects.bulk_create(films_to_create)
        # Build films cache right after creating films
        self._build_films_cache()

        return stored_films

    @transaction.atomic
    def fetch_and_store_starships(self) -> List[Starship]:
        starships_data = self.client.fetch_starships()
        starships_to_create = []
        for starship_data in starships_data:
            starships_to_create.append(
                Starship(
                    name=starship_data["name"],
                    swapi_url=starship_data["url"],
                    data=starship_data,
                )
            )
        stored_starships = Starship.objects.bulk_create(starships_to_create)
        # Build starships cache right after creating starships
        self._build_starships_cache()
        return stored_starships

    @transaction.atomic
    def fetch_and_store_characters(self) -> List[Character]:
        # Ensure caches are built before accessing them if they are empty
        if not self.films_cache:
            self._build_films_cache()
        if not self.starships_cache:
            self._build_starships_cache()

        characters_data = self.client.fetch_people()
        stored_characters = []

        for character_data in characters_data:
            # Create the character first
            character = Character.objects.create(
                name=character_data["name"],
                swapi_url=character_data["url"],
                data=character_data,
            )

            # Add many-to-many relationships after creation
            # Add films
            films = [self.films_cache[film_url] for film_url in character_data["films"] if film_url in self.films_cache]
            character.films.add(*films)
            # Add starships
            starships = [
                self.starships_cache[starship_url]
                for starship_url in character_data["starships"]
                if starship_url in self.starships_cache
            ]
            character.starships.add(*starships)

            stored_characters.append(character)

        return stored_characters
