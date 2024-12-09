import json


class Tournament:
    def __init__(
        self,
        name,
        place,
        start_date,
        end_date,
        current_round,
        rounds_list,
        players_list,
        description,
        total_round_number=4,
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

    def to_dict(self):
        return {
            "name": self.name,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "current_round": self.current_round,
            "rounds_list": [round_.to_dict() for round_ in self.rounds_list],
            "players_list": [player.to_dict() for player in self.players_list],
            "description": self.description,
            "total_round_number": self.total_round_number,
        }