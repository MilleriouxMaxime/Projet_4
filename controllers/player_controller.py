from tinydb import Query

from models.player import Player
from utils.db import db_players
from views.player_view import PlayerView


class PlayerController:
    def __init__(self, view: PlayerView):
        self.view = view

    def create_player(self):
        """
        Ajouter un joueur à la base de données
        """
        self.view.display_player_title("Création de joueur")
        try:
            infos = self.view.get_player_infos()
        except KeyboardInterrupt:
            return
        player = Player(
            infos["last_name"],
            infos["first_name"],
            infos["birth_date"],
            infos["identifier"],
        )
        if db_players.get(Query().identifier == player.identifier) is not None:
            self.view.display_error(f"Joueur '{player.identifier}' existe deja !")
            return
        db_players.insert(player.to_dict())
        self.view.display_success(
            f"Joueur {player.identifier} a été ajouté avec succès !"
        )

    def remove_player(self):
        """
        Supprimer un joueur de la base de données
        """
        self.view.display_player_title("Suppression de joueur")
        try:
            identifier_to_remove = self.view.ask_for_input(
                "Saisissez l'ID du joueur à supprimer (ou tapez 'q' pour annuler la saisie.): ",
                "identifier",
            )
        except KeyboardInterrupt:
            return
        player = db_players.get(Query().identifier == identifier_to_remove)

        if player is None:
            self.view.display_error(f"Joueur '{identifier_to_remove}' n'existe pas !")
            return

        db_players.remove(Query().identifier == identifier_to_remove)
        self.view.display_success(
            f"Joueur '{identifier_to_remove}' supprimé avec succès !"
        )

    def run(self):
        while True:
            self.view.display_player_title("Gestion des joueurs")
            choice = self.view.ask_for_options(
                ["Créer un joueur", "Supprimer un joueur"]
            )

            if choice == "1":
                self.create_player()
            elif choice == "2":
                self.remove_player()
            elif choice == "q":
                break
