from colorama import Fore, Style

from controllers.player_manager import PlayerManager
from controllers.tournament_manager import TournamentManager, input_choice, print_error


class MenuManager:

    def run(self):
        while True:
            print("\n1. Gestion des tournois")
            print("2. Gestion des joueurs")
            print("q. Quitter")
            choice = input_choice("Votre choix: ")

            if choice == "1":
                tournament_manager = TournamentManager()
                tournament_manager.run()
            elif choice == "2":
                player_manager = PlayerManager()
                player_manager.run()
            elif choice == "q":
                break
            else:
                print_error(
                    "Attention, votre choix doit faire parti de la liste ci-dessous."
                )
