from datetime import datetime

from tinydb import Query

from models.player import Player
from utils.db import db_players
from utils.formating import input_choice, print_error, print_player_title, print_success


class PlayerController:

    def create_player(self):
        """
        Ajouter un joueur à la base de données
        """
        print_player_title("Création de joueur")

        while True:
            last_name = input_choice(
                "Saisissez le nom du joueur ou tapez 'q' pour quitter la création de joueur): "
            )
            if last_name == "q":
                return
            elif (
                not last_name.isalpha()
                or not last_name[0].isupper()
                or not last_name[1:].islower()
            ):
                print_error(
                    "Le nom doit commencer par une lettre majuscule et ne peut contenir que des lettres."
                )
            else:
                break

        while True:
            first_name = input_choice(
                "Saisissez le prénom du joueur (ou tapez 'q' pour quitter la création de joueur): "
            )
            if first_name == "q":
                return
            elif (
                not first_name.isalpha()
                or not first_name[0].isupper()
                or not first_name[1:].islower()
            ):
                print_error(
                    "Le prénom doit commencer par une lettre majuscule et ne peut contenir que des lettres."
                )
            else:
                break

        while True:
            birth_date = input_choice(
                "Saisissez la date de naissance du joueur au format JJ/MM/AAAA (ou tapez 'q' pour quitter la création de joueur): "
            )
            if birth_date == "q":
                return
            try:
                datetime.strptime(birth_date, "%d/%m/%Y")
            except ValueError:
                print_error("La date de naissance doit avoir le format JJ/MM/AAAA.")
            else:
                break

        while True:
            identifier = input_choice(
                "Saisissez l'ID du joueur (ou tapez 'q' pour quitter la création de joueur): "
            )
            if identifier == "q":
                return
            elif (
                not identifier[0:2].isupper()
                or not identifier[2:].isdigit()
                or len(identifier) != 7
            ):
                print_error(
                    "L'ID doit avoir le format AB12345 (2 lettres Majuscules puis 5 chiffres)."
                )
                continue

            player_query = Query()
            existing_player = db_players.search(player_query.identifier == identifier)

            if existing_player:
                print_error(
                    f"L'ID {identifier} existe déjà dans la base de données. Veuillez saisir un autre ID."
                )
                continue

            break

        player_query = Query()
        existing_player = db_players.search(player_query.identifier == identifier)

        if existing_player:
            print_error(
                f"L'ID {identifier} existe déjà dans la base de données. Veuillez saisir un autre ID."
            )
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
        while True:
            identifier_to_remove = input_choice(
                "Saisissez l'ID du joueur à supprimer (ou tapez 'q' pour annuler la saisie.): "
            )
            player = db_players.get(Query().identifier == identifier_to_remove)

            if identifier_to_remove == "q":
                return
            elif (
                not identifier_to_remove[0:2].isupper()
                or not identifier_to_remove[2:].isdigit()
                or len(identifier_to_remove) != 7
            ):
                print_error(
                    "L'ID doit avoir le format AB12345 (2 lettres puis 5 chiffres)."
                )
            elif player is None:
                print_error(f"Joueur '{identifier_to_remove}' n'existe pas !")
            else:
                break

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
