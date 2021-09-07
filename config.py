import tomli

# Loads "UltraEmu.conf" and parses it to create a list of each repository named "repos".
# It also creates variable "repos_len" that states the number of repos
with open("UltraEmu.conf", "rb") as config:
    config = tomli.load(config)


repos = config["repositories"]
repos_len = len(repos)
theme = config["theme"][0]
theme_style = config["theme"][1]
top_game_1_PS3 = [config['top_games_PS3'][0][0], config['top_games_PS3'][0][1], config['top_games_PS3'][0][2], config['top_games_PS3'][0][3]]
top_game_2_PS3 = [config['top_games_PS3'][1][0], config['top_games_PS3'][1][1], config['top_games_PS3'][1][2], config['top_games_PS3'][1][3]]
top_game_3_PS3 = [config['top_games_PS3'][2][0], config['top_games_PS3'][2][1], config['top_games_PS3'][2][2], config['top_games_PS3'][2][3]]
top_game_4_PS3 = [config['top_games_PS3'][3][0], config['top_games_PS3'][3][1], config['top_games_PS3'][3][2], config['top_games_PS3'][3][3]]
top_game_5_PS3 = [config['top_games_PS3'][4][0], config['top_games_PS3'][4][1], config['top_games_PS3'][4][2], config['top_games_PS3'][4][3]]
recommended_games_PS3_simulation = [config["recommended_games_PS3_simulation"][0], config["recommended_games_PS3_simulation"][1], config["recommended_games_PS3_simulation"][2], config["recommended_games_PS3_simulation"][3], config["recommended_games_PS3_simulation"][4], config["recommended_games_PS3_simulation"][5], config["recommended_games_PS3_simulation"][6], config["recommended_games_PS3_simulation"][7], config["recommended_games_PS3_simulation"][8], config["recommended_games_PS3_simulation"][9], config["recommended_games_PS3_simulation"][10], config["recommended_games_PS3_simulation"][11], config["recommended_games_PS3_simulation"][12], config["recommended_games_PS3_simulation"][13], config["recommended_games_PS3_simulation"][14], config["recommended_games_PS3_simulation"][15], config["recommended_games_PS3_simulation"][16], config["recommended_games_PS3_simulation"][17], config["recommended_games_PS3_simulation"][18], config["recommended_games_PS3_simulation"][19], config["recommended_games_PS3_simulation"][20], config["recommended_games_PS3_simulation"][21], config["recommended_games_PS3_simulation"][22], config["recommended_games_PS3_simulation"][23]]
if config["auto_update"] == "true":
    auto_update = True
else:
    auto_update = False
