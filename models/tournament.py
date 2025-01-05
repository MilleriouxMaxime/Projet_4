from models.round import Round


class Tournament:
    """
    Classe représentant un tournoi
    """

    def __init__(
        self,
        name: str,
        place: str,
        start_date: str,
        end_date: str,
        current_round: int,
        rounds_list: list[Round],
        players_list: list[str],
        description: str,
        scoreboard: dict[str, int],
        total_round_number: int = 4,
        status: str = "Pas commence",
    ):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.current_round = current_round
        self.rounds_list = rounds_list
        self.players_list = players_list
        self.description = description
        self.total_round_number = total_round_number
        self.scoreboard = scoreboard
        self.status = status

    def to_dict(self):
        return {
            "name": self.name,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "current_round": self.current_round,
            "rounds_list": [round_.to_dict() for round_ in self.rounds_list],
            "players_list": self.players_list,
            "description": self.description,
            "scoreboard": self.scoreboard,
            "total_round_number": self.total_round_number,
            "status": self.status,
        }
