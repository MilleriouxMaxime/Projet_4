from models.player import Player
import json


class PlayerManager:

    def create_player(self):
        last_name = input("Enter last name: ")
        first_name = input("Enter first name: ")
        birth_date = input("Enter birth date: ")
        identifier = input("Enter identifier: ")
        player = Player(
            last_name,
            first_name,
            birth_date,
            identifier,
        )
