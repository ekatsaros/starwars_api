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

        # Prefetch all existing films into a dictionary keyed by swapi_url
        incoming_urls = [film_data["url"] for film_data in films_data]
        existing_films_dict: Dict[str, Film] = {
            film.swapi_url: film for film in Film.objects.filter(swapi_url__in=incoming_urls)
        }

        films_to_create = []
        films_to_update = []

        for film_data in films_data:
            # Parse the release_date from SWAPI format (YYYY-MM-DD) to date object
            release_date = datetime.strptime(film_data["release_date"], "%Y-%m-%d").date()

            if film_data["url"] in existing_films_dict:
                # Update existing film (no database query needed)
                film = existing_films_dict[film_data["url"]]
                film.title = film_data["title"]
                film.release_date = release_date
                film.data = film_data
                films_to_update.append(film)
            else:
                # Create new film
                films_to_create.append(
                    Film(
                        title=film_data["title"],
                        swapi_url=film_data["url"],
                        release_date=release_date,
                        data=film_data,
                    )
                )

        # Perform bulk operations
        created_films = Film.objects.bulk_create(films_to_create) if films_to_create else []

        if films_to_update:
            Film.objects.bulk_update(films_to_update, fields=["title", "release_date", "data"])

        # Build films cache right after creating/updating films
        self._build_films_cache()

        return created_films + films_to_update

    @transaction.atomic
    def fetch_and_store_starships(self) -> List[Starship]:
        starships_data = self.client.fetch_starships()

        # Prefetch all existing starships into a dictionary keyed by swapi_url
        incoming_urls = [starship_data["url"] for starship_data in starships_data]
        existing_starships_dict: Dict[str, Starship] = {
            starship.swapi_url: starship for starship in Starship.objects.filter(swapi_url__in=incoming_urls)
        }

        starships_to_create = []
        starships_to_update = []

        for starship_data in starships_data:
            if starship_data["url"] in existing_starships_dict:
                # Update existing starship (no database query needed - using dict lookup)
                starship = existing_starships_dict[starship_data["url"]]
                starship.name = starship_data["name"]
                starship.data = starship_data
                starships_to_update.append(starship)
            else:
                # Create new starship
                starships_to_create.append(
                    Starship(
                        name=starship_data["name"],
                        swapi_url=starship_data["url"],
                        data=starship_data,
                    )
                )

        # Perform bulk operations
        created_starships = Starship.objects.bulk_create(starships_to_create) if starships_to_create else []

        if starships_to_update:
            Starship.objects.bulk_update(starships_to_update, fields=["name", "data"])

        # Build starships cache right after creating/updating starships
        self._build_starships_cache()

        return created_starships + starships_to_update

    @transaction.atomic
    def fetch_and_store_characters(self) -> List[Character]:
        # Ensure caches are built before accessing them if they are empty
        if not self.films_cache:
            self._build_films_cache()
        if not self.starships_cache:
            self._build_starships_cache()

        characters_data = self.client.fetch_people()

        # Prefetch all existing characters into a dictionary keyed by swapi_url
        incoming_urls = [character_data["url"] for character_data in characters_data]
        existing_characters_dict: Dict[str, Character] = {
            character.swapi_url: character for character in Character.objects.filter(swapi_url__in=incoming_urls)
        }

        characters_to_create = []
        characters_to_update = []

        for character_data in characters_data:
            if character_data["url"] in existing_characters_dict:
                # Update existing character (no database query needed)
                character = existing_characters_dict[character_data["url"]]
                character.name = character_data["name"]
                character.data = character_data
                characters_to_update.append(character)
            else:
                # Create new character
                characters_to_create.append(
                    Character(
                        name=character_data["name"],
                        swapi_url=character_data["url"],
                        data=character_data,
                    )
                )

        # Perform bulk operations
        created_characters = Character.objects.bulk_create(characters_to_create) if characters_to_create else []

        if characters_to_update:
            Character.objects.bulk_update(characters_to_update, fields=["name", "data"])

        # Handle many-to-many relationships for all characters (both new and updated)
        all_characters = list(created_characters) + characters_to_update
        characters_data_dict = {char_data["url"]: char_data for char_data in characters_data}

        for character in all_characters:
            character_data = characters_data_dict[character.swapi_url]

            # Clear existing relationships for updated characters
            character.films.clear()
            character.starships.clear()

            # Add films
            films = [self.films_cache[film_url] for film_url in character_data["films"] if film_url in self.films_cache]
            if films:
                character.films.add(*films)

            # Add starships
            starships = [
                self.starships_cache[starship_url]
                for starship_url in character_data["starships"]
                if starship_url in self.starships_cache
            ]
            if starships:
                character.starships.add(*starships)

        return all_characters
