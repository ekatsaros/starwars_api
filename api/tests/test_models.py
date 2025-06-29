from datetime import date

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from ..models import Character, Film, Starship, Vote

User = get_user_model()


class FilmModelTest(TestCase):
    """Test cases for the Film model"""

    def setUp(self) -> None:
        """Set up test data"""
        self.film_data = {
            "title": "A New Hope",
            "swapi_url": "https://swapi.dev/api/films/1/",
            "release_date": date(1977, 5, 25),
        }

    def test_create_film(self) -> None:
        """Test creating a film with basic data"""
        film = Film.objects.create(**self.film_data)

        self.assertEqual(film.title, "A New Hope")
        self.assertEqual(film.swapi_url, "https://swapi.dev/api/films/1/")
        self.assertEqual(film.release_date, date(1977, 5, 25))
        self.assertEqual(str(film), "A New Hope")

    def test_film_unique_swapi_url(self) -> None:
        """Test that SWAPI URL must be unique"""
        Film.objects.create(**self.film_data)

        with self.assertRaises(IntegrityError):
            Film.objects.create(**self.film_data)

    def test_film_str_representation(self) -> None:
        """Test string representation of film"""
        film = Film.objects.create(**self.film_data)
        self.assertEqual(str(film), "A New Hope")

    def test_film_characters_relationship(self) -> None:
        """Test many-to-many relationship with characters"""
        film = Film.objects.create(**self.film_data)

        character_data = {
            "name": "Luke Skywalker",
            "swapi_url": "https://swapi.dev/api/people/1/",
            "data": {
                "birth_year": "19 BBY",
                "eye_color": "Blue",
                "gender": "Male",
                "hair_color": "Blond",
                "height": "172",
                "mass": "77",
                "name": "Luke Skywalker",
                "skin_color": "Fair",
            },
        }
        character = Character.objects.create(**character_data)
        character.films.add(film)

        self.assertIn(character, film.characters.all())
        self.assertIn(film, character.films.all())


class StarshipModelTest(TestCase):
    """Test cases for the Starship model"""

    def setUp(self) -> None:
        """Set up test data"""
        self.starship_data = {
            "name": "Death Star",
            "swapi_url": "https://swapi.dev/api/starships/9/",
            "data": {
                "MGLT": "10 MGLT",
                "cargo_capacity": "1000000000000",
                "consumables": "3 years",
                "cost_in_credits": "1000000000000",
                "crew": "342953",
                "hyperdrive_rating": "4.0",
                "length": "120000",
                "manufacturer": "Imperial Department of Military Research, Sienar Fleet Systems",
                "max_atmosphering_speed": "n/a",
                "model": "DS-1 Orbital Battle Station",
                "name": "Death Star",
                "passengers": "843342",
                "starship_class": "Deep Space Mobile Battlestation",
            },
        }

    def test_create_starship(self) -> None:
        """Test creating a starship with SWAPI data"""
        starship = Starship.objects.create(**self.starship_data)

        self.assertEqual(starship.name, "Death Star")
        self.assertEqual(starship.swapi_url, "https://swapi.dev/api/starships/9/")
        self.assertEqual(starship.data["model"], "DS-1 Orbital Battle Station")
        self.assertEqual(starship.data["starship_class"], "Deep Space Mobile Battlestation")
        self.assertEqual(str(starship), "Death Star")

    def test_starship_unique_swapi_url(self) -> None:
        """Test that SWAPI URL must be unique"""
        Starship.objects.create(**self.starship_data)

        with self.assertRaises(IntegrityError):
            Starship.objects.create(**self.starship_data)

    def test_starship_str_representation(self) -> None:
        """Test string representation of starship"""
        starship = Starship.objects.create(**self.starship_data)
        self.assertEqual(str(starship), "Death Star")

    def test_starship_json_data_access(self) -> None:
        """Test accessing JSON data fields"""
        starship = Starship.objects.create(**self.starship_data)

        self.assertEqual(starship.data["crew"], "342953")
        self.assertEqual(starship.data["passengers"], "843342")
        self.assertEqual(starship.data["hyperdrive_rating"], "4.0")

    def test_starship_characters_relationship(self) -> None:
        """Test many-to-many relationship with characters"""
        starship = Starship.objects.create(**self.starship_data)

        character_data = {
            "name": "Darth Vader",
            "swapi_url": "https://swapi.dev/api/people/4/",
            "data": {
                "name": "Darth Vader",
                "birth_year": "41.9BBY",
                "eye_color": "yellow",
                "gender": "male",
                "hair_color": "none",
                "height": "202",
                "mass": "136",
                "skin_color": "white",
            },
        }
        character = Character.objects.create(**character_data)
        character.starships.add(starship)

        self.assertIn(character, starship.characters.all())
        self.assertIn(starship, character.starships.all())


