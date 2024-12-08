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
        round_number=4,
    ):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.current_round = current_round
        self.rounds_list = rounds_list
        self.players_list = players_list
        self.description = description
        self.round_number = round_number
