from tinydb import TinyDB, Query

# Initialiser la base de données
db = TinyDB("db.json")

# Tables pour tournois et joueurs
tournaments_table = db.table("Tournaments")
players_table = db.table("Players")
