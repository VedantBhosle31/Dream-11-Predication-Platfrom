from players.models import (
    BatterIt20, BatterMdm, BatterOdi, BatterOdm, BatterTest, BatterT20,
    BatterWit20, BatterWodi, BatterWodm, BatterWt20, BatterWtest,
    BowlerIt20, BowlerMdm, BowlerOdi, BowlerOdm, BowlerTest, BowlerT20,
    BowlerWit20, BowlerWodi, BowlerWodm, BowlerWt20, BowlerWtest,
    FielderIt20, FielderMdm, FielderOdi, FielderOdm, FielderTest, FielderT20,
    FielderWit20, FielderWodi, FielderWodm, FielderWt20, FielderWtest,
    MatchupIt20, MatchupMdm, MatchupOdi, MatchupOdm, MatchupT20, MatchupTest,
    MatchupWit20, MatchupWodi, MatchupWodm, MatchupWt20, MatchupWtest,
    PlayerNames, TeamDetails, FantasyBowl7
)


def model_mapping(name):
    models = {
        'BatterOdi': BatterOdi,
        'BatterIt20': BatterIt20,
        'BatterMdm': BatterMdm,
        'BatterOdm': BatterOdm,
        'BatterTest': BatterTest,
        'BatterWit20': BatterWit20,
        'BatterWodi': BatterWodi,
        'BatterWodm': BatterWodm,
        'BatterWt20': BatterWt20,
        'BatterWtest': BatterWtest,
        'BatterT20': BatterT20,
        'BowlerOdi': BowlerOdi,
        'BowlerIt20': BowlerIt20,
        'BowlerMdm': BowlerMdm,
        'BowlerOdm': BowlerOdm,
        'BowlerTest': BowlerTest,
        'BowlerT20': BowlerT20,
        'BowlerWit20': BowlerWit20,
        'BowlerWodi': BowlerWodi,
        'BowlerWodm': BowlerWodm,
        'BowlerWt20': BowlerWt20,
        'BowlerWtest': BowlerWtest,
        'FielderOdi': FielderOdi,
        'FielderIt20': FielderIt20,
        'FielderMdm': FielderMdm,
        'FielderOdm': FielderOdm,
        'FielderTest': FielderTest,
        'FielderT20': FielderT20,
        'FielderWit20': FielderWit20,
        'FielderWodi': FielderWodi,
        'FielderWodm': FielderWodm,
        'FielderWt20': FielderWt20,
        'FielderWtest': FielderWtest,
        'MatchupIt20': MatchupIt20,
        'MatchupMdm': MatchupMdm,
        'MatchupOdi': MatchupOdi,
        'MatchupOdm': MatchupOdm,
        'MatchupT20': MatchupT20,
        'MatchupTest': MatchupTest,
        'MatchupWit20': MatchupWit20,
        'MatchupWodi': MatchupWodi,
        'MatchupWodm': MatchupWodm,
        'MatchupWt20': MatchupWt20,
        'MatchupWtest': MatchupWtest,
        'PlayerNames': PlayerNames,
        'TeamDetails': TeamDetails,
        'FantasyBowl7': FantasyBowl7
    }
    return models.get(name)

