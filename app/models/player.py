"""Player module."""

from tinydb import TinyDB
from faker import Faker
from random import randint, choice

from .db import DB


class Player:
    """Class of a player with his full name, birth's date, sex, rank and id."""

    db = TinyDB("db.json")
    table = db.table("players")

    def __init__(self, name: str, birth: str, sex: str, rank: int, score=0, id=None):
        """All the attributes of a player."""
        self.name = name
        self.birth = birth
        self.sex = sex
        self.rank = rank
        self.id = id
        self.score = score

    def auto_init():
        """All the attributes of a player."""
        fake = Faker()
        sex = choice(["f", "m", "o"])
        return Player(fake.name(), fake.date(), sex, randint(0, 100))

    def print_details(self):
        """Return the attribute of the player when print is use."""
        return f"{self.name} \tDate de naissance: \
            {self.birth} \tSexe: {self.sex} \tRang: {self.rank}"

    def __repr__(self):
        """Repr."""
        return str(self)

    def __str__(self):
        """Get the rank of the player."""
        return f"{self.id} {self.name}\t {self.rank}"

    def serialized(self):
        """Return the player serialized."""
        serialized = self.__dict__.copy()
        serialized.pop("id")
        return serialized

    @classmethod
    def deserialized(cls, player_info):
        """Get a dictionnary and return a player obj."""
        player = Player(**player_info)
        player.id = player_info.doc_id
        return player

    def save(self):
        """Save the player in the db."""
        DB.save(self)

    def get(id):
        """Get the player from the db with his id."""
        return DB.get(Player, id)

    @classmethod
    def print_all(cls):
        """Print all the player in the db."""
        all = cls.table.all()
        for obj_serialized in all:
            obj_desirialized = cls.deserialized(obj_serialized)
            print(obj_desirialized)


if __name__ == "__main__":
    player = Player.auto_init()

    id = player.id

    DB.save(player)
    player1 = DB.get(Player, 1)

    player1.rank = 12
    DB.save(player1)

    DB.print_all(Player)
