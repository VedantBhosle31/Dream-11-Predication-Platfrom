import pandas as pd
import yaml

import os
import time
import numpy as np
import warnings
import math
import json

warnings.filterwarnings("ignore")  # Hide messy Numpy warnings


def extract_details(filename):
    dict = yaml.load(open(filename),yaml.Loader)
    flag = False
    
    match_details = {}
    try:
        match_details['venue_name'] = dict['info']['venue']
    except:
        match_details['venue_name'] = ""
    try: 
        match_details['format'] = dict['info']['match_type']    
    except:
        match_details['format'] = ""
    try:
        match_details['city'] = dict['info']['city']
    except:
        match_details['city'] = ""
    try:
        match_details['date'] = dict['info']['dates'][0]
    except:
        match_details['date'] = ""
    try:
        match_details['team1'] = dict['info']['teams'][0]
    except:
        match_details['team1'] = ""
    try:
        match_details['team2'] = dict['info']['teams'][1]
    except:
        match_details['team2'] = ""
    try:
        match_details['match_id'] = dict['info']['match_type_number']   
    except:
        match_details['match_id'] = ""
    
    if dict['info']['toss']['winner'] == match_details['team1']:
        if dict['info']['toss']['decision'] == 'bat':
            match_details['bat_first'] = [match_details['team1'],match_details['team2']]
            toss = 1
        else:
            match_details['bat_first'] = [match_details['team2'],match_details['team1']]
    else:
        if dict['info']['toss']['decision'] == 'bat':
            match_details['bat_first'] = [match_details['team2'],match_details['team1']]
            toss = 1
        else:
            match_details['bat_first'] = [match_details['team1'],match_details['team2']]
    
    # batsman','bowler','runs','dots','4s','6s','balls_involved','balls','not_out'
    
    matchup = {}
    
    innings1 = dict['innings'][0]['1st innings']['deliveries']
    for ball in innings1:
        for delivery in ball:
            
            batsman = ball[delivery]['batsman']
            bowler = ball[delivery]['bowler']

            if (batsman, bowler) not in matchup:
                matchup[(batsman, bowler)] = {}
                matchup[(batsman, bowler)]['batsman'] = batsman
                matchup[(batsman, bowler)]['bowler'] = bowler
                matchup[(batsman, bowler)]['runs'] = 0
                matchup[(batsman, bowler)]['dots'] = 0
                matchup[(batsman, bowler)]['4s'] = 0
                matchup[(batsman, bowler)]['6s'] = 0
                matchup[(batsman, bowler)]['balls_involved'] = 0
                matchup[(batsman, bowler)]['balls'] = 0
                matchup[(batsman, bowler)]['notout'] = 1
                matchup[(batsman, bowler)]['bowledlbw'] = 0
                matchup[(batsman, bowler)]['maidens'] = 0
                matchup[(batsman, bowler)]['batsman_team'] = match_details['bat_first'][0]
                matchup[(batsman, bowler)]['bowler_team'] = match_details['bat_first'][1]
            
            matchup[(batsman, bowler)]['runs'] += ball[delivery]['runs']['batsman']
            matchup[(batsman, bowler)]['dots'] += ball[delivery]['runs']['total'] == 0
            matchup[(batsman, bowler)]['4s'] += ball[delivery]['runs']['batsman'] == 4
            matchup[(batsman, bowler)]['6s'] += ball[delivery]['runs']['batsman'] == 6
            matchup[(batsman, bowler)]['balls_involved'] += ball[delivery]['runs']['batsman'] != 0
            matchup[(batsman, bowler)]['balls'] += 1
            
            ball_no, over_no = math.modf(delivery)
            if abs(ball_no - 0.1) < 1e-6:
                runs_this_over = 0
            runs_this_over += ball[delivery]['runs']['total']
            if abs(ball_no - 0.6) < 1e-6:
                if runs_this_over == 0:
                    matchup[(batsman, bowler)]['maidens'] += 1
            
            if 'wicket' in ball[delivery]:
                try:
                    if ball[delivery]['wicket']['player_out'] == batsman:
                        matchup[(batsman, bowler)]['notout'] = 0 
                        if ball[delivery]['wicket']['kind'] == 'lbw' or ball[delivery]['wicket']['kind'] == 'bowled':
                            matchup[(batsman, bowler)]['bowledlbw'] += 1 
                except Exception as e:
                    # print("hi")
                    pass
    try:
        innings2 = dict['innings'][1]['2nd innings']['deliveries']
    except:
        flag = True
    else:
        for ball in innings2:
            for delivery in ball:
                
                batsman = ball[delivery]['batsman']
                bowler = ball[delivery]['bowler']

                if (batsman, bowler) not in matchup:
                    matchup[(batsman, bowler)] = {}
                    matchup[(batsman, bowler)]['batsman'] = batsman
                    matchup[(batsman, bowler)]['bowler'] = bowler
                    matchup[(batsman, bowler)]['runs'] = 0
                    matchup[(batsman, bowler)]['dots'] = 0
                    matchup[(batsman, bowler)]['4s'] = 0
                    matchup[(batsman, bowler)]['6s'] = 0
                    matchup[(batsman, bowler)]['balls_involved'] = 0
                    matchup[(batsman, bowler)]['balls'] = 0
                    matchup[(batsman, bowler)]['notout'] = 1
                    matchup[(batsman, bowler)]['bowledlbw'] = 0
                    matchup[(batsman, bowler)]['maidens'] = 0
                    matchup[(batsman, bowler)]['batsman_team'] = match_details['bat_first'][1]
                    matchup[(batsman, bowler)]['bowler_team'] = match_details['bat_first'][0]
                
                matchup[(batsman, bowler)]['runs'] += ball[delivery]['runs']['batsman']
                matchup[(batsman, bowler)]['dots'] += ball[delivery]['runs']['total'] == 0
                matchup[(batsman, bowler)]['4s'] += ball[delivery]['runs']['batsman'] == 4
                matchup[(batsman, bowler)]['6s'] += ball[delivery]['runs']['batsman'] == 6
                matchup[(batsman, bowler)]['balls_involved'] += ball[delivery]['runs']['batsman'] != 0
                matchup[(batsman, bowler)]['balls'] += 1
                
                ball_no, over_no = math.modf(delivery)
                if abs(ball_no - 0.1) < 1e-6:
                    runs_this_over = 0
                runs_this_over += ball[delivery]['runs']['total']
                if abs(ball_no - 0.6) < 1e-6:
                    if runs_this_over == 0:
                        matchup[(batsman, bowler)]['maidens'] += 1
                
                if 'wicket' in ball[delivery]:
                    try:
                        if ball[delivery]['wicket']['player_out'] == batsman:
                            matchup[(batsman, bowler)]['notout'] = 0 
                            if ball[delivery]['wicket']['kind'] == 'lbw' or ball[delivery]['wicket']['kind'] == 'bowled':
                                matchup[(batsman, bowler)]['bowledlbw'] += 1
                    except:
                        # print("ho")
                        pass
                    
    try:
        innings3 = dict['innings'][2]['3rd innings']['deliveries']
    except:
        flag = True
    else:
        for ball in innings3:
            for delivery in ball:
                
                batsman = ball[delivery]['batsman']
                bowler = ball[delivery]['bowler']

                if (batsman, bowler) not in matchup:
                    matchup[(batsman, bowler)] = {}
                    matchup[(batsman, bowler)]['batsman'] = batsman
                    matchup[(batsman, bowler)]['bowler'] = bowler
                    matchup[(batsman, bowler)]['runs'] = 0
                    matchup[(batsman, bowler)]['dots'] = 0
                    matchup[(batsman, bowler)]['4s'] = 0
                    matchup[(batsman, bowler)]['6s'] = 0
                    matchup[(batsman, bowler)]['balls_involved'] = 0
                    matchup[(batsman, bowler)]['balls'] = 0
                    matchup[(batsman, bowler)]['notout'] = 1
                    matchup[(batsman, bowler)]['bowledlbw'] = 0
                    matchup[(batsman, bowler)]['maidens'] = 0
                    matchup[(batsman, bowler)]['batsman_team'] = match_details['bat_first'][0]
                    matchup[(batsman, bowler)]['bowler_team'] = match_details['bat_first'][1]
                
                matchup[(batsman, bowler)]['runs'] += ball[delivery]['runs']['batsman']
                matchup[(batsman, bowler)]['dots'] += ball[delivery]['runs']['total'] == 0
                matchup[(batsman, bowler)]['4s'] += ball[delivery]['runs']['batsman'] == 4
                matchup[(batsman, bowler)]['6s'] += ball[delivery]['runs']['batsman'] == 6
                matchup[(batsman, bowler)]['balls_involved'] += ball[delivery]['runs']['batsman'] != 0
                matchup[(batsman, bowler)]['balls'] += 1
                
                ball_no, over_no = math.modf(delivery)
                if abs(ball_no - 0.1) < 1e-6:
                    runs_this_over = 0
                runs_this_over += ball[delivery]['runs']['total']
                if abs(ball_no - 0.6) < 1e-6:
                    if runs_this_over == 0:
                        matchup[(batsman, bowler)]['maidens'] += 1
                
                if 'wicket' in ball[delivery]:
                    try:
                        if ball[delivery]['wicket']['player_out'] == batsman:
                            matchup[(batsman, bowler)]['notout'] = 0 
                            if ball[delivery]['wicket']['kind'] == 'lbw' or ball[delivery]['wicket']['kind'] == 'bowled':
                                matchup[(batsman, bowler)]['bowledlbw'] += 1 
                    except Exception as e:
                        # print("hi")
                        pass
    
    try:
        innings4 = dict['innings'][1]['2nd innings']['deliveries']
    except:
        flag = True
    else:
        for ball in innings4:
            for delivery in ball:
                
                batsman = ball[delivery]['batsman']
                bowler = ball[delivery]['bowler']

                if (batsman, bowler) not in matchup:
                    matchup[(batsman, bowler)] = {}
                    matchup[(batsman, bowler)]['batsman'] = batsman
                    matchup[(batsman, bowler)]['bowler'] = bowler
                    matchup[(batsman, bowler)]['runs'] = 0
                    matchup[(batsman, bowler)]['dots'] = 0
                    matchup[(batsman, bowler)]['4s'] = 0
                    matchup[(batsman, bowler)]['6s'] = 0
                    matchup[(batsman, bowler)]['balls_involved'] = 0
                    matchup[(batsman, bowler)]['balls'] = 0
                    matchup[(batsman, bowler)]['notout'] = 1
                    matchup[(batsman, bowler)]['bowledlbw'] = 0
                    matchup[(batsman, bowler)]['maidens'] = 0
                    matchup[(batsman, bowler)]['batsman_team'] = match_details['bat_first'][1]
                    matchup[(batsman, bowler)]['bowler_team'] = match_details['bat_first'][0]
                
                matchup[(batsman, bowler)]['runs'] += ball[delivery]['runs']['batsman']
                matchup[(batsman, bowler)]['dots'] += ball[delivery]['runs']['total'] == 0
                matchup[(batsman, bowler)]['4s'] += ball[delivery]['runs']['batsman'] == 4
                matchup[(batsman, bowler)]['6s'] += ball[delivery]['runs']['batsman'] == 6
                matchup[(batsman, bowler)]['balls_involved'] += ball[delivery]['runs']['batsman'] != 0
                matchup[(batsman, bowler)]['balls'] += 1
                
                ball_no, over_no = math.modf(delivery)
                if abs(ball_no - 0.1) < 1e-6:
                    runs_this_over = 0
                runs_this_over += ball[delivery]['runs']['total']
                if abs(ball_no - 0.6) < 1e-6:
                    if runs_this_over == 0:
                        matchup[(batsman, bowler)]['maidens'] += 1
                
                if 'wicket' in ball[delivery]:
                    try:
                        if ball[delivery]['wicket']['player_out'] == batsman:
                            matchup[(batsman, bowler)]['notout'] = 0 
                            if ball[delivery]['wicket']['kind'] == 'lbw' or ball[delivery]['wicket']['kind'] == 'bowled':
                                matchup[(batsman, bowler)]['bowledlbw'] += 1
                    except:
                        # print("ho")
                        pass
    
    return match_details, matchup

