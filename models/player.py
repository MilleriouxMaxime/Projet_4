class Player:
    def __init__(self, last_name, first_name, birth_date, identifier):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.identifier = identifier

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
