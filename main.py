from controllers.menu_controller import MenuController
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from models.match import Match
from models.player import Player
from models.round import Round
from models.tournament import Tournament
from views.base_view import BaseView


def main():

    view = BaseView()

    menu_manager = MenuController(view)
    menu_manager.run()


if __name__ == "__main__":
    main()
