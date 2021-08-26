from bot import *

print("---[Skribbl.io Bot v.1]---")
player_name = input("Player: ")
game_url = input("URL: ")
bot = Bot(player_name.strip() ,game_url.strip())