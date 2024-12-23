import random
from collections import defaultdict
from datetime import datetime

from colorama import Fore, Style
from tinydb import Query

from controllers.player_controller import ask_for_input
from models.round import Match, Round
from models.tournament import Tournament
from utils.db import db_players, db_tournaments
from utils.formating import (
    input_choice,
    print_error,
    print_success,
    print_tornament_title,
)


class TournamentController:

    def create_tournament(self):
        """
        Création d'un tournoi
        """
        print_tornament_title("Création d'un tournoi")
        try:
            name = ask_for_input(
                "Saisissez le nom du tournoi (ou tapez 'q' pour quitter la création de tournoi): ",
                None,
            )
            place = ask_for_input(
                "Saisissez le lieu du tournoi (ou tapez 'q' pour quitter la création de tournoi): ",
                None,
            )
            start_date = ask_for_input(
                "Saisissez la date de début du tournoi (ou tapez 'q' pour quitter la création de tournoi): ",
                "date",
            )
            end_date = ask_for_input(
                "Saisissez la date de fin du tournoi (ou tapez 'q' pour quitter la création de tournoi): ",
                "date",
            )
            total_round_number = ask_for_input(
                "Saisissez le nombre total de tours du tournoi (ou tapez 'q' pour quitter la création de tournoi): ",
                "round",
            )
            description = ask_for_input(
                "Saisissez la description du tournoi (ou tapez 'q' pour quitter la création de tournoi): ",
                None,
            )
        except KeyboardInterrupt:
            return

        tournament = Tournament(
            name,
            place,
            start_date,
            end_date,
            0,
            [],
            [],
            description,
            total_round_number,
        )

        db_tournaments.insert(tournament.to_dict())

        print_success(f"Tournament '{tournament.name}' a été créé avec succès !")

    def subscribe_players_to_tournament(self, tournament):
        """
        Inscription d'un joueur à un tournoi en utilisant son ID pour le retrouver dans la base de données
        """
        try:
            player_id = ask_for_input(
                "Saisissez l'ID du joueur à inscrire (ou tapez 'q' pour annuler la saisie.): ",
                "identifier",
            )
        except KeyboardInterrupt:
            return

        player = db_players.get(Query().identifier == player_id)

        if player is None:
            print_error(f"Joueur '{player_id}' n'existe pas !")
            return

        tournament_name = tournament["name"]
        tournament["players_list"].append(player_id)
        db_tournaments.update(tournament, Query().name == tournament_name)

        print_success(
            f"Player '{player_id}' subscribed to tournament '{tournament_name}' successfully!"
        )

    def unsubscribe_players_from_tournament(self, tournament):
        """
        Désinscription d'un joueur à un tournoi en utilisant son ID pour le retrouver dans la base de données
        """

        try:
            player_id = ask_for_input(
                "Saisissez l'ID du joueur à inscrire (ou tapez 'q' pour annuler la saisie.): ",
                "identifier",
            )
        except KeyboardInterrupt:
            return

        # Check if player exist
        player = db_players.get(Query().identifier == player_id)

        if player is None:
            print_error(f"Player '{player_id}' not found!")
            return

        tournament_name = tournament["name"]
        if player_id not in tournament["players_list"]:
            print_error(
                f"Player '{player_id}' not subscribed to tournament '{tournament_name}'!"
            )
            return

        tournament["players_list"].remove(player_id)
        db_tournaments.update(tournament, Query().name == tournament_name)

        print_success(
            f"Player '{player_id}' unsubscribed from tournament '{tournament_name}' successfully!"
        )

    def start_next_round(self, tournament):
        players_list = tournament["players_list"]

        if len(players_list) < 2:
            print_error(
                "Le nombre de joueurs inscrits doit être au moins 2 pour commencer un tour !"
            )
            return
        if len(players_list) % 2 != 0:
            print_error(
                "Le nombre de joueurs inscrits doit être pair pour commencer un tour !"
            )
            return

        if (
            tournament["rounds_list"] != []
            and tournament["rounds_list"][-1]["end_date"] is None
        ):
            print_error("Le tour n'est pas encore terminé !")
            return

        if tournament["rounds_list"] == []:
            random.shuffle(players_list)
        else:
            players_scores = defaultdict(float)

            for round in tournament["rounds_list"]:
                for match in round["matches_list"]:
                    for player_id, score in match:
                        players_scores[player_id] += score

            # print(players_scores)
            # {
            #     "AB12345": 2.0,
            #     "CD67890": 2.5,
            #     "EF12345": 1.0,
            #     "GH67890": 2.5,
            #     "IJ12345": 3.0,
            #     "KL67890": 1.0,
            # }
            players_list = [
                key
                for key, _ in sorted(
                    players_scores.items(), key=lambda item: item[1], reverse=True
                )
            ]

        matches_list = []
        for index in range(0, len(players_list), 2):
            matches_list.append(
                Match(
                    player1_id=players_list[index],
                    score1=0,
                    player2_id=players_list[index + 1],
                    score2=0,
                )
            )

        tournament["current_round"] += 1

        # create 1st round
        round = Round(
            matchs_list=matches_list,
            name=f"Round {tournament['current_round']}",
            start_time=datetime.now(),
            end_time=None,
        )

        tournament_name = tournament["name"]

        tournament["rounds_list"].append(round.to_dict())
        db_tournaments.update(tournament, Query().name == tournament_name)

        print_success(
            f"{round.name} created for tournament '{tournament_name}' successfully!"
        )

    def add_results_for_the_round(self, tournament):
        print_tornament_title(f"Round {tournament['current_round']}")

        for match in tournament["rounds_list"][-1]["matches_list"]:
            player1_id = match[0][0]
            player2_id = match[1][0]

            print(
                f"\n{Fore.YELLOW}Qui a gagné ? {player1_id} ou {player2_id} :{Style.RESET_ALL}\n"
            )
            print(f"1. {player1_id}")
            print(f"2. {player2_id}")
            print("3. Egalité")
            print("q. Quitter")
            try:

                choice = ask_for_input(
                    "Votre choix: ",
                    "integer",
                )
            except KeyboardInterrupt:
                return

            if choice == "1":
                match[0][1] = 1
                match[1][1] = 0
            elif choice == "2":
                match[0][1] = 0
                match[1][1] = 1
            elif choice == "3":
                match[0][1] = 0.5
                match[1][1] = 0.5

        tournament["rounds_list"][-1]["end_date"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

        db_tournaments.update(tournament, Query().name == tournament["name"])
        print_success("Résultats ajoutés avec succès !")

    def run(self):
        print_tornament_title("Gestion des tournois")
        menu = """1. Créer un tournoi
2. Gérer un tournoi
q. Quitter

Votre choix: """
        try:
            choice = ask_for_input(menu, "integer")
            if choice == "1":
                self.create_tournament()
            elif choice == "2":
                self.manage_tournament()
        except KeyboardInterrupt:
            return

    def manage_tournament(self):
        while True:
            print_tornament_title("Gérer un tournoi")
            # print all the tournaments names
            tournaments = db_tournaments.all()
            for index, tournament in enumerate(tournaments):
                print(f"{index + 1}. {tournament['name']}")
            print("q. Quitter")

            tournament_index = input_choice("Votre choix: ")

            if tournament_index == "q":
                return

            tournament = tournaments[int(tournament_index) - 1]
            self.manage_selected_tournament(tournament)

    def manage_selected_tournament(self, tournament):
        tournament_name = tournament["name"]
        while True:
            print_tornament_title(f"Tournoi '{tournament_name}'")
            print("1. Inscrire un joueur")
            print("2. Désinscrire un joueur")
            print("3. Ajouter les résultats du tour")
            print("4. Commencer le prochain tour")
            print("q. Quitter")
            choice = input_choice("Votre choix: ")
            if choice == "1":
                self.subscribe_players_to_tournament(tournament)
            elif choice == "2":
                self.unsubscribe_players_from_tournament(tournament)
            elif choice == "3":
                self.add_results_for_the_round(tournament)
            elif choice == "4":
                self.start_next_round(tournament)

            elif choice == "q":
                break
