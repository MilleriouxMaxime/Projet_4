class Match:
    def __init__(self, player1, score1, player2, score2):
        self.player1 = player1
        self.score1 = score1
        self.player2 = player2
        self.score2 = score2

    #     self.match = ([player1, score1], [player2, score2])

    def __repr__(self):
        return f"{self.player1} {self.score1} - {self.score2} {self.player2}"
