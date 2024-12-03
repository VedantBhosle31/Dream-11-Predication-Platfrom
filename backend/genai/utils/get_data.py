import players.utils.player_service as player_service
from genai.utils.db import db

db = db()

def batter_data( player_name, date, model, player_opponents, player_type):
    player_data = player_service.get_player_data(player_name,date,model)
    matchups = db['matchup'][model.upper()].objects.filter(
        batsman_name=player_name,
        bowler_name__in=player_opponents,
        date__lt=date
        ).order_by('-date').values('bowler_name', 'runs', 'previous_runs', 'previous_wickets', 'previous_avg_strike_rate', 'previous_innings_head_to_head', 'previous_4s', 'previous_6s').first()
    
    matchups_data = list(matchups)
    data = {
        'player_name': player_name,
        "player_type": player_type,
        'bowlerwise_matchups' : matchups_data,
        "fielding_stats": {
            "catches_per_game": player_data['fielding']['pfa_catches'],
            "runouts_per_game": player_data['fielding']['pfa_runouts'],
            "stumpings_per_game": player_data['fielding']['pfa_stumpings'],
            "total_dismissals": 60
             },
        "batter_indices": {
                "consistency": player_data['batting']['consistency'],
                "venue": player_data['batting']['venue'],
                "form": player_data['batting']['form'],
                "opposition": player_data['batting']['opposition'],
                },
        "historical_data": {
            "total_runs": player_data['batting']['previous_runs'],
            "total_matches": player_data['batting']['innings_played'],
            "total_fifties": player_data['batting']['previous_fifties'],
            "total_hundreds": player_data['batting']['previous_centuries'],
            "highest_score": player_data['batting']['highest_score'],
            "average": player_data['batting']['previous_average'],
            "average_against_spin": player_data['batting']['tbahs_economy_agg']*100,
            "strike_rate_against_spin": player_data['batting']['previous_strike_rate']*player_data['batting']['tbahr_economy_agg'],
            "strike_rate_against_pace": player_data['batting']['previous_strike_rate']/player_data['batting']['tbahp_economy_agg'],
            "average_against_pace": player_data['batting']['tbahp_economy_agg']*100,
            "career_strike_rate": player_data['batting']['previous_strike_rate'],
            "boundary_percentage": ((player_data['batting']['previous_4s']+player_data['batting']['previous_6s'])/player_data['batting']['previous_balls'])*100,
            }

    }

    
    return data

def get_data(player_type, player_name, date, model, player_opponents):
    if player_type == 'batter':
        return batter_data( player_name, date, model, player_opponents, player_type)