def get_player_stats(name,match_date,format):
    '''
        take player_name and format(type of match + gender)
        get the mapped mapped model and use it to get relevant stats 
    '''
    model_batter = model_mapping("Batter" + format)
    model_bowler = model_mapping("Bowler" + format)
    model_fielder = model_mapping("Fielder"+format) 
    stats ={}
    stats["batting"] = list(model_batter.objects.filter(player_name=name, date__lt = match_date).order_by('-date')[:10].values('player_name','previous_average','previous_strike_rate','innings_played','previous_runs','previous_average','previous_4s','previous_6s','previous_runs','previous_fifties','previous_centuries','highest_score','form','venue_avg','opposition','previous_zeros','tbahs_economy_agg', 'tbahs_4s_agg', 'tbahp_dismissals_agg', 'dots', 'venue', 'previous_average', f'{format.lower()}_match_fantasy_points', 'venue_avg', 'opposition', 'form', 'consistency', 'previous_balls_involved', 'tbahs_economy_agg', 'tbahp_economy_agg', 'tbahs_4s_agg', 'tbahp_4s_agg', 'tbahs_dismissals_agg', 'dots', 'venue', 'previous_average', f'{format.lower()}_match_fantasy_points', 'venue_avg', 'opposition', 'form', 'consistency', 'previous_balls_involved', 'tbahs_6s_agg', 'tbahp_6s_agg', 'tbahs_economy_1', 'tbahp_economy_1', 'tbahs_4s_1', 'tbahs_6s_1', 'tbahp_4s_1', 'tbahp_6s_1', 'tbahs_dismissals_1', 'tbahp_dismissals_1', 'tbahs_economy_2', 'tbahp_economy_2', 'tbahs_4s_2', 'tbahs_6s_2', 'tbahp_4s_2', 'tbahp_6s_2', 'tbahs_dismissals_2', 'tbahp_dismissals_2', 'tbahs_economy_3', 'tbahp_economy_3', 'tbahs_4s_3', 'tbahs_6s_3', 'tbahp_4s_3', 'tbahp_6s_3', 'tbahs_dismissals_3', 'tbahp_dismissals_3', 'tbahr_economy_agg', 'date'))
    stats["bowling"] = list(model_bowler.objects.filter(player_name=name, date__lt = match_date).order_by('-date')[:10].values('previous_wickets','previous_economy','previous_balls_involved','innings_played','previous_strike_rate','previous_maidens','previous_average', 'consistency','venue','form','opposition', 'date'))
    stats["fielding"] = list(model_fielder.objects.filter(player_name=name, date__lt = match_date).order_by('-date')[:10].values('pfa_catches','pfa_stumpings','pfa_runouts', 'previous_stumpings', 'previous_runouts', 'previous_catches','previous_stumpings',"previous_catches","previous_runouts", 'date'))
    return stats

def matchup_stats_two_players(player_1, player_2, format, match_date):
    matchUp = model_mapping(f"Matchup{format}")
    
    def fetch_stats(batsman, bowler):
        return (
            matchUp.objects.filter(
                batsman_name=batsman, bowler_name=bowler, date__lt=match_date
            )
            .order_by('-date')
            .values('previous_runs', 'previous_wickets', 'previous_avg_strike_rate')
            .first()
        )
    
    stats = fetch_stats(player_1, player_2)
    if not stats:
        stats = fetch_stats(player_2, player_1)
    
    return stats

def matchup_stats(player_name,opponents_list,format,match_date):
    stats = {}
    for opponent in opponents_list:
        stats[opponent] = matchup_stats_two_players(player_1=player_name,player_2=opponent,format=format,match_date=match_date)
    return stats
    
def player_features(name,match_date,format):
    model_batter = model_mapping("Batter" + format)
    model_bowler = model_mapping("Bowler" + format)
    model_fielder = model_mapping("Fielder"+format) 

    stats ={}
    stats["batting"] = model_batter.objects.filter(player_name=name, date__lt = match_date).order_by('-date').values().first()
    stats["bowling"] = model_bowler.objects.filter(player_name=name, date__lt = match_date).order_by('-date').values().first()
    stats["fielding"] = model_fielder.objects.filter(player_name=name, date__lt = match_date).order_by('-date').values().first()
    return stats

def fetch_all_player_features(player_names, match_date, format):
    model_batter = model_mapping("Batter" + format)
    model_bowler = model_mapping("Bowler" + format)
    model_fielder = model_mapping("Fielder" + format)

    # Fetch all data in one query per model
    batter_data = model_batter.objects.filter(
        player_name__in=player_names, date__lt=match_date
    ).order_by('-date').values()
    
    bowler_data = model_bowler.objects.filter(
        player_name__in=player_names, date__lt=match_date
    ).order_by('-date').values()
    
    fielder_data = model_fielder.objects.filter(
        player_name__in=player_names, date__lt=match_date
    ).order_by('-date').values()
    
    # Organize data by player name for easy lookup
    batter_dict = {}
    for entry in batter_data:
        if entry["player_name"] not in batter_dict:
            batter_dict[entry["player_name"]] = entry

        if len(batter_dict) == len(player_names):
            break

    bowler_dict = {}
    for entry in bowler_data:
        if entry["player_name"] not in bowler_dict:
            bowler_dict[entry["player_name"]] = entry
        
        if len(bowler_dict) == len(player_names):
            break

    fielder_dict = {}
    for entry in fielder_data:
        if entry["player_name"] not in fielder_dict:
            fielder_dict[entry["player_name"]] = entry

        if len(fielder_dict) == len(player_names):
            break
        

    # Combine data for each player
    player_stats = {}
    for name in player_names:
        player_stats[name] = {
            "batting": batter_dict.get(name),
            "bowling": bowler_dict.get(name),
            "fielding": fielder_dict.get(name),
        }

    return player_stats