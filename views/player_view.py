from views.base_view import BaseView


class PlayerView(BaseView):
    def get_player_infos(self):
        last_name = self.ask_for_input(
            "Saisissez le nom du joueur (ou tapez 'q' pour quitter la création de joueur): ",
            "name",
        )
        first_name = self.ask_for_input(
            "Saisissez le prénom du joueur (ou tapez 'q' pour quitter la création de joueur): ",
            "name",
        )

        birth_date = self.ask_for_input(
            "Saisissez la date de naissance du joueur au format JJ/MM/AAAA (ou tapez 'q' pour quitter la création de joueur): ",
            "date",
        )
        identifier = self.ask_for_input(
            "Saisissez l'ID du joueur (ou tapez 'q' pour quitter la création de joueur): ",
            "identifier",
        )
        return {
            "last_name": last_name,
            "first_name": first_name,
            "birth_date": birth_date,
            "identifier": identifier,
        }
