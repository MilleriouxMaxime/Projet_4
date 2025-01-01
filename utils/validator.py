from datetime import datetime


class Validator:

    def name_is_valid(self, choice: str):
        if not choice.isalpha() or not choice[0].isupper() or not choice[1:].islower():
            return False
        return True

    def date_is_valid(self, choice: str):
        try:
            datetime.strptime(choice, "%d/%m/%Y")
        except ValueError:
            return False
        return True

    def identifier_is_valid(self, choice: str):
        if not choice[0:2].isupper() or not choice[2:].isdigit() or len(choice) != 7:
            return False
        return True

    def integer_is_valid(self, choice: str):
        if not choice.isdigit():
            return False
        return True

    def round_is_valid(self, choice: str):
        if not self.integer_is_valid(choice):
            return False
        choice = int(choice)
        if choice <= 0 or choice > 10:
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
