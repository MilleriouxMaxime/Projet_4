from utils.db import db_manager
from views.base_view import BaseView


class ReportsController:
    def __init__(self, view: BaseView):
        self.view = view

    def get_tournament(self):
        while True:
            tournaments = db_manager.get_all_tournaments()
            tournament_names = [tournament["name"] for tournament in tournaments]
            tournament_index = self.view.ask_for_options(tournament_names)

            if tournament_index == "q":
                return None

            tournament_index = int(tournament_index)

            if tournament_index not in range(1, len(tournament_names) + 1):
                self.view.display_error("Veuillez choisir un tournoi dans la liste !")
                continue

            tournament = tournaments[tournament_index - 1]
            return tournament

    def list_of_players(self):
        """
        Afficher la liste des joueurs par ordre alphabétique
        """
        self.view.display_rapport_title("Liste des joueurs")
        players = db_manager.get_all_players()
        players_list = []
        for player in sorted(players, key=lambda p: p["last_name"]):
            players_list.append(
                f"{player["last_name"]} {player["first_name"]} - {player["identifier"]}"
            )
        self.view.display_list(players_list)

    def tournaments_list(self):
        """
        Afficher la liste des tournois par ordre alphabétique
        """
        self.view.display_rapport_title("Liste des tournois")
        tournaments = db_manager.get_all_tournaments()
        tournaments_list = []
        for tournament in tournaments:
            tournaments_list.append(
                f"{tournament["name"]} /// Status : {tournament["status"]} /// Lieu : {tournament["place"]}"
            )
        self.view.display_list(sorted(tournaments_list))

    def get_tournament_name_and_date(self):
        """
        Afficher le nom et la date d'un tournoi
        """
        self.view.display_rapport_title("Nom et Dates d'un tournoi")

        tournament = self.get_tournament()
        if tournament is None:
            return
        self.view.display_list(
            [
                f"Nom du tournoi : {tournament["name"]}",
                f"Date de début du tournoi : {tournament["start_date"]}",
                f"Date de fin du tournoi : {tournament["end_date"]}",
            ]
        )

    def list_of_players_in_tournament(self):
        """
        Afficher la liste des ID de joueurs d'un tournoi
        """
        self.view.display_rapport_title("Liste des joueurs d'un tournoi")

        tournament = self.get_tournament()
        if tournament is None:
            return

        players_list = []
        for player_id in tournament["players_list"]:
            player = db_manager.get_player(player_id)
            players_list.append(
                f"{player["last_name"]} {player["first_name"]} - {player["identifier"]}"
            )

        self.view.display_list(sorted(players_list))

    def list_of_rounds_and_matches_in_tournament(self):
        """
        Afficher la liste des tours et matchs d'un tournoi
        """
        self.view.display_rapport_title("Liste des tours et matchs d'un tournoi")

        tournament = self.get_tournament()
        if tournament is None:
            return

        rounds_list = []

        for round_ in tournament["rounds_list"]:
            rounds_list.append(f"\n{round_['name']}\n")
            for match in round_["matches_list"]:
                player1 = db_manager.get_player(match[0][0])
                player2 = db_manager.get_player(match[1][0])
                rounds_list.append(
                    f"{player1["last_name"]} {player1["first_name"]} - {player2["last_name"]} {player2["first_name"]}"
                )

        self.view.display_list(rounds_list)

    def run(self):
        """
        Gestion des rapports
        """
        while True:
            self.view.display_rapport_title("Rapports")
            choice = self.view.ask_for_options(
                [
                    "Liste des joueurs",
                    "Liste des tournois",
                    "Nom et date d'un tournoi",
                    "Liste des joueurs d'un tournoi",
                    "Liste des tours et matchs d'un tournoi",
                ]
            )

            if choice == "1":
                self.list_of_players()
            elif choice == "2":
                self.tournaments_list()
            elif choice == "3":
                self.get_tournament_name_and_date()
            elif choice == "4":
                self.list_of_players_in_tournament()
            elif choice == "5":
                self.list_of_rounds_and_matches_in_tournament()
            elif choice == "q":
                break
