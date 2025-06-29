from typing import Any

from django.core.management.base import BaseCommand

from api.swapi_service import SWAPIService


class Command(BaseCommand):
    help = "Fetch and sync SWAPI data (films, characters, starships) into the database."

    def __init__(self) -> None:
        super().__init__()
        self.service = SWAPIService()

    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write("Syncing Films...")
        self.service.fetch_and_store_films()
        self.stdout.write("Syncing Characters...")
        self.service.fetch_and_store_characters()
        self.stdout.write("Syncing Starships...")
        self.service.fetch_and_store_starships()
        self.stdout.write(self.style.SUCCESS("SWAPI data sync complete!"))
