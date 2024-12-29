from datetime import datetime

from colorama import Fore, Style


class BaseView:
    def ask_for_input(self, message, input_type):
        while True:
            choice = self.input_choice(message)
            if choice == "q":
                raise KeyboardInterrupt
            if self.choice_is_valid(choice, input_type):
                return choice

    def display_error(self, message):
        print("\n ⚠️  " + Fore.RED + message + Style.RESET_ALL + "⚠️\n")

    def display_success(self, message):
        print("\n ✅  " + Fore.GREEN + message + Style.RESET_ALL + "✅\n")

    def display_tournament_title(self, message):
        print("\n ♟️  " + Fore.MAGENTA + message + Style.RESET_ALL + "♟️\n")

    def display_player_title(self, message):
        print("\n 🧑‍💻 " + Fore.MAGENTA + message + Style.RESET_ALL + "🧑‍💻\n")

    def display_rapport_title(self, message):
        print("\n 📊 " + Fore.MAGENTA + message + Style.RESET_ALL + "📊\n")

    def display_list(self, list_to_display: list[str]):
        print()
        for item in list_to_display:
            print(item)

    def input_choice(self, message):
        return input("\n" + Fore.CYAN + message + Style.RESET_ALL)

    def ask_for_options(self, options):
        for index, option in enumerate(options):
            print(f"{index + 1}. {option}")
        print("q. Quitter")
        choice = self.input_choice("Votre choix: ")
        return choice

    def name_is_valid(self, choice: str):
        if not choice.isalpha() or not choice[0].isupper() or not choice[1:].islower():
            self.display_error(
                "Le nom doit commencer par une lettre majuscule et ne peut contenir que des lettres."
            )
            return False
        return True

    def date_is_valid(self, choice: str):
        try:
            datetime.strptime(choice, "%d/%m/%Y")
        except ValueError:
            self.display_error("La date de naissance doit avoir le format JJ/MM/AAAA.")
            return False
        return True

    def identifier_is_valid(self, choice: str):
        if not choice[0:2].isupper() or not choice[2:].isdigit() or len(choice) != 7:
            self.display_error(
                "L'ID doit avoir le format AB12345 (2 lettres Majuscules puis 5 chiffres)."
            )
            return False
        return True

    def integer_is_valid(self, choice: str):
        if not choice.isdigit():
            self.display_error("Le choix doit être un entier.")
            return False
        return True

    def round_is_valid(self, choice: str):
        if not self.integer_is_valid(choice):
            return False
        choice = int(choice)
        if choice <= 0 or choice > 10:
            self.display_error(
                "Le nombre de tour ne peut pas être 0 ou inférieur et ne peut pas dépasser 10."
            )
            return False
        return True

    def choice_is_valid(self, choice, input_type):
        if input_type == "name":
            return self.name_is_valid(choice)
        elif input_type == "date":
            return self.date_is_valid(choice)
        elif input_type == "identifier":
            return self.identifier_is_valid(choice)
        elif input_type == "integer":
            return self.integer_is_valid(choice)
        elif input_type == "round":
            return self.round_is_valid(choice)
        return True
