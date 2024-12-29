from controllers.player_controller import PlayerController
from controllers.reports_controller import ReportsController
from controllers.tournament_controller import TournamentController
from views.base_view import BaseView
from views.player_view import PlayerView
from views.reports_view import ReportsView
from views.tournament_view import TournamentView


class MenuController:
    def __init__(self, view: BaseView):
        self.view = view

    def run(self):
        while True:
            choice = self.view.ask_for_options(
                [
                    "Gestion des tournois",
                    "Gestion des joueurs",
                    "Rapports",
                ]
            )
            if choice == "1":
                tournament_view = TournamentView()
                tournament_manager = TournamentController(tournament_view)
                tournament_manager.run()
            elif choice == "2":
                player_view = PlayerView()
                player_manager = PlayerController(player_view)
                player_manager.run()
            elif choice == "3":
                reports_view = ReportsView()
                reports_manager = ReportsController(reports_view)
                reports_manager.run()
            elif choice == "q":
                break
            else:
                self.view.display_error(
                    "Attention, votre choix doit faire parti de la liste ci-dessous."
                )
