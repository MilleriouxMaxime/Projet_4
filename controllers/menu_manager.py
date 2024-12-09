from controllers.tournament_manager import TournamentManager
from controllers.player_manager import PlayerManager


class MenuManager:

    def run(self):
        while True:
            print("1. Gestion des tournois")
            print("2. Gestion des joueurs")
            print("q. Quitter")
            choice = input("Votre choix: ")

            if choice == "1":
                tournament_manager = TournamentManager()
                tournament_manager.run()
            elif choice == "2":
                player_manager = PlayerManager()
                player_manager.run()
            elif choice == "q":
                break
