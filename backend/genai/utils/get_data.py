impor
def get_data(player_type, player_id, format):
    '''
        take player_name and format(type of match
    '''
    
    batter_player_data_json= {
      "player_name": "Virat Kohli",
      "player_id": player_id,
      "player_type": "Batter",
      "bowlerwise_matchups": [
        {
          "bowler": "Mitchell Starc",
          "bowler_type": "left arm fast",
          "runs": 300,
          "balls_faced": 250,
          "average": 33.3,
          "strike_rate": 60.5,
          "dismissals": 4,
          "boundary_percentage": 16.2
        },
        {
          "bowler": "James Anderson",
          "bowler_type": "right arm fast",
          "runs": 250,
          "balls_faced": 220,
          "average": 30.0,
          "strike_rate": 55.3,
          "dismissals": 3,
          "boundary_percentage": 12.5
        },
        {
          "bowler": "Nathan Lyon",
          "bowler_type": "right arm off spin",
          "runs": 300,
          "balls_faced": 250,
          "average": 33.3,
          "strike_rate": 60.5,
          "dismissals": 4,
          "boundary_percentage": 16.2
        }
      ],
      "fielding_stats": {
        "catches_per_game": 1.6,
        "runouts_per_game": 0.4,
        "stumpings_per_game": 0,
        "total_dismissals": 60
      },
      "batter_indices": {
        "consistency": 87,
        "venue": 80,
        "form": 56,
        "opposition": 77.8
      },
      "opposition": {
        "opposition_team_name": "Australia",
        "average": 52.3,
        "strike_rate": 87.5,
        "runs": 1200,
        "matches": 24
      },
      "historical_data": {
        "total_runs": 12345,
        "total_matches": 250,
        "total_fifties": 45,
        "total_hundreds": 20,
        "highest_score": 189,
        "average": 53.4,
        "average_against_spin": 55,
        "strike_rate_against_spin": 155,
        "strike_rate_against_pace": 125,
        "average_against_pace": 20,
        "strike_rate": 87.6,
        "boundary_percentage": 15.1
      }
    }
