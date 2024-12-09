from models.player import Player
from utils.db import players_table


class PlayerManager:

    def create_player(self):
        last_name = input("Enter last name: ")
        first_name = input("Enter first name: ")
        birth_date = input("Enter birth date: ")
        identifier = input("Enter identifier: ")
        player = Player(
            last_name,
            first_name,
            birth_date,
            identifier,
        )
        players_table.insert(player.to_dict())

    def run(self):
        while True:
            print("1. Creer un joueur")
            print("q. Quitter")
            choice = input("Votre choix: ")
            if choice == "1":
                self.create_player()
            elif choice == "q":
                break