def func(gender, location, formats, matchid_mapping):

    files = pd.read_csv(location)
    grouped = files.groupby('format')

    j = -1
    for format in formats:
        if format[0] == 'W':
            form = format[1:]
        else:
            form = format
        date_file_pair = (grouped.get_group(form))['filename']

        matchups = pd.DataFrame(columns=['date','match_id','batsman_name','batsman_id','bowler_name','bowler_id',
                                        'balls','balls_involved','runs','strike_rate','economy',
                                        '6s','4s','got_out','maidens',
                                        'previous_innings_head_to_head','previous_runs','previous_4s','previous_6s','previous_avg_strike_rate','previous_average','previous_wickets','previous_maidens','previous_economy',
                                        'batsman_team','bowler_team']
                                )

        count = -1

        total_runs = {}
        total_balls = {}
        total_6s = {}
        total_4s = {}
        total_maidens = {}
        total_innings = {}
        wickets = {}

        print('To process ' + str(len(date_file_pair)) + ' files for ' + format)
        j += 1
        i = matchid_mapping[j]
        for ele in date_file_pair:
            i += 1
            if i%10 == 0:
                print(i - matchid_mapping[j])
                # break
            
            location = os.path.join('data','raw','cricsheet_data','all_'+gender,ele)
            match_details, matchup = extract_details(location)
            for key,headtohead in matchup.items():
                count += 1
                
                if key not in total_runs:
                    total_runs[key] = 0
                if key not in total_runs:
                    total_runs[key] = 0
                if key not in total_balls:
                    total_balls[key] = 0
                if key not in total_4s:
                    total_4s[key] = 0
                if key not in total_6s:
                    total_6s[key] = 0
                if key not in wickets:
                    wickets[key] = 0
                if key not in total_innings:
                    total_innings[key] = 0
                if key not in total_maidens:
                    total_maidens[key] = 0
                
                matchups.loc[count, 'date'] = match_details['date']
                matchups.loc[count, 'batsman_name'] = headtohead['batsman']
                matchups.loc[count, 'bowler_name'] = headtohead['bowler']
                matchups.loc[count, 'balls'] = headtohead['balls']
                matchups.loc[count, 'balls_involved'] = headtohead['balls_involved']
                matchups.loc[count, 'runs'] = headtohead['runs']
                matchups.loc[count, '4s'] = headtohead['4s']
                matchups.loc[count, '6s'] = headtohead['6s']
                matchups.loc[count, 'batsman_team'] = headtohead['batsman_team']
                matchups.loc[count, 'bowler_team'] = headtohead['bowler_team']
                matchups.loc[count, 'got_out'] = (headtohead['notout'] == 0) + 0
                matchups.loc[count, 'strike_rate'] = headtohead['runs'] * 100 / headtohead['balls']
                matchups.loc[count, 'economy'] = headtohead['runs'] * 6 / headtohead['balls']
                matchups.loc[count, 'match_id'] = i
                
                
                matchups.loc[count, 'previous_wickets'] = wickets[key]
                matchups.loc[count, 'previous_runs'] = total_runs[key]
                matchups.loc[count, 'previous_4s'] = total_4s[key]
                matchups.loc[count, 'previous_6s'] = total_6s[key]
                if total_balls[key] == 0:
                    matchups.loc[count, 'previous_avg_strike_rate'] = total_runs[key]
                else:
                    matchups.loc[count, 'previous_avg_strike_rate'] = total_runs[key] * 100 / total_balls[key]
                try:
                    matchups.loc[count, 'previous_average'] = total_runs[key] / wickets[key]
                except:
                    matchups.loc[count, 'previous_average'] = total_runs[key]
                matchups.loc[count, 'previous_innings_head_to_head'] = total_innings[key]
                matchups.loc[count, 'previous_maidens'] = total_maidens[key]
                matchups.loc[count, 'previous_economy'] = (total_runs[key] * 6 / total_balls[key]) if total_balls[key] != 0 else 0
                matchups.loc[count, 'maidens'] = headtohead['maidens']
                
                
                wickets[key] += headtohead['notout'] == 0
                total_runs[key] += headtohead['runs']
                total_balls[key] += headtohead['balls']
                total_maidens[key] += headtohead['maidens']
                total_4s[key] += headtohead['4s']
                total_6s[key] += headtohead['6s']
                total_innings[key] += 1
                

        # UNCOMMENT TO ADD IDS
        location = os.path.join('data','raw','additional_data','people_with_images_and_countries.csv')
        mapping = pd.read_csv(location)

        for i in range(len(matchups)):
            name = matchups.iloc[i]['batsman_name']
            matched = mapping[mapping['unique_name'] == name]
            if not matched.empty:
                matchups.iloc[i, matchups.columns.get_loc('batsman_id')] = matched['identifier'].values[0]
            else:
                # print(f"No matching entry for {name}: {len(mapping[mapping['unique_name'] == name])} matches")
                matchups.iloc[i, matchups.columns.get_loc('batsman_id')] = 'xxxxxxxx'
            
            name = matchups.iloc[i]['bowler_name']
            matched = mapping[mapping['unique_name'] == name]
            if not matched.empty:
                matchups.iloc[i, matchups.columns.get_loc('bowler_id')] = matched['identifier'].values[0]
            else:
                # print(f"No matching entry for {name}: {len(mapping[mapping['unique_name'] == name])} matches")
                matchups.iloc[i, matchups.columns.get_loc('bowler_id')] = 'xxxxxxxx'
            
        folder = os.path.join('data','processed',format)
        os.makedirs(folder, exist_ok=True)
        file_name = 'matchups.csv'
        matchups.to_csv(os.path.join(folder, file_name))        
        
    return

import argparse

def main():
    parser = argparse.ArgumentParser(description="Process some inputs.")

    parser.add_argument("name", type=str, help="type of processing")
    args = parser.parse_args()
    
    if args.name == 'male_t20':
        location = os.path.join('data','interim','sorted_acc_to_date_and_format_male.csv')
        formats = ['T20']
        matchid_mapping = [10000]
        func('male',location,formats,matchid_mapping)
    elif args.name == 'male_others':
        location = os.path.join('data','interim','sorted_acc_to_date_and_format_male.csv')
        formats = ['ODI', 'MDM', 'ODM','Test','IT20']
        matchid_mapping = [20000, 30000, 40000, 50000, 60000]
        func('male',location,formats,matchid_mapping)
    elif args.name == 'female':
        location = os.path.join('data','interim','sorted_acc_to_date_and_format_female.csv')
        formats = ['WT20', 'WODI','WODM','WTest','WIT20']
        matchid_mapping = [70000, 75000, 80000, 85000, 90000]
        func('female',location,formats,matchid_mapping)
        

if __name__ == "__main__":
    main()