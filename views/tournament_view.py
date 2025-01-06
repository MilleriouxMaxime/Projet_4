from colorama import Fore, Style

from views.base_view import BaseView


class TournamentView(BaseView):
    def get_tournament_infos(self):
        """
        Demande les infos du tournoi
        Retourne un dictionnaire contenant les infos du tournoi
        """
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

    def get_match_results(self, player1, player2):
        """
        Demande les résultats d'un match
        Retourne le choix de l'utilisateur
        """
        print(
            f"\n{Fore.YELLOW}Qui a gagné ? {player1} ou {player2} :{Style.RESET_ALL}\n"
        )
        print(f"1. {player1}")
        print(f"2. {player2}")
        print("3. Egalité")
        print("q. Quitter")

        choice = self.ask_for_input(
            "Votre choix: ",
            "integer",
        )
        return choice
