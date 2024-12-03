from players.models import (
    BatterIt20, BatterMdm, BatterOdi, BatterOdm, BatterTest,
    BatterWit20, BatterWodi, BatterWodm, BatterWt20, BatterWtest,
    BowlerIt20, BowlerMdm, BowlerOdi, BowlerOdm, BowlerTest,
    BowlerWit20, BowlerWodi, BowlerWodm, BowlerWt20, BowlerWtest,
    FielderIt20, FielderMdm, FielderOdi, FielderOdm, FielderTest,
    FielderWit20, FielderWodi, FielderWodm, FielderWt20, FielderWtest,
    MatchupIt20, MatchupWit20, MatchupWtest
)

def model_mapping(name):
    if name == 'BatterOdi':
        return BatterOdi
    elif name == 'BatterIt20':
        return BatterIt20
    elif name == 'BatterMdm':
        return BatterMdm
    elif name == 'BatterOdm':
        return BatterOdm
    elif name == 'BatterTest':
        return BatterTest
    elif name == 'BatterWit20':
        return BatterWit20
    elif name == 'BatterWodi':
        return BatterWodi
    elif name == 'BatterWodm':
        return BatterWodm
    elif name == 'BatterWt20':
        return BatterWt20
    elif name == 'BatterWtest':
        return BatterWtest
    elif name == 'BowlerIt20':
        return BowlerIt20
    elif name == 'BowlerMdm':
        return BowlerMdm
    elif name == 'BowlerOdi':
        return BowlerOdi
    elif name == 'BowlerOdm':
        return BowlerOdm
    elif name == 'BowlerTest':
        return BowlerTest
    elif name == 'BowlerWit20':
        return BowlerWit20
    elif name == 'BowlerWodi':
        return BowlerWodi
    elif name == 'BowlerWodm':
        return BowlerWodm
    elif name == 'BowlerWt20':
        return BowlerWt20
    elif name == 'BowlerWtest':
        return BowlerWtest
    elif name == 'FielderIt20':
        return FielderIt20
    elif name == 'FielderMdm':
        return FielderMdm
    elif name == 'FielderOdi':
        return FielderOdi
    elif name == 'FielderOdm':
        return FielderOdm
    elif name == 'FielderTest':
        return FielderTest
    elif name == 'FielderWit20':
        return FielderWit20
    elif name == 'FielderWodi':
        return FielderWodi
    elif name == 'FielderWodm':
        return FielderWodm
    elif name == 'FielderWt20':
        return FielderWt20
    elif name == 'FielderWtest':
        return FielderWtest
    elif name == 'MatchupIt20':
        return MatchupIt20
    elif name == 'MatchupWit20':
        return MatchupWit20
    elif name == 'MatchupWtest':
        return MatchupWtest
    else:
        raise ValueError(f"Unknown model name: {name}")

def get_player_stats(name,match_date,format):
    '''
        take player_name and format(type of match + gender)
        get the mapped mapped model and use it to get relevant stats 
    '''
    model_batter = model_mapping("Batter" + format)
    model_bowler = model_mapping("Bowler" + format)
    model_fielder = model_mapping("Fielder"+format) 
    stats ={}
    stats["batting"] = list(model_batter.objects.filter(player_name=name, date__lt = match_date).order_by('-date')[:10].values('player_name','previous_average','previous_strike_rate','innings_played','previous_runs','previous_average','previous_4s','previous_6s','previous_runs','previous_fifties','previous_centuries','highest_score','form','venue_avg','opposition','previous_zeros','tbahs_economy_agg', 'tbahs_4s_agg', 'tbahp_dismissals_agg', 'dots', 'venue', 'previous_average', 'odi_match_fantasy_points', 'venue_avg', 'opposition', 'form', 'consistency', 'previous_balls_involved'))

    stats["bowling"] = list(model_bowler.objects.filter(player_name=name, date__lt = match_date).order_by('-date')[:10].values('previous_wickets','previous_economy','previous_balls_involved','innings_played','previous_strik(e_rate','previous_maidens','previous_average'))
    stats["fielding"] = list(model_fielder.objects.filter(player_name=name, date__lt = match_date).order_by('-date')[:10].values('pfa_catches','pfa_stumpings','pfa_runouts', 'previous_stumpings', 'previous_runouts', 'previous_catches'))
    return stats

def matchup_stats_two_players(player_1, player_2, format, match_date):
    matchUp = model_mapping(f"Matchup{format}")
    
    def fetch_stats(batsman, bowler):
        return (
            matchUp.objects.filter(
                batsman_name=batsman, bowler_name=bowler, date__lt=match_date
            )
            .order_by('-date')
            .values('previous_runs', 'previous_wickets', 'previous_avg_strike_rate', 'balls_involved')
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

