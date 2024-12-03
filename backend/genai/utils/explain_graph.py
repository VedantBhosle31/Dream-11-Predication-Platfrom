from groq_client import generate_completion

def graph_explain(graph_name, input_data):
  # 'chart name':['description','input data description','input_data']
  graph_name_list = {'fantasy_points_vs_matches':['Chart plots fantasy points attained by the player in the last 9 matches, with the 10th point being the prediction for the current game.','Input data is fantasy points over time.','[40,70,80,50,20,10,95,60,67,78]'],
                   'spider_chart_bat':['this is a radar chart that shows the player profile of a batter using 6 cricketing metrics which are batting strike rate, batting average, wickets, economy, fielding and matchup','Input data is a score from 0-10 which is  given to all the metrics','[9,3,2,2,7,6]'],
                   'spider_chart_bowl':['this is a radar chart that shows the player profile of a bowler using 6 cricketing metrics which are batting strike rate, batting average, wickets, economy, fielding and matchup','Input data is a score from 0-10 which is  given to all the metrics','[1,3,8,9,7,6]'],
                   'spider_chart_all':['this is a radar chart that shows the player profile of an all rounder using 6 cricketing metrics which are batting strike rate, batting average, wickets, economy, fielding and matchup','Input data is a score from 0-10 which is  given to all the metrics','[7,6,7,5,7,6]'],
                   'recent_performance':['this has three progress bars which represent recent overall performance, venue performance, opposition performance of the player','input data is on a scale from 0 to 100','[65,30,95]'],
                   'matchups_bat':['this graph shows the performmance of a particular batter against 3 opposition bowlers','the inputs are bowler name, balls faced by the bowler, runs scored against the bowler, dismissals against the bowler, and batting strike rate against the bowler. There will be 3 sets of these inputs', '[Jofra Archer, 26,39,3,150; Jasprit Bumrah, 23,23,7,100; Yuzi Chahal,20,40,1,200]'],
                   'matchups_bowl':['this graph shows the performmance of a particular bowler against 3 opposition batters','the inputs are batter name, balls bowled by the bowler, runs conceded by the bowler, wickets taken by the bowler, and economy of the bowler against that batter. There will be 3 sets of these inputs', '[Virat Kohli, 26,39,3,9; Rohit Sharma, 23,23,7,6; Hardik Pandya,20,40,1,12]'],
                   'differential_exp_venue':['this is a line chart that shows that plots the last 10 venue index at the same venue, with the 10th index being the prediction for the current game. there is also a reference line which is the consistency, if the line graph is above reference the player has performed better than usual and vice versa', 'you get the 10 venue index and a reference consistency as inputs','[45,49,55,60,65,30,24,24,29,40,35]',],
                   'differential_exp_opposition':['this is a line chart that shows that plots the last 10 oppostion index at against the same opposition, with the 10th index being the prediction for the current game. there is also a reference line which is the consistency, if the line graph is above reference the player has performed better than usual and vice versa', 'you get the 10 opposition index and a reference consistency as inputs','[45,49,55,60,65,30,24,24,29,40,35]',],
                   'differential_exp_matchups':['this is a line chart that shows that plots the last 10 matchup index at against the same matchups, with the 10th index being the prediction for the current game. there is also a reference line which is the consistency, if the line graph is above reference the player has performed better than usual and vice versa', 'you get the 10 matchup index and a reference consistency as inputs','[45,49,55,60,65,30,24,24,29,40,35]',],
                   'differential_exp_form':['this is a line chart that shows that plots the last 10 form index at against the same form, with the 10th index being the prediction for the current game. there is also a reference line which is the consistency, if the line graph is above reference the player has performed better than usual and vice versa', 'you get the 10 form index and a reference consistency as inputs','[45,49,55,60,65,30,24,24,29,40,35]',],
                   'demography_bat':['it is a pie chart that represents the percentage of type of runs scored by a batter','the inputs are percentages of 0 runs,1 run,2 run, 4 run, 6 runs and others','[20,25,15,20,10,10]'],
                   'demography_bowl':['it is a pie chart that represents the percentage of type of balls bowled by a bowler','the inputs are percentages of wickets, 0 runs,1 run,2 run, bowndaries and others','[5,25,15,20,25,10]'],
                   'impact_index_overall_bat':['it is a bar chart that represents a batters performance against two types of bowlers which are spinners and pacers','the inputs are strike rate against spinner and pacer, boundaries made against spinners and pacers, wickets lost against spinner and pacer','[156.7,188.5,7,5,1,3]'],
                   'impact_index_pp_bat':['it is a bar chart that represents a batters performance against two types of bowlers which are spinners and pacers in powerplay overs','the inputs are strike rate against spinner and pacer in powerplay, boundaries made against spinners and pacers in powerplay, wickets lost against spinner and pacer in powerplay','[156.7,188.5,7,5,1,3]'],
                   'impact_index_middle_bat':['it is a bar chart that represents a batters performance against two types of bowlers which are spinners and pacers in middle overs','the inputs are strike rate against spinner and pacer in middle overs, boundaries made against spinners and pacers in middle overs, wickets lost against spinner and pacer in middle overs','[156.7,188.5,7,5,1,3]'],
                   'impact_index_death_bat':['it is a bar chart that represents a batters performance against two types of bowlers which are spinners and pacers in death overs','the inputs are strike rate against spinner and pacer in death overs, boundaries made against spinners and pacers in death overs, wickets lost against spinner and pacer in death overs','[156.7,188.5,7,5,1,3]'],
                   'impact_index_overall_bowl':['it is a bar chart that represents a bowlers performance against two types of batters which are left hand batter (LHB) and right hand batter (RHB)','the inputs are economy against LHB and RHB, boundaries conceeded against LHB and RHB, wickets gained against LHB and RHB','[6.7,8.5,7,5,1,3]'],
                   'impact_index_pp_bowl':['it is a bar chart that represents a bowlers performance against two types of batters which are left hand batter (LHB) and right hand batter (RHB) in powerplay overs','the inputs are economy against LHB and RHB in powerplay overs, boundaries conceeded against LHB and RHB in powerplay overs, wickets gained against LHB and RHB in powerplay','[6.7,8.5,7,5,1,3]'],
                   'impact_index_middle_bowl':['it is a bar chart that represents a bowlers performance against two types of batters which are left hand batter (LHB) and right hand batter (RHB) in middle overs','the inputs are economy against LHB and RHB in middle overs, boundaries conceeded against LHB and RHB in middle overs, wickets gained against LHB and RHB in middle overs','[6.7,8.5,7,5,1,3]'],
                   'impact_index_death_bowl':['it is a bar chart that represents a bowlers performance against two types of batters which are left hand batter (LHB) and right hand batter (RHB) in death overs','the inputs are economy against LHB and RHB in death overs, boundaries conceeded against LHB and RHB in death overs, wickets gained against LHB and RHB in death overs','[6.7,8.5,7,5,1,3]']
                   }
  data = []
  data.append(graph_name)
  data.append(graph_name_list[graph_name][0])
  data.append(graph_name_list[graph_name][1])
  data.append(input_data)
  prompt = '''
You are a cricket data analyst explaining a certain chart to a user.
Description of the plot and what it's input means is given, along with data_input. You have to talk about how the chart works and what can we infer about the player.
Don't just say what's there on the chart, give peroper cricketing insights. try to tell what is the nature of player and what can be expected of the player in the next game.
use all data provided to yoy dont miss anything.
lower economy is good for a bowler keep this in mind.
high strike rate is better for a batter keep this in mind.
whenever there are two similar stats compare them and tell me which case is better.
mention the strengths and weaknesses of the player from your insights.
try to comment something about all stats provided to you.
comment on the player accordingly if they are a batter or a bowler or an all rounder.
use gender neutral terms, be respectful.
when i am scoring someone, higher the number the better in all other cases use  regular convention.
try to give a definite conclusion in the end.
try not to mention anything about the bowling performance of a batter and vice versa.
higher the batting strike rate more agressive is the batter.
Always give positive resposnses like you are an expert, never say you dont know anything or you dont know the conclusion or you cant predit.
Always think you answers again before answering.
Never tell the user that something is unclear
Always pretend like you are an expert at this, be confindent dont let any user doubt you, you got this.
Chart name : {}
Description : {}
Expected kind of analysis : {}
Data given : {}


Write your explanation of the data visual concisely in 20-50 words. Do not go over the word limit. Tell the user what you conclude from the data
'''
  fantasy_points_prompt_final = prompt.format(data[0],data[1],data[2],data[3])
  generated_insight = generate_completion(fantasy_points_prompt_final)

  return generated_insight
