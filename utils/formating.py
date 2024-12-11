from colorama import Fore, Style


def print_error(message):
    print("\n ⚠️  " + Fore.RED + message + Style.RESET_ALL + "⚠️\n")


def print_success(message):
    print("\n \u2705 " + Fore.GREEN + message + Style.RESET_ALL + "\u2705 \n")


def print_tornament_title(message):
    print("\n ♟️  "+ Fore.MAGENTA + message + Style.RESET_ALL + "♟️\n")

def print_player_title(message):
    print("\n 🧑‍💻 "+ Fore.MAGENTA + message + Style.RESET_ALL + "🧑‍💻\n")
def input_choice(message):
    return input("\n" + Fore.CYAN + message + Style.RESET_ALL)