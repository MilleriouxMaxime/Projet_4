from tinydb import Query, TinyDB

from models.player import Player
from models.tournament import Tournament
from utils.config import config


class TinyDBManager:
    def __init__(self):
        self.db_tournaments = TinyDB("db_tournaments.json")
        self.db_players = TinyDB("db_players.json")

    def get_all_players(self):
        return self.db_players.all()

    def get_all_tournaments(self):
        return self.db_tournaments.all()

    def get_player(self, identifier):
        return self.db_players.get(Query().identifier == identifier)

    def get_tournament(self, name):
        return self.db_tournaments.get(Query().name == name)

    def update_tournament(self, tournament):
        self.db_tournaments.update(tournament, Query().name == tournament["name"])

    def insert_tournament(self, tournament: Tournament):
        self.db_tournaments.insert(tournament.to_dict())

    def insert_player(self, player: Player):
        self.db_players.insert(player.to_dict())

    def remove_player(self, identifier):
        self.db_players.remove(Query().identifier == identifier)


if config["database"] == "tinydb":
    db_manager = TinyDBManager()
# elif config["database"] == "postgresql":
#    db_manager = PostgreSQLManager()
else:
    raise ValueError(f"Unknown database type: {config['database']}")
