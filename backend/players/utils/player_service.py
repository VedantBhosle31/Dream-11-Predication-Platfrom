# from players.models import BatterIt20

# def get_player_stats(player_name,match_date):
#     '''
#         take player_name and format(type of match + gender)
#         get the mapped mapped model and use it to get relevant stats 
#     '''
#     model=BatterIt20
#     stats = model.objects.filter(player_name=player_name,date__lt = match_date).order_by('-date')
#     return stats