from datetime import datetime

from models.match import Match


class Round:
    """
    Classe représentant un tour
    """

    def __init__(
        self,
        matchs_list: list[Match],
        name: str,
        start_time: datetime,
        end_time: datetime,
    ):
        self.matchs_list = matchs_list
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"Round{self.name}, {self.matchs_list} date de début : {self.start_time}, date de fin : {self.end_time}"

    def to_dict(self):
        return {
            "matches_list": [match.to_dict() for match in self.matchs_list],
            "name": self.name,
            "start_date": self.start_time.strftime("%Y-%m-%d %H:%M"),
            "end_date": self.end_time,
        }