class CharacterModelTest(TestCase):
    """Test cases for the Character model"""

    def setUp(self) -> None:
        """Set up test data"""
        self.film = Film.objects.create(
            title="A New Hope", swapi_url="https://swapi.dev/api/films/1/", release_date=date(1977, 5, 25)
        )

        self.starship = Starship.objects.create(
            name="X-wing",
            swapi_url="https://swapi.dev/api/starships/12/",
            data={
                "name": "X-wing",
                "model": "T-65 X-wing",
                "manufacturer": "Incom Corporation",
                "starship_class": "Starfighter",
            },
        )

        self.character_data = {
            "name": "Luke Skywalker",
            "swapi_url": "https://swapi.dev/api/people/1/",
            "data": {
                "birth_year": "19 BBY",
                "eye_color": "Blue",
                "gender": "Male",
                "hair_color": "Blond",
                "height": "172",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "mass": "77",
                "name": "Luke Skywalker",
                "skin_color": "Fair",
                "created": "2014-12-09T13:50:51.644000Z",
                "edited": "2014-12-10T13:52:43.172000Z",
                "films": [
                    "https://swapi.dev/api/films/1/",
                ],
                "species": ["https://swapi.dev/api/species/1/"],
                "starships": [
                    "https://swapi.dev/api/starships/12/",
                ],
                "url": "https://swapi.dev/api/people/1/",
                "vehicles": ["https://swapi.dev/api/vehicles/14/"],
            },
        }

    def test_create_character(self) -> None:
        """Test creating a character with SWAPI data"""
        character = Character.objects.create(**self.character_data)

        self.assertEqual(character.name, "Luke Skywalker")
        self.assertEqual(character.swapi_url, "https://swapi.dev/api/people/1/")
        self.assertEqual(character.data["birth_year"], "19 BBY")
        self.assertEqual(character.data["eye_color"], "Blue")
        self.assertEqual(character.data["gender"], "Male")
        self.assertEqual(str(character), "Luke Skywalker")

    def test_character_unique_swapi_url(self) -> None:
        """Test that SWAPI URL must be unique"""
        Character.objects.create(**self.character_data)

        with self.assertRaises(IntegrityError):
            Character.objects.create(**self.character_data)

    def test_character_str_representation(self) -> None:
        """Test string representation of character"""
        character = Character.objects.create(**self.character_data)
        self.assertEqual(str(character), "Luke Skywalker")

    def test_character_json_data_access(self) -> None:
        """Test accessing JSON data fields"""
        character = Character.objects.create(**self.character_data)

        self.assertEqual(character.data["height"], "172")
        self.assertEqual(character.data["mass"], "77")
        self.assertEqual(character.data["hair_color"], "Blond")
        self.assertEqual(character.data["skin_color"], "Fair")

    def test_character_films_relationship(self) -> None:
        """Test many-to-many relationship with films"""
        character = Character.objects.create(**self.character_data)
        character.films.add(self.film)

        self.assertIn(self.film, character.films.all())
        self.assertIn(character, self.film.characters.all())

    def test_character_starships_relationship(self) -> None:
        """Test many-to-many relationship with starships"""
        character = Character.objects.create(**self.character_data)
        character.starships.add(self.starship)

        self.assertIn(self.starship, character.starships.all())
        self.assertIn(character, self.starship.characters.all())

    def test_character_multiple_relationships(self) -> None:
        """Test character with multiple films and starships"""
        character = Character.objects.create(**self.character_data)

        # Add another film
        film2 = Film.objects.create(
            title="The Empire Strikes Back", swapi_url="https://swapi.dev/api/films/2/", release_date=date(1980, 5, 21)
        )

        # Add another starship
        starship2 = Starship.objects.create(
            name="Imperial shuttle",
            swapi_url="https://swapi.dev/api/starships/22/",
            data={"name": "Imperial shuttle", "model": "Lambda-class T-4a shuttle"},
        )

        character.films.add(self.film, film2)
        character.starships.add(self.starship, starship2)

        self.assertEqual(character.films.count(), 2)
        self.assertEqual(character.starships.count(), 2)
        self.assertIn(self.film, character.films.all())
        self.assertIn(film2, character.films.all())
        self.assertIn(self.starship, character.starships.all())
        self.assertIn(starship2, character.starships.all())

    def test_character_with_swapi_url_references(self) -> None:
        """Test character data contains proper SWAPI URL references"""
        character = Character.objects.create(**self.character_data)

        # Test that SWAPI URL references are preserved in data
        self.assertIn("https://swapi.dev/api/films/1/", character.data["films"])
        self.assertIn("https://swapi.dev/api/starships/12/", character.data["starships"])
        self.assertEqual(character.data["homeworld"], "https://swapi.dev/api/planets/1/")


