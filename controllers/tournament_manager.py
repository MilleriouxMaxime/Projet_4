from models.tournament import Tournament
from utils.db import tournaments_table, players_table
from tinydb import Query
from colorama import Fore, Style


def print_error(message):
    print(Fore.RED + "\n \u26A0 " + message + " \u26A0 " + Style.RESET_ALL)


def print_success(message):
    print(Fore.GREEN + "\n \u2705 " + message + " \u2705 " + Style.RESET_ALL)


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

        print_success("Tournament created successfully!")

    def subscribe_players_to_tournament(self):
        """
        Inscription d'un joueur à un tournoi en utilisant son ID pour le retrouver dans la base de données
        """
        player_id = input("Enter player ID: ")
        # Check if player exist
        player = players_table.get(Query().identifier == player_id)

        if player is None:
            print_error("Player not found!")
            return

        tournament_name = input("Enter tournament name: ")
        # Check if tounament exist
        tournament = tournaments_table.get(Query().name == tournament_name)

        if tournament is None:
            print_error("Tournament not found!")
            return

        tournament["players_list"].append(player_id)
        tournaments_table.update(tournament, Query().name == tournament_name)

        print_success("Player subscribed to tournament successfully!")

    def run(self):
        while True:

            print("\n Tournoi \n")
            print("1. Creer un tournoi")
            print("2. Inscrire un joueur")
            print("q. Quitter")
            choice = input("Votre choix: ")
            if choice == "1":
                self.create_tournament()
            elif choice == "2":
                self.subscribe_players_to_tournament()
            elif choice == "q":
                break
