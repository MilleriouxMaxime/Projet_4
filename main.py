from controllers.menu_controller import MenuController
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from models.match import Match
from models.player import Player
from models.round import Round
from models.tournament import Tournament
from views.base_view import BaseView


def main():

    # player1 = Player("Millérioux", "Maxime", "05/08/1995", "AB12345")

    # player2 = Player("Smith", "John", "07/02/1991", "CD67890")

    # player3 = Player("Black", "Elene", "17/08/1995", "EF12345")

    # player4 = Player("Green", "Stephane", "10/02/1991", "GH67890")

    # match1 = Match(player1.identifier, 0, player2.identifier, 0)

    # match2 = Match(player3.identifier, 0, player4.identifier, 0)

    # match3 = Match(player1.identifier, 0, player3.identifier, 0)

    # match4 = Match(player2.identifier, 0, player4.identifier, 0)

    # round1 = Round([match1, match2], "Round 1", "05/08/2023", "05/08/2023")
    # round2 = Round([match3, match4], "Round 2", "05/08/2023", "05/08/2023")

    # tournament1 = Tournament(
    #     "Tournoi de Paris",
    #     "Paris",
    #     "05/08/2023",
    #     "05/08/2023",
    #     0,
    #     [round1, round2],
    #     [],
    #     "Tournoi de tennis",
    #     2,
    # )

    # print(tournament1.to_dict())
    view = BaseView()

    menu_manager = MenuController(view)
    menu_manager.run()


if __name__ == "__main__":
    main()
