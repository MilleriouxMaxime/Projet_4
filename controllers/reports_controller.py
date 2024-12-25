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
        for player in sorted(players, key=lambda p: p["last_name"]):
            print(
                f"{player['last_name']} {player['first_name']} - {player['identifier']}"
            )

    def tournaments_list(self):
        """
        Afficher la liste des tournois par ordre alphabétique
        """
        self.view.display_rapport_title("Liste des tournois")
        tournaments = db_tournaments.all()
        for tournament in sorted(tournaments, key=lambda t: t["name"]):
            print(f"{tournament['name']} - Lieu : {tournament['place']}")

    def get_tournament_name_and_date(self):
        """
        Afficher le nom et la date d'un tournoi
        """
        while True:
            self.view.display_rapport_title("Nom et Dates d'un tournoi")

            tournaments = db_tournaments.all()
            for index, tournament in enumerate(tournaments):
                print(f"{index + 1}. {tournament['name']}")
            print("q. Quitter")

            tournament_index = input_choice("Votre choix: ")

            if tournament_index == "q":
                return

            tournament_name = tournaments[int(tournament_index) - 1]["name"]
            tournament = db_tournaments.get(Query().name == tournament_name)

            print(f"\nNom du tournoi : {tournament['name']}")
            print(f"Date de début du tournoi : {tournament['start_date']}")
            print(f"Date de fin du tournoi : {tournament['end_date']}")

    def list_of_players_in_tournament(self):
        """
        Afficher la liste des ID de joueurs d'un tournoi
        """
        self.view.display_rapport_title("Liste des joueurs d'un tournoi")
        tournaments = db_tournaments.all()

        for index, tournament in enumerate(tournaments):
            print(f"{index + 1}. {tournament['name']}")
        print("q. Quitter")

        tournament_index = input_choice("Votre choix: ")

        if tournament_index == "q":
            return

        tournament_name = tournaments[int(tournament_index) - 1]["name"]
        tournament = db_tournaments.get(Query().name == tournament_name)
        print()
        # print player list propretly
        for player_id in tournament["players_list"]:
            player = db_players.get(Query().identifier == player_id)
            print(
                f"{player['last_name']} {player['first_name']} - {player['identifier']}"
            )

    def list_of_rounds_and_matches_in_tournament(self):
        """
        Afficher la liste des tours et matchs d'un tournoi
        """
        self.view.display_rapport_title("Liste des tours et matchs d'un tournoi")
        tournaments = db_tournaments.all()

        for index, tournament in enumerate(tournaments):
            print(f"{index + 1}. {tournament['name']}")
        print("q. Quitter")

        tournament_index = input_choice("Votre choix: ")

        if tournament_index == "q":
            return

        tournament_name = tournaments[int(tournament_index) - 1]["name"]
        tournament = db_tournaments.get(Query().name == tournament_name)

        for round_ in tournament["rounds_list"]:
            print(f"\n{round_['name']}\n")
            for match in round_["matches_list"]:
                player1 = db_players.get(Query().identifier == match[0][0])
                player2 = db_players.get(Query().identifier == match[1][0])
                print(
                    f"{player1['last_name']} {player1['first_name']} - {player2['last_name']} {player2['first_name']}"
                )

    def run(self):
        """
        Gestion des rapports
        """
        while True:
            self.view.display_rapport_title("Rapports")
            print("1. Liste des joueurs")
            print("2. Liste des tournois")
            print("3. Nom et date d'un tournoi")
            print("4. Liste des joueurs d'un tournoi")
            print("5. Liste des tours et matchs d'un tournoi")
            print("q. Quitter")
            choice = input_choice("Votre choix: ")
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
