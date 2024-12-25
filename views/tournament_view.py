from colorama import Fore, Style

from views.base_view import BaseView


class TournamentView(BaseView):
    def get_tournament_infos(self):
        name = self.ask_for_input(
            "Saisissez le nom du tournoi (ou tapez 'q' pour quitter la création de tournoi): ",
            None,
        )
        place = self.ask_for_input(
            "Saisissez le lieu du tournoi (ou tapez 'q' pour quitter la création de tournoi): ",
            None,
        )
        start_date = self.ask_for_input(
            "Saisissez la date de début du tournoi (ou tapez 'q' pour quitter la création de tournoi): ",
            "date",
        )
        end_date = self.ask_for_input(
            "Saisissez la date de fin du tournoi (ou tapez 'q' pour quitter la création de tournoi): ",
            "date",
        )
        total_round_number = int(
            self.ask_for_input(
                "Saisissez le nombre total de tours du tournoi (ou tapez 'q' pour quitter la création de tournoi): ",
                "round",
            )
        )
        description = self.ask_for_input(
            "Saisissez la description du tournoi (ou tapez 'q' pour quitter la création de tournoi): ",
            None,
        )

        return {
            "name": name,
            "place": place,
            "start_date": start_date,
            "end_date": end_date,
            "total_round_number": total_round_number,
            "description": description,
        }

    def get_match_results(self, player1_id, player2_id):
        print(
            f"\n{Fore.YELLOW}Qui a gagné ? {player1_id} ou {player2_id} :{Style.RESET_ALL}\n"
        )
        print(f"1. {player1_id}")
        print(f"2. {player2_id}")
        print("3. Egalité")
        print("q. Quitter")

        choice = self.ask_for_input(
            "Votre choix: ",
            "integer",
        )
        return choice