class VoteModelTest(TestCase):
    """Test cases for the Vote model"""

    def setUp(self) -> None:
        """Set up test data"""
        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", first_name="Test", last_name="User", password="testpass123"
        )

        self.character = Character.objects.create(
            name="Luke Skywalker",
            swapi_url="https://swapi.dev/api/people/1/",
            data={"name": "Luke Skywalker", "birth_year": "19 BBY"},
        )

        self.film = Film.objects.create(
            title="A New Hope", swapi_url="https://swapi.dev/api/films/1/", release_date=date(1977, 5, 25)
        )

        self.starship = Starship.objects.create(
            name="Death Star",
            swapi_url="https://swapi.dev/api/starships/9/",
            data={"name": "Death Star", "model": "DS-1 Orbital Battle Station"},
        )

    def test_create_character_vote(self) -> None:
        """Test creating a vote for a character"""
        vote = Vote.objects.create(user=self.user, character=self.character)

        self.assertEqual(vote.user, self.user)
        self.assertEqual(vote.character, self.character)
        self.assertIsNone(vote.film)
        self.assertIsNone(vote.starship)
        self.assertIsNotNone(vote.created_at)

    def test_create_film_vote(self) -> None:
        """Test creating a vote for a film"""
        vote = Vote.objects.create(user=self.user, film=self.film)

        self.assertEqual(vote.user, self.user)
        self.assertEqual(vote.film, self.film)
        self.assertIsNone(vote.character)
        self.assertIsNone(vote.starship)
        self.assertIsNotNone(vote.created_at)

    def test_create_starship_vote(self) -> None:
        """Test creating a vote for a starship"""
        vote = Vote.objects.create(user=self.user, starship=self.starship)

        self.assertEqual(vote.user, self.user)
        self.assertEqual(vote.starship, self.starship)
        self.assertIsNone(vote.character)
        self.assertIsNone(vote.film)
        self.assertIsNotNone(vote.created_at)

    def test_unique_character_vote_constraint(self) -> None:
        """Test that a user cannot vote twice for the same character"""
        Vote.objects.create(user=self.user, character=self.character)

        with self.assertRaises(IntegrityError):
            Vote.objects.create(user=self.user, character=self.character)

    def test_unique_film_vote_constraint(self) -> None:
        """Test that a user cannot vote twice for the same film"""
        Vote.objects.create(user=self.user, film=self.film)

        with self.assertRaises(IntegrityError):
            Vote.objects.create(user=self.user, film=self.film)

    def test_unique_starship_vote_constraint(self) -> None:
        """Test that a user cannot vote twice for the same starship"""
        Vote.objects.create(user=self.user, starship=self.starship)

        with self.assertRaises(IntegrityError):
            Vote.objects.create(user=self.user, starship=self.starship)

    def test_user_can_vote_for_different_items(self) -> None:
        """Test that a user can vote for different characters, films, and starships"""
        character_vote = Vote.objects.create(user=self.user, character=self.character)
        film_vote = Vote.objects.create(user=self.user, film=self.film)
        starship_vote = Vote.objects.create(user=self.user, starship=self.starship)

        self.assertEqual(Vote.objects.filter(user=self.user).count(), 3)
        self.assertNotEqual(character_vote.id, film_vote.id)
        self.assertNotEqual(character_vote.id, starship_vote.id)
        self.assertNotEqual(film_vote.id, starship_vote.id)

    def test_different_users_can_vote_for_same_item(self) -> None:
        """Test that different users can vote for the same item"""
        user2 = User.objects.create_user(
            email="test2@example.com",
            username="testuser2",
            first_name="Test2",
            last_name="User2",
            password="testpass123",
        )

        vote1 = Vote.objects.create(user=self.user, character=self.character)
        vote2 = Vote.objects.create(user=user2, character=self.character)

        self.assertEqual(Vote.objects.filter(character=self.character).count(), 2)
        self.assertNotEqual(vote1.user, vote2.user)
        self.assertEqual(vote1.character, vote2.character)

    def test_vote_cascade_deletion_user(self) -> None:
        """Test that votes are deleted when user is deleted"""
        Vote.objects.create(user=self.user, character=self.character)
        Vote.objects.create(user=self.user, film=self.film)

        self.assertEqual(Vote.objects.filter(user=self.user).count(), 2)

        self.user.delete()

        self.assertEqual(Vote.objects.count(), 0)

    def test_vote_cascade_deletion_character(self) -> None:
        """Test that votes are deleted when character is deleted"""
        Vote.objects.create(user=self.user, character=self.character)

        self.assertEqual(Vote.objects.count(), 1)

        self.character.delete()

        self.assertEqual(Vote.objects.count(), 0)

    def test_vote_cascade_deletion_film(self) -> None:
        """Test that votes are deleted when film is deleted"""
        Vote.objects.create(user=self.user, film=self.film)

        self.assertEqual(Vote.objects.count(), 1)

        self.film.delete()

        self.assertEqual(Vote.objects.count(), 0)

    def test_vote_cascade_deletion_starship(self) -> None:
        """Test that votes are deleted when starship is deleted"""
        Vote.objects.create(user=self.user, starship=self.starship)

        self.assertEqual(Vote.objects.count(), 1)

        self.starship.delete()

        self.assertEqual(Vote.objects.count(), 0)


