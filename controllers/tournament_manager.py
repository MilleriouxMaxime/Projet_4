from models.tournament import Tournament
from utils.db import tournaments_table, players_table
from tinydb import Query
from colorama import Fore, Style
from models.round import Round
from models.round import Match

from datetime import datetime


def print_error(message):
    print("\n ⚠️  " + Fore.RED + message + Style.RESET_ALL + "⚠️")


def print_success(message):
    print("\n \u2705 " + Fore.GREEN + message + Style.RESET_ALL + "\u2705")


def print_title(message):
    print("\n" + Fore.MAGENTA + message + Style.RESET_ALL)


def input_choice(message):
    return input("\n" + Fore.CYAN + message + Style.RESET_ALL)


class TournamentManager:

    def create_tournament(self):
        """
        Création d'un tournoi
        """
        name = input("Enter tournament name: ")
        place = input("Enter tournament place: ")
        start_date = input("Enter tournament start date: ")
        end_date = input("Enter tournament end date: ")
        total_round_number = input("Enter tournament total round number: ")
        description = input("Enter tournament description: ")

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

        tournaments_table.insert(tournament.to_dict())

        print_success(f"Tournament '{tournament.name}' created successfully!")

    def subscribe_players_to_tournament(self, tournament):
        """
        Inscription d'un joueur à un tournoi en utilisant son ID pour le retrouver dans la base de données
        """
        player_id = input("Enter player ID: ")
        # Check if player exist
        player = players_table.get(Query().identifier == player_id)

        if player is None:
            print_error(f"Player '{player_id}' not found!")
            return

        tournament_name = tournament["name"]
        tournament["players_list"].append(player_id)
        tournaments_table.update(tournament, Query().name == tournament_name)

        print_success(
            f"Player '{player_id}' subscribed to tournament '{tournament_name}' successfully!"
        )

    def unsubscribe_players_from_tournament(self, tournament):
        """
        Désinscription d'un joueur à un tournoi en utilisant son ID pour le retrouver dans la base de données
        """

        player_id = input("Enter player ID: ")
        # Check if player exist
        player = players_table.get(Query().identifier == player_id)

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
        tournaments_table.update(tournament, Query().name == tournament_name)

        print_success(
            f"Player '{player_id}' unsubscribed from tournament '{tournament_name}' successfully!"
        )

    def start_next_round(self, tournament):
        players_list = tournament["players_list"]
        # ["ED1234", "AZ8797", "AZ8791", "AZ8792", "AZ8793", "AZ8794"]

        if len(players_list) < 4:
            print_error(
                "Le nombre de joueurs inscrits doit être au moins 4 pour commencer un tour !"
            )
            return
        if len(players_list) % 2 != 0:
            print_error(
                "Le nombre de joueurs inscrits doit être pair pour commencer un tour !"
            )
            return

        # TODO if not pair return error

        # TODO if less then 4 players return error

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

        # create 1st round
        round = Round(
            matchs_list=matches_list,
            name="Round 1",
            start_time=datetime.now(),
            end_time=None,
        )

        tournament_name = tournament["name"]

        tournament["current_round"] = 1
        tournament["rounds_list"].append(round.to_dict())
        tournaments_table.update(tournament, Query().name == tournament_name)

        print_success(
            f"Round 1 created for tournament '{tournament_name}' successfully!"
        )

    def add_results_for_the_round(self, tournament):
        print(f"Current round is {tournament['current_round']}")

        # TODO check that end_time is None

    def run(self):
        while True:
            print_title("♟️  Gestion des tournois ♟️ \n")
            print("1. Créer un tournoi")
            print("2. Gérer un tournoi")
            print("q. Quitter")
            choice = input_choice("Votre choix: ")
            if choice == "1":
                self.create_tournament()
            elif choice == "2":
                self.manage_tournament()
            elif choice == "q":
                break

    def manage_tournament(self):
        print_title("♟️  Gérer un tournoi ♟️ \n")
        tournament_name = input("Enter tournament name: ")
        # Check if tournament exist
        tournament = tournaments_table.get(Query().name == tournament_name)

        if tournament is None:
            print_error(f"Tournament '{tournament_name}' not found!")
            return

        while True:
            print_title(f"♟️  Tournoi '{tournament_name}' ♟️\n")
            print("1. Inscrire un joueur")
            print("2. Désinscrire un joueur")
            print("3. Commencer le prochain tour")
            print("4. Ajouter les résultats du tour")
            print("q. Quitter")
            choice = input_choice("Votre choix: ")
            if choice == "1":
                self.subscribe_players_to_tournament(tournament)
            elif choice == "2":
                self.unsubscribe_players_from_tournament(tournament)
            elif choice == "3":
                self.start_next_round(tournament)
            elif choice == "4":
                self.add_results_for_the_round(tournament)

            elif choice == "q":
                break
