import json

def get_player_data(player_id, player_data_path):
    with open(player_data_path) as f:
        player_data = json.load(f)
    
    