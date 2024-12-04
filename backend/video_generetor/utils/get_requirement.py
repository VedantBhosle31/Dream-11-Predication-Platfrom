from players.utils.player_service import get_player_stats


def get_requirements_object(n, name, match_date, format, team, predictions):
    data = get_player_stats(name, match_date, format)
    
    player_type = predictions['position']
    ps = data[player_type]
    ps0 = data[player_type][0]
    basic_requirements={
        "name": name,
        "team": team,
        "expct_pts": predictions["expected_points"],
        "cost": predictions["cost"],
        "expct_runs": predictions["runs"],
        "expct_4s_and_6s": predictions["4s"] + predictions["6s"],
        "runs": predictions["runs"],
        "strike_rate": predictions["strike_rate"],
        "boundaries": predictions["4s"],
        "wickets": predictions["wickets"],
        "economy": predictions["economy"],
        "catches": predictions["catches"],
        "run_outs": predictions["runouts"],
        "form": ps0["form"],
        'player_img': "image.jpg",
        'team_symbol':"image.jpg",
    }

    basic_requirements["Matches"] = ps0["innings_played"]
    basic_requirements["cruns"] = ps0["previous_runs"]
    basic_requirements["hstrike_rate"] = ps0["previous_strike_rate"]
    basic_requirements["4s/6s"] = ps0["previous_4s"]+ps0["previous_6s"]
    basic_requirements["highest_score"] = ps0["highest_score"]
    basic_requirements["innings"] = ps0["innings_played"]
    basic_requirements["Average"] = ps0["previous_average"]
    basic_requirements["50/100"] = ps0["previous_fifties"]+ps0["previous_centuries"]


    if n == 1:
        fantasy_points_array = []
        match_dates = []
        for i in range(0, 10):
            format_lower_case = format.lower()
            # print(format_lower_case, ps[i][f"{format_lower_case}_match_fantasy_points"], i)
            if ps[i][f"{format_lower_case}_match_fantasy_points"] == None:
                fantasy_points_array.append(0)
            fantasy_points_array.append(ps[i][f"{format_lower_case}_match_fantasy_points"])
            match_dates.append(i)
        
        # print(fantasy_points_array, match_dates)
        basic_requirements["graph"] = {
            "fantasy": {
                "points": fantasy_points_array,
                "date": match_dates
            }
        }
    if n == 2:
        basic_requirements["graph"] = {
            "consistancy": [ps[0]["consistency"], ps[1]["consistency"], ps[2]["consistency"]]
        }
    if n == 3:
        vpis = []
        for i in range(1, 11):
            vpis.append(ps[i]["venue"])
        basic_requirements["graph"] = {
            "vpi": vpis
        }
    if n == 4:
        vpis = []
        for i in range(1, 11):
            vpis.append(ps[i]["venue"])
        basic_requirements["graph"] = {
            "vpi": vpis
        }

    return basic_requirements