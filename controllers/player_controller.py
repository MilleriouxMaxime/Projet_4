from datetime import datetime

from tinydb import Query

from models.player import Player
from utils.db import db_players
from utils.formating import input_choice, print_error, print_player_title, print_success


def name_is_valid(choice: str):
    if not choice.isalpha() or not choice[0].isupper() or not choice[1:].islower():
        print_error(
            "Le nom doit commencer par une lettre majuscule et ne peut contenir que des lettres."
        )
        return False
    return True


def date_is_valid(choice: str):
    try:
        datetime.strptime(choice, "%d/%m/%Y")
    except ValueError:
        print_error("La date de naissance doit avoir le format JJ/MM/AAAA.")
        return False
    return True


def identifier_is_valid(choice: str):
    if not choice[0:2].isupper() or not choice[2:].isdigit() or len(choice) != 7:
        print_error(
            "L'ID doit avoir le format AB12345 (2 lettres Majuscules puis 5 chiffres)."
        )
        return False
    return True


def choice_is_valid(choice, input_type):
    if input_type == "name":
        return name_is_valid(choice)
    elif input_type == "date":
        return date_is_valid(choice)
    elif input_type == "identifier":
        return identifier_is_valid(choice)
    return True


def ask_for_input(message, input_type):
    while True:
        choice = input_choice(message)
        if choice == "q":
            raise KeyboardInterrupt
        if choice_is_valid(choice, input_type):
            return choice


class PlayerController:

    def create_player(self):
        """
        Ajouter un joueur à la base de données
        """
        print_player_title("Création de joueur")
        try:
            last_name = ask_for_input(
                "Saisissez le nom du joueur ou tapez 'q' pour quitter la création de joueur): ",
                "name",
            )
            first_name = ask_for_input(
                "Saisissez le prénom du joueur ou tapez 'q' pour quitter la création de joueur): ",
                "name",
            )

            birth_date = ask_for_input(
                "Saisissez la date de naissance du joueur au format JJ/MM/AAAA (ou tapez 'q' pour quitter la création de joueur): ",
                "date",
            )
            identifier = ask_for_input(
                "Saisissez l'ID du joueur (ou tapez 'q' pour quitter la création de joueur): ",
                "identifier",
            )
        except KeyboardInterrupt:
            return

        player = Player(
            last_name,
            first_name,
            birth_date,
            identifier,
        )
        db_players.insert(player.to_dict())
        print_success(f"Joueur {identifier} a été ajouté avec succès !")

    def remove_player(self):
        """
        Supprimer un joueur de la base de données
        """
        print_player_title("Suppression de joueur")
        try:
            identifier_to_remove = ask_for_input(
                "Saisissez l'ID du joueur à supprimer (ou tapez 'q' pour annuler la saisie.): ",
                "identifier",
            )
        except KeyboardInterrupt:
            return
        player = db_players.get(Query().identifier == identifier_to_remove)

        if player is None:
            print_error(f"Joueur '{identifier_to_remove}' n'existe pas !")
            return

        confirmation = input_choice(
            f"Etes-vous sûr de vouloir supprimer le joueur {identifier_to_remove}? (o/n): "
        )

        if confirmation == "n":
            return
        if confirmation == "o":

            db_players.remove(Query().identifier == identifier_to_remove)
            print_success(f"Joueur '{identifier_to_remove}' supprimé avec succès !")

    def run(self):
        while True:
            print_player_title("Gestion des joueurs")
            print("1. Créer un joueur")
            print("2. Supprimer un joueur")
            print("q. Quitter")
            choice = input_choice("Votre choix: ")
            if choice == "1":
                self.create_player()
            elif choice == "2":
                self.remove_player()
            elif choice == "q":
                break
