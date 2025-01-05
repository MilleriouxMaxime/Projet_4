from datetime import datetime


class Validator:

    def name_is_valid(self, choice: str):
        """
        Vérifie que le format du nom est correct
        """
        if not choice.isalpha() or not choice[0].isupper() or not choice[1:].islower():
            return False
        return True

    def date_is_valid(self, choice: str):
        """
        Vérifie que le format de la date est correct
        """
        try:
            datetime.strptime(choice, "%d/%m/%Y")
        except ValueError:
            return False
        return True

    def identifier_is_valid(self, choice: str):
        """
        Vérifie que le format de l'identifiant est correct
        """
        if not choice[0:2].isupper() or not choice[2:].isdigit() or len(choice) != 7:
            return False
        return True

    def integer_is_valid(self, choice: str):
        """
        Vérifie que le "choice" est bien un entier
        """
        if not choice.isdigit():
            return False
        return True

    def round_is_valid(self, choice: str):
        """
        Vérifie que le "choice" est bien un entier entre 1 et 10
        """
        if not self.integer_is_valid(choice):
            return False
        choice = int(choice)
        if choice <= 0 or choice > 10:
            return False
        return True

    def choice_is_valid(self, choice: str, input_type: str):
        """
        Selon le "input_type" vérifie que le "choice" est au bon format
        """

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
