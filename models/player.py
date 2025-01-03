class Player:
    """
    Classe représentant un joueur
    """

    def __init__(self, last_name, first_name, birth_date, identifier):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.identifier = identifier

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def to_dict(self):
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "identifier": self.identifier,
        }
