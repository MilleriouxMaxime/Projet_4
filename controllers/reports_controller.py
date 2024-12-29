from tinydb import Query

from utils.db import db_players, db_tournaments
from views.base_view import BaseView


class ReportsController:
    def __init__(self, view: BaseView):
        self.view = view

    def list_of_players(self):
        """
        Afficher la liste des joueurs par ordre alphabétique
        """
        self.view.display_rapport_title("Liste des joueurs")
        players = db_players.all()
        players_list = []
        for player in sorted(players, key=lambda p: p["last_name"]):
            players_list.append(
                f"{player['last_name']} {player['first_name']} - {player['identifier']}"
            )
        self.view.display_list(players_list)

    def tournaments_list(self):
        """
        Afficher la liste des tournois par ordre alphabétique
        """
        self.view.display_rapport_title("Liste des tournois")
        tournaments = db_tournaments.all()
        tournaments_list = []
        for tournament in tournaments:
            tournaments_list.append(
                f"{tournament['name']} - Lieu : {tournament['place']}"
            )
        self.view.display_list(sorted(tournaments_list))

    def get_tournament_name_and_date(self):
        """
        Afficher le nom et la date d'un tournoi
        """
        while True:
            self.view.display_rapport_title("Nom et Dates d'un tournoi")

            tournaments = db_tournaments.all()
            tournament_names = [tournament["name"] for tournament in tournaments]
            tournament_index = self.view.ask_for_options(tournament_names)

            if tournament_index == "q":
                return

            tournament_name = tournaments[int(tournament_index) - 1]["name"]
            tournament = db_tournaments.get(Query().name == tournament_name)

            self.view.display_list(
                [
                    f"Nom du tournoi : {tournament['name']}",
                    f"Date de début du tournoi : {tournament['start_date']}",
                    f"Date de fin du tournoi : {tournament['end_date']}",
                ]
            )

    def list_of_players_in_tournament(self):
        """
        Afficher la liste des ID de joueurs d'un tournoi
        """
        self.view.display_rapport_title("Liste des joueurs d'un tournoi")

        tournaments = db_tournaments.all()
        tournament_names = [tournament["name"] for tournament in tournaments]
        tournament_index = self.view.ask_for_options(tournament_names)

        if tournament_index == "q":
            return

        tournament_name = tournaments[int(tournament_index) - 1]["name"]
        tournament = db_tournaments.get(Query().name == tournament_name)

        players_list = []
        for player_id in tournament["players_list"]:
            player = db_players.get(Query().identifier == player_id)
            players_list.append(
                f"{player['last_name']} {player['first_name']} - {player['identifier']}"
            )

        self.view.display_list(sorted(players_list))

    def list_of_rounds_and_matches_in_tournament(self):
        """
        Afficher la liste des tours et matchs d'un tournoi
        """
        self.view.display_rapport_title("Liste des tours et matchs d'un tournoi")

        tournaments = db_tournaments.all()
        tournament_names = [tournament["name"] for tournament in tournaments]
        tournament_index = self.view.ask_for_options(tournament_names)

        if tournament_index == "q":
            return

        tournament_name = tournaments[int(tournament_index) - 1]["name"]
        tournament = db_tournaments.get(Query().name == tournament_name)

        rounds_list = []

        for round_ in tournament["rounds_list"]:
            rounds_list.append(f"\n{round_['name']}\n")
            for match in round_["matches_list"]:
                player1 = db_players.get(Query().identifier == match[0][0])
                player2 = db_players.get(Query().identifier == match[1][0])
                rounds_list.append(
                    f"{player1['last_name']} {player1['first_name']} - {player2['last_name']} {player2['first_name']}"
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
