from datetime import datetime
from typing import List

from django.db import transaction

from api.models import Character, Film, Starship
from clients.swapi_client import SWAPIClient


class SWAPIService:
    def __init__(self) -> None:
        self.client = SWAPIClient(disable_ssl_verification=True)

    @transaction.atomic
    def fetch_and_store_films(self) -> List[Film]:
        films_data = self.client.fetch_films()
        stored_films = []

        for film_data in films_data:
            # Parse the release_date from SWAPI format (YYYY-MM-DD) to date object
            release_date = datetime.strptime(film_data["release_date"], "%Y-%m-%d").date()

            film = Film.objects.create(
                title=film_data["title"],
                swapi_url=film_data["url"],
                release_date=release_date,
                data=film_data,
            )
            stored_films.append(film)

        return stored_films

    @transaction.atomic
    def fetch_and_store_starships(self) -> List[Starship]:
        starships_data = self.client.fetch_starships()
        stored_starships = []

        for starship_data in starships_data:
            starship = Starship.objects.create(
                name=starship_data["name"],
                swapi_url=starship_data["url"],
                data=starship_data,
            )
            stored_starships.append(starship)

        return stored_starships

    @transaction.atomic
    def fetch_and_store_characters(self) -> List[Character]:
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
            for film_url in character_data["films"]:
                try:
                    film = Film.objects.get(swapi_url=film_url)
                    character.films.add(film)
                except Film.DoesNotExist:
                    # Film doesn't exist yet, skip for now
                    pass

            # Add starships
            for starship_url in character_data["starships"]:
                try:
                    starship = Starship.objects.get(swapi_url=starship_url)
                    character.starships.add(starship)
                except Starship.DoesNotExist:
                    # Starship doesn't exist yet, skip for now
                    pass

            stored_characters.append(character)

        return stored_characters
