import random
from datetime import datetime

from models.round import Match, Round
from models.tournament import Tournament
from utils.db import db_manager
from views.tournament_view import TournamentView


class TournamentController:
    def __init__(self, view: TournamentView):
        self.view = view

    def insert_match_result(self, tournament):
        """
        Demande le resultat de chaque match du tour
        Met à jour les scores d'un match
        Met à jour le tableau de scores
        """

        for match in tournament["rounds_list"][-1]["matches_list"]:
            player1_id = match[0][0]
            player2_id = match[1][0]

            player1 = db_manager.get_player(player1_id)
            player2 = db_manager.get_player(player2_id)

            player1_full_name = f"{player1['last_name']} {player1['first_name']}"
            player2_full_name = f"{player2['last_name']} {player2['first_name']}"

            try:
                choice = self.view.get_match_results(
                    player1_full_name, player2_full_name
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

            if player1_id not in tournament["scoreboard"]:
                tournament["scoreboard"][player1_id] = 0
            if player2_id not in tournament["scoreboard"]:
                tournament["scoreboard"][player2_id] = 0

            tournament["scoreboard"][player1_id] += match[0][1]
            tournament["scoreboard"][player2_id] += match[1][1]

    def get_sorted_players_list(self, tournament):
        """
        Si c'est le premier tour, mélange les joueurs
        Sinon, ordonne les joueurs selon leurs scores dans le tableau des scores
        """
        players_list = tournament["players_list"]
        if tournament["rounds_list"] == []:
            random.shuffle(players_list)
        else:
            players_scores = tournament["scoreboard"]

            players_list = [
                key
                for key, _ in sorted(
                    players_scores.items(), key=lambda item: item[1], reverse=True
                )
            ]

        return players_list

    def create_round(self, tournament, players_list):
        """
        Crée les matchs d'un tour
        Crée un nouveau tour
        """
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
        return round

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
            {},
            infos["total_round_number"],
        )

        db_manager.insert_tournament(tournament)

        self.view.display_success(
            f"Tournament '{tournament.name}' a été créé avec succès !"
        )

    def subscribe_players_to_tournament(self, tournament):
        """
        Inscription d'un joueur à un tournoi en utilisant son ID pour le retrouver dans la base de données
        """
        if tournament["status"] == "En cours" or tournament["status"] == "Termine":
            self.view.display_error(
                "Impossible d'inscrire des joueurs à un tournoi en cours ou terminé."
            )
            return
        try:
            player_id = self.view.ask_for_input(
                "Saisissez l'ID du joueur à inscrire (ou tapez 'q' pour annuler la saisie.): ",
                "identifier",
            )
        except KeyboardInterrupt:
            return

        player = db_manager.get_player(player_id)

        if player is None:
            self.view.display_error(f"Joueur '{player_id}' n'existe pas !")
            return

        tournament_name = tournament["name"]
        tournament["players_list"].append(player_id)
        db_manager.update_tournament(tournament)

        self.view.display_success(
            f"Player '{player_id}' subscribed to tournament '{tournament_name}' successfully!"
        )

    def unsubscribe_players_from_tournament(self, tournament):
        """
        Désinscription d'un joueur à un tournoi en utilisant son ID pour le retrouver dans la base de données
        """
        if tournament["status"] == "En cours" or tournament["status"] == "Termine":
            self.view.display_error(
                "Impossible de désinscrire des joueurs d'un tournoi en cours ou terminé."
            )
            return
        try:
            player_id = self.view.ask_for_input(
                "Saisissez l'ID du joueur à inscrire (ou tapez 'q' pour annuler la saisie.): ",
                "identifier",
            )
        except KeyboardInterrupt:
            return

        player = db_manager.get_player(player_id)

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
        db_manager.update_tournament(tournament)

        self.view.display_success(
            f"Player '{player_id}' unsubscribed from tournament '{tournament_name}' successfully!"
        )

    def start_next_round(self, tournament):
        """
        Vérifie que le tournoi n'est pas terminé
        Crée un nouveau tour
        Met a jour le tournoi dans la base de données
        Affiche les matchs du nouveau tour
        """
        if tournament["status"] == "Termine":
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

        players_list = self.get_sorted_players_list(tournament)
        round = self.create_round(tournament, players_list)

        tournament["rounds_list"].append(round.to_dict())
        tournament["status"] = "En cours"
        db_manager.update_tournament(tournament)

        self.view.display_success(f"{round.name} créé avec succès !")
        self.view.display_tournament_title(f"Liste des matchs pour le {round.name}")
        self.show_matches_for_round(round)

    def add_results_for_the_round(self, tournament):
        """
        Met à jour les score d'un match dans un tournoi dans la base de données
        """
        if tournament["status"] != "En cours":
            self.view.display_error("Le tournoi n'est pas en cours !")
            return

        if tournament["rounds_list"][-1]["end_date"] is not None:
            self.view.display_error("Les scores ont déjà été renseignés !")
            return

        self.view.display_tournament_title(f"Round {tournament['current_round']}")
        self.insert_match_result(tournament)
        tournament["rounds_list"][-1]["end_date"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

        self.view.display_success("Résultats ajoutés avec succès !")
        scoreboard = sorted(
            tournament["scoreboard"].items(), key=lambda item: item[1], reverse=True
        )

        self.view.display_tournament_title("Tableau des scores : ")

        for player_id, score in scoreboard:
            player = db_manager.get_player(player_id)
            self.view.display_info(
                f"{player['last_name']} {player['first_name']} : {score}"
            )

        if tournament["current_round"] == tournament["total_round_number"]:
            tournament["status"] = "Termine"
            self.view.display_success("Le tournoi est terminé !")
            player = db_manager.get_player(scoreboard[0][0])
            self.view.display_tournament_title(
                f"Vainqueur : {player['last_name']} {player['first_name']}"
            )

        db_manager.update_tournament(tournament)

    def run(self):
        """
        Affiche le menu d'un tournoi
        Demande à l'utilisateur de choisir une option
        """
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
        """
        Affiche tous les tournois et demande à l'utilisateur de choisir un tournoi
        Affiche le menu pour le tournoi sélectionné
        """
        while True:
            self.view.display_tournament_title("Gérer un tournoi")
            tournaments = db_manager.get_all_tournaments()
            tournament_names = [tournament["name"] for tournament in tournaments]
            tournament_index = self.view.ask_for_options(tournament_names)

            if tournament_index == "q":
                return

            tournament_index = int(tournament_index)

            if tournament_index not in range(1, len(tournament_names) + 1):
                self.view.display_error("Veuillez choisir un tournoi dans la liste !")
                continue

            tournament = tournaments[tournament_index - 1]
            self.manage_selected_tournament(tournament)

    def manage_selected_tournament(self, tournament):
        """
        Affiche le menu pour le tournoi sélectionné
        Demande à l'utilisateur de choisir une option
        """
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

    def show_matches_for_round(self, round: Round):
        """
        Affiche les matchs d'un tour
        """

        for match in round.matchs_list:
            player1 = db_manager.get_player(match.player1_id)
            player2 = db_manager.get_player(match.player2_id)
            self.view.display_info(
                f"{player1["last_name"]} {player1['first_name']} vs {player2['last_name']} {player2['first_name']}"
            )
