from models.player import Player
from models.tournament import Tournament
from models.match import Match
from models.round import Round


def main():

    player1 = Player("Millérioux", "Maxime", "05/08/1995", "AB12345")

    player2 = Player("Smith", "John", "07/02/1991", "CD67890")

    player3 = Player("Black", "Elene", "17/08/1995", "EF12345")

    player4 = Player("Green", "Stephane", "10/02/1991", "GH67890")

    match1 = Match(player1, 0, player2, 0)

    match2 = Match(player3, 0, player4, 0)

    round1 = Round([match1, match2], 1, "05/08/2023", "05/08/2023")

    print(match1)


if __name__ == "__main__":
    main()
