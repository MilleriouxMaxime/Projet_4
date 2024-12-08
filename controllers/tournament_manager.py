from models.tournament import Tournament
import json


class TournamentManager:

    def create_tournament(self):
        """
        Création d'un fichier JSON avec les informations du tournoi
        (name, place, start date, end date, current_round, rounds_list, players_list, description, total_round_number)
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

        with open(f"models/data/tournaments/{name}.json", "w") as file:
            json.dump(tournament.to_dict(), file, indent=4)
