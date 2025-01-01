from colorama import Fore, Style

from utils.validator import Validator


class BaseView:
    def ask_for_input(self, message, input_type):
        while True:
            choice = self.input_choice(message)
            if choice == "q":
                raise KeyboardInterrupt
            if Validator().choice_is_valid(choice, input_type):
                return choice
            else:
                self.display_choice_error(input_type)

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

    def display_choice_error(self, input_type):
        if input_type == "name":
            self.display_error(
                "Le nom doit commencer par une lettre majuscule et ne peut contenir que des lettres."
            )
        elif input_type == "date":
            self.display_error("La date de naissance doit avoir le format JJ/MM/AAAA.")
        elif input_type == "identifier":
            self.display_error(
                "L'ID doit avoir le format AB12345 (2 lettres Majuscules puis 5 chiffres)."
            )
        elif input_type == "integer":
            self.display_error("Le choix doit être un entier.")
        elif input_type == "round":
            self.display_error(
                "Le nombre de tour ne peut pas être 0 ou inférieur et ne peut pas dépasser 10."
            )

    def input_choice(self, message):
        return input("\n" + Fore.CYAN + message + Style.RESET_ALL)

    def ask_for_options(self, options):
        for index, option in enumerate(options):
            print(f"{index + 1}. {option}")
        print("q. Quitter")
        choice = self.input_choice("Votre choix: ")
        return choice