class ModelRelationshipIntegrationTest(TestCase):
    """Integration tests for model relationships"""

    def setUp(self) -> None:
        """Set up comprehensive test data"""
        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", first_name="Test", last_name="User", password="testpass123"
        )

        # Create a film
        self.film = Film.objects.create(
            title="A New Hope", swapi_url="https://swapi.dev/api/films/1/", release_date=date(1977, 5, 25)
        )

        # Create starships
        self.x_wing = Starship.objects.create(
            name="X-wing",
            swapi_url="https://swapi.dev/api/starships/12/",
            data={
                "name": "X-wing",
                "model": "T-65 X-wing",
                "starship_class": "Starfighter",
            },
        )

        self.millennium_falcon = Starship.objects.create(
            name="Millennium Falcon",
            swapi_url="https://swapi.dev/api/starships/10/",
            data={
                "name": "Millennium Falcon",
                "model": "YT-1300 light freighter",
                "starship_class": "Light freighter",
            },
        )

        # Create character with full SWAPI data structure
        self.luke = Character.objects.create(
            name="Luke Skywalker",
            swapi_url="https://swapi.dev/api/people/1/",
            data={
                "birth_year": "19 BBY",
                "eye_color": "Blue",
                "films": [
                    "https://swapi.dev/api/films/1/",
                ],
                "gender": "Male",
                "hair_color": "Blond",
                "height": "172",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "mass": "77",
                "name": "Luke Skywalker",
                "skin_color": "Fair",
                "species": ["https://swapi.dev/api/species/1/"],
                "starships": [
                    "https://swapi.dev/api/starships/12/",
                ],
                "url": "https://swapi.dev/api/people/1/",
                "vehicles": ["https://swapi.dev/api/vehicles/14/"],
            },
        )

    def test_complete_swapi_character_relationships(self) -> None:
        """Test creating a character with all SWAPI relationships"""
        # Add relationships
        self.luke.films.add(self.film)
        self.luke.starships.add(self.x_wing)

        # Test that relationships work both ways
        self.assertIn(self.luke, self.film.characters.all())
        self.assertIn(self.luke, self.x_wing.characters.all())
        self.assertIn(self.film, self.luke.films.all())
        self.assertIn(self.x_wing, self.luke.starships.all())

        # Test JSON data integrity
        self.assertEqual(self.luke.data["name"], "Luke Skywalker")
        self.assertIn("https://swapi.dev/api/films/1/", self.luke.data["films"])
        self.assertIn("https://swapi.dev/api/starships/12/", self.luke.data["starships"])

    def test_multiple_character_film_starship_relationships(self) -> None:
        """Test complex relationships between multiple characters, films, and starships"""
        # Create another character
        han = Character.objects.create(
            name="Han Solo",
            swapi_url="https://swapi.dev/api/people/14/",
            data={
                "name": "Han Solo",
                "birth_year": "29BBY",
                "gender": "male",
                "height": "180",
                "mass": "80",
                "hair_color": "brown",
                "eye_color": "brown",
                "skin_color": "fair",
            },
        )

        # Add relationships
        self.luke.films.add(self.film)
        han.films.add(self.film)

        self.luke.starships.add(self.x_wing)
        han.starships.add(self.millennium_falcon)

        # Test film has multiple characters
        self.assertEqual(self.film.characters.count(), 2)
        self.assertIn(self.luke, self.film.characters.all())
        self.assertIn(han, self.film.characters.all())

        # Test characters have correct starships
        self.assertIn(self.x_wing, self.luke.starships.all())
        self.assertIn(self.millennium_falcon, han.starships.all())
        self.assertNotIn(self.millennium_falcon, self.luke.starships.all())
        self.assertNotIn(self.x_wing, han.starships.all())

    def test_voting_on_related_objects(self) -> None:
        """Test voting functionality with all related objects"""
        # Set up relationships
        self.luke.films.add(self.film)
        self.luke.starships.add(self.x_wing)

        # Create votes
        character_vote = Vote.objects.create(user=self.user, character=self.luke)
        film_vote = Vote.objects.create(user=self.user, film=self.film)
        starship_vote = Vote.objects.create(user=self.user, starship=self.x_wing)

        # Verify votes were created
        self.assertEqual(Vote.objects.count(), 3)

        # Test that we can access the voted objects and their relationships
        self.assertEqual(character_vote.character.name, "Luke Skywalker")
        self.assertIn(self.film, character_vote.character.films.all())
        self.assertIn(self.x_wing, character_vote.character.starships.all())

        self.assertEqual(film_vote.film.title, "A New Hope")
        self.assertIn(self.luke, film_vote.film.characters.all())

        self.assertEqual(starship_vote.starship.name, "X-wing")
        self.assertIn(self.luke, starship_vote.starship.characters.all())

    def test_swapi_data_structure_integrity(self) -> None:
        """Test that SWAPI data structure is properly maintained"""
        # Test Film data (if we had stored full SWAPI data)
        self.assertEqual(self.film.title, "A New Hope")
        self.assertEqual(self.film.swapi_url, "https://swapi.dev/api/films/1/")

        # Test Starship data structure
        self.assertEqual(self.x_wing.data["model"], "T-65 X-wing")
        self.assertEqual(self.x_wing.data["starship_class"], "Starfighter")

        # Test Character data structure with all SWAPI fields
        luke_data = self.luke.data
        expected_fields = [
            "birth_year",
            "eye_color",
            "films",
            "gender",
            "hair_color",
            "height",
            "homeworld",
            "mass",
            "name",
            "skin_color",
            "species",
            "starships",
            "url",
            "vehicles",
        ]

        for field in expected_fields:
            self.assertIn(field, luke_data)

        # Test specific data values
        self.assertEqual(luke_data["birth_year"], "19 BBY")
        self.assertEqual(luke_data["eye_color"], "Blue")
        self.assertEqual(luke_data["gender"], "Male")
        self.assertEqual(luke_data["height"], "172")
        self.assertEqual(luke_data["mass"], "77")
