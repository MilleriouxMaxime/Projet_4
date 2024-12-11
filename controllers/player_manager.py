from controllers.tournament_manager import input_choice
from models.player import Player
from utils.db import players_table


class PlayerManager:

    def create_player(self):
        last_name = input("Saisissez le nom du joueur: ")
        first_name = input("Saisissez le prénom du joueur: ")
        birth_date = input("Saisissez la date de naissance du joueur: ")
        identifier = input("Saisissez l'ID du joueur: ")
        player = Player(
            last_name,
            first_name,
            birth_date,
            identifier,
        )
        players_table.insert(player.to_dict())

    # TODO : Fonction pour supprimer un joueur de la base de données
    def run(self):
        while True:
            print("\n1. Créer un joueur")
            print("2. Supprimer un joueur")
            print("q. Quitter")
            choice = input_choice("Votre choix: ")
            if choice == "1":
                self.create_player()
            elif choice == "2":
                self.remove_player()
            elif choice == "q":
                break
