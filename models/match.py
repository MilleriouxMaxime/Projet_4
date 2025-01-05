class Match:
    """
    Classe représentant un match
    """

    def __init__(
        self,
        player1_id: str,
        score1: int,
        player2_id: str,
        score2: int,
    ):
        self.player1_id = player1_id
        self.score1 = score1
        self.player2_id = player2_id
        self.score2 = score2

    def to_dict(self):
        return (
            [self.player1_id, self.score1],
            [self.player2_id, self.score2],
        )
