from models.player import Player
from utils.db import db_manager
from views.player_view import PlayerView


class PlayerController:
    def __init__(self, view: PlayerView):
        self.view = view

    def create_player(self):
        """
        Demande les infos d'un joueur et l'ajoute à la base de données
        Si le joueur existe déjà, affiche un message d'erreur
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
        if db_manager.get_player(player.identifier) is not None:
            self.view.display_error(f"Joueur '{player.identifier}' existe deja !")
            return

        db_manager.insert_player(player)

        self.view.display_success(
            f"Joueur {player.identifier} a été ajouté avec succès !"
        )

    def remove_player(self):
        """
        Demande l'ID d'un joueur et le supprime de la base de données
        Si le joueur n'existe pas, affiche un message d'erreur
        """
        self.view.display_player_title("Suppression de joueur")
        try:
            identifier_to_remove = self.view.ask_for_input(
                "Saisissez l'ID du joueur à supprimer (ou tapez 'q' pour annuler la saisie.): ",
                "identifier",
            )
        except KeyboardInterrupt:
            return
        player = db_manager.get_player(identifier_to_remove)

        if player is None:
            self.view.display_error(f"Joueur '{identifier_to_remove}' n'existe pas !")
            return

        db_manager.remove_player(identifier_to_remove)
        self.view.display_success(
            f"Joueur '{identifier_to_remove}' supprimé avec succès !"
        )

    def run(self):
        """
        Affiche le menu des joueurs et demande à l'utilisateur de choisir une option
        """
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
