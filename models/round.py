class Round:
    def __init__(self, matchs_list, name, start_time, end_time):
        self.matchs_list = matchs_list
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"Round{self.name}, {self.matchs_list} date de début : {self.start_time}, date de fin : {self.end_time}"

    def to_dict(self):
        return {
            "matches": [match.to_dict() for match in self.matches],
            "round_number": self.round_number,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
