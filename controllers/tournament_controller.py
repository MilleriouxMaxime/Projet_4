import random
from collections import defaultdict
from datetime import datetime

from tinydb import Query

from models.round import Match, Round
from models.tournament import Tournament
from utils.db import db_players, db_tournaments
from views.tournament_view import TournamentView


class TournamentController:
    def __init__(self, view: TournamentView):
        self.view = view

    def create_tournament(self):
        """
        Création d'un tournoi
        """
        self.view.display_tournament_title("Création d'un tournoi")
        try:
            infos = self.view.get_tournament_infos()
        except KeyboardInterrupt:
            return

        tournament = Tournament(
            infos["name"],
            infos["place"],
            infos["start_date"],
            infos["end_date"],
            0,
            [],
            [],
            infos["description"],
            infos["total_round_number"],
        )

        db_tournaments.insert(tournament.to_dict())

        self.view.display_success(
            f"Tournament '{tournament.name}' a été créé avec succès !"
        )

    def subscribe_players_to_tournament(self, tournament):
        """
        Inscription d'un joueur à un tournoi en utilisant son ID pour le retrouver dans la base de données
        """
        try:
            player_id = self.view.ask_for_input(
                "Saisissez l'ID du joueur à inscrire (ou tapez 'q' pour annuler la saisie.): ",
                "identifier",
            )
        except KeyboardInterrupt:
            return

        player = db_players.get(Query().identifier == player_id)

        if player is None:
            self.view.display_error(f"Joueur '{player_id}' n'existe pas !")
            return

        tournament_name = tournament["name"]
        tournament["players_list"].append(player_id)
        db_tournaments.update(tournament, Query().name == tournament_name)

        self.view.display_success(
            f"Player '{player_id}' subscribed to tournament '{tournament_name}' successfully!"
        )

    def unsubscribe_players_from_tournament(self, tournament):
        """
        Désinscription d'un joueur à un tournoi en utilisant son ID pour le retrouver dans la base de données
        """

        try:
            player_id = self.view.ask_for_input(
                "Saisissez l'ID du joueur à inscrire (ou tapez 'q' pour annuler la saisie.): ",
                "identifier",
            )
        except KeyboardInterrupt:
            return

        # Check if player exist
        player = db_players.get(Query().identifier == player_id)

        if player is None:
            self.view.display_error(f"Player '{player_id}' not found!")
            return

        tournament_name = tournament["name"]
        if player_id not in tournament["players_list"]:
            self.view.display_error(
                f"Player '{player_id}' not subscribed to tournament '{tournament_name}'!"
            )
            return

        tournament["players_list"].remove(player_id)
        db_tournaments.update(tournament, Query().name == tournament_name)

        self.view.display_success(
            f"Player '{player_id}' unsubscribed from tournament '{tournament_name}' successfully!"
        )

    def start_next_round(self, tournament):
        if tournament["current_round"] == tournament["total_round_number"]:
            self.view.display_error("Le tournoi est terminé !")
            return

        players_list = tournament["players_list"]

        if len(players_list) < 2:
            self.view.display_error(
                "Le nombre de joueurs inscrits doit être au moins 2 pour commencer un tour !"
            )
            return
        if len(players_list) % 2 != 0:
            self.view.display_error(
                "Le nombre de joueurs inscrits doit être pair pour commencer un tour !"
            )
            return

        if (
            tournament["rounds_list"] != []
            and tournament["rounds_list"][-1]["end_date"] is None
        ):
            self.view.display_error("Le tour n'est pas encore terminé !")
            return

        if tournament["rounds_list"] == []:
            random.shuffle(players_list)
        else:
            players_scores = defaultdict(float)

            for round in tournament["rounds_list"]:
                for match in round["matches_list"]:
                    for player_id, score in match:
                        players_scores[player_id] += score

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

        round = Round(
            matchs_list=matches_list,
            name=f"Round {tournament['current_round']}",
            start_time=datetime.now(),
            end_time=None,
        )

        tournament_name = tournament["name"]

        tournament["rounds_list"].append(round.to_dict())
        db_tournaments.update(tournament, Query().name == tournament_name)

        self.view.display_success(f"{round.name} créé avec succès !")

        tournament["status"] = "En cours"
        db_tournaments.update(tournament, Query().name == tournament_name)

    def add_results_for_the_round(self, tournament):
        self.view.display_tournament_title(f"Round {tournament['current_round']}")

        for match in tournament["rounds_list"][-1]["matches_list"]:
            player1_id = match[0][0]
            player2_id = match[1][0]

            try:
                choice = self.view.get_match_results(player1_id, player2_id)
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
        self.view.display_success("Résultats ajoutés avec succès !")
        if tournament["current_round"] == tournament["total_round_number"]:
            tournament["status"] = "Termine"
            db_tournaments.update(tournament, Query().name == tournament["name"])

    def run(self):
        while True:
            self.view.display_tournament_title("Gestion des tournois")
            choice = self.view.ask_for_options(["Créer un tournoi", "Gérer un tournoi"])
            if choice == "1":
                self.create_tournament()
            elif choice == "2":
                self.manage_tournament()
            elif choice == "q":
                break

    def manage_tournament(self):
        while True:
            self.view.display_tournament_title("Gérer un tournoi")
            tournaments = db_tournaments.all()
            tournament_names = [tournament["name"] for tournament in tournaments]
            tournament_index = self.view.ask_for_options(tournament_names)

            if tournament_index == "q":
                return

            tournament = tournaments[int(tournament_index) - 1]
            self.manage_selected_tournament(tournament)

    def manage_selected_tournament(self, tournament):
        tournament_name = tournament["name"]
        while True:
            self.view.display_tournament_title(f"Tournoi '{tournament_name}'")
            choice = self.view.ask_for_options(
                [
                    "Inscrire un joueur",
                    "Désinscrire un joueur",
                    "Ajouter les résultats du tour",
                    "Commencer le prochain tour",
                ]
            )
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
