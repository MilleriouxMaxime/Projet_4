from colorama import Fore, Style

from controllers.player_controller import PlayerController
from controllers.reports_controller import ReportsController
from controllers.tournament_controller import (
    TournamentController,
    input_choice,
    print_error,
)


class MenuController:

    def run(self):
        while True:
            print("\n1. Gestion des tournois")
            print("2. Gestion des joueurs")
            print("3. Rapports")
            print("q. Quitter")
            choice = input_choice("Votre choix: ")

            if choice == "1":
                tournament_manager = TournamentController()
                tournament_manager.run()
            elif choice == "2":
                player_manager = PlayerController()
                player_manager.run()
            elif choice == "3":
                reports_manager = ReportsController()
                reports_manager.run()
            elif choice == "q":
                break
            else:
                print_error(
                    "Attention, votre choix doit faire parti de la liste ci-dessous."
                )
