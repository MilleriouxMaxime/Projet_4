from models.player import Player


class Match:
    def __init__(
        self,
        player1: Player,
        score1: int,
        player2: Player,
        score2: int,
    ):
        self.player1 = player1
        self.score1 = score1
        self.player2 = player2
        self.score2 = score2

    def __repr__(self):
        return f"{self.player1} {self.score1} - {self.score2} {self.player2}"

    def to_dict(self):
        return {
            "player1": self.player1.to_dict(),
            "score1": self.score1,
            "player2": self.player2.to_dict(),
            "score2": self.score2,
        }
