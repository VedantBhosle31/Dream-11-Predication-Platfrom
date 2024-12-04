def calculate_batsman_points_t20(runs, boundaries, sixes, strike_rate):
    batsman_points = 0

    # Balls faced calculation
    balls_faced = (runs * 100) / strike_rate

    # Runs points
    batsman_points += runs

    # Boundary points
    batsman_points += boundaries * 1  # 1 point per boundary

    # Six points
    batsman_points += sixes * 2  # 2 points per six

    # Milestones points
    if runs >= 100:
        batsman_points += 16  # 100 runs = 16 points
    elif runs >= 50:
        batsman_points += 8  # 50 runs = 8 points
    elif runs >= 30:
        batsman_points += 4  # 30 runs = 4 points

    # Duck points
    if runs == 0:
        batsman_points -= 2  # Duck = -2 points

    # Strike rate bonus points (if player faced at least 10 balls)
    if balls_faced >= 10:
        runs_per_100_balls = (runs / balls_faced) * 100
        if runs_per_100_balls > 170:
            batsman_points += 6  # Above 170 runs per 100 balls
        elif 150.01 <= runs_per_100_balls <= 170:
            batsman_points += 4  # Between 150.01 and 170 runs per 100 balls
        elif 130 <= runs_per_100_balls < 150:
            batsman_points += 2  # Between 130 and 150 runs per 100 balls
        elif 60 <= runs_per_100_balls < 70:
            batsman_points -= 2  # Between 60 and 70 runs per 100 balls
        elif 50 <= runs_per_100_balls < 60:
            batsman_points -= 4  # Between 50 and 59.99 runs per 100 balls
        elif runs_per_100_balls < 50:
            batsman_points -= 6  # Below 50 runs per 100 balls

    return batsman_points

def calculate_batsman_points_odi(runs, boundaries, sixes, strike_rate):
    batsman_points = 0

    balls_faced = (runs * 100) / strike_rate  # Calculate balls faced if not provided

    # Run points
    batsman_points += runs

    # Boundary points
    batsman_points += boundaries * 1  # 1 point per boundary

    # Six points
    batsman_points += sixes * 2  # 2 points per six

    # Half-century & Century points
    if runs >= 100:
        batsman_points += 8  # 100 runs = 8 points
    elif runs >= 50:
        batsman_points += 4  # 50 runs = 4 points

    # Duck points
    if runs == 0:
        batsman_points -= 3  # Duck = -3 points

    # Strike rate bonus points (if player faced at least 20 balls)
    if balls_faced >= 20:
        runs_per_100_balls = (runs / balls_faced) * 100
        if runs_per_100_balls > 140:
            batsman_points += 6  # Above 140 runs per 100 balls
        elif 120.01 <= runs_per_100_balls <= 140:
            batsman_points += 4  # Between 120.01 and 140 runs per 100 balls
        elif 100 <= runs_per_100_balls < 120:
            batsman_points += 2  # Between 100 and 120 runs per 100 balls
        elif 40 <= runs_per_100_balls < 50:
            batsman_points -= 2  # Between 40 and 50 runs per 100 balls
        elif 30 <= runs_per_100_balls < 40:
            batsman_points -= 4  # Between 30 and 39.99 runs per 100 balls
        elif runs_per_100_balls < 30:
            batsman_points -= 6  # Below 30 runs per 100 balls

    return batsman_points

def calculate_batsman_points_test(runs, boundaries, sixes, strike_rate):
    batsman_points = 0

    # Run points
    batsman_points += runs

    # Boundary points
    batsman_points += boundaries * 1  # 1 point per boundary

    # Six points
    batsman_points += sixes * 2  # 2 points per six

    # Half-century & Century points
    if runs >= 100:
        batsman_points += 8  # 100 runs = 8 points
    elif runs >= 50:
        batsman_points += 4  # 50 runs = 4 points

    # Duck points
    if runs == 0:
        batsman_points -= 4  # Duck = -4 points

    return batsman_points

def calculate_batsman_points_t10(runs, boundaries, sixes, strike_rate):
    batsman_points = 0

    balls_faced = (runs * 100) / strike_rate  # Calculate balls faced if not provided

    # Run points
    batsman_points += runs

    # Boundary points
    batsman_points += boundaries * 1  # 1 point per boundary

    # Six points
    batsman_points += sixes * 2  # 2 points per six

    # 30 and 50 Run Bonus points
    if runs >= 50:
        batsman_points += 16  # 50 runs = 16 points
    elif runs >= 30:
        batsman_points += 8  # 30 runs = 8 points

    # Duck points
    if runs == 0:
        batsman_points -= 2  # Duck = -2 points

    # Strike rate bonus points (if player faced at least 5 balls)
    if balls_faced >= 5:
        runs_per_100_balls = (runs / balls_faced) * 100
        if runs_per_100_balls > 190:
            batsman_points += 6  # Over 190 runs per 100 balls
        elif 170.01 <= runs_per_100_balls <= 190:
            batsman_points += 4  # Between 170.01 and 190 runs per 100 balls
        elif 150 <= runs_per_100_balls < 170:
            batsman_points += 2  # Between 150 and 170 runs per 100 balls
        elif 70 <= runs_per_100_balls < 80:
            batsman_points -= 2  # Between 70 and 80 runs per 100 balls
        elif 60 <= runs_per_100_balls < 70:
            batsman_points -= 4  # Between 60 and 69.99 runs per 100 balls
        elif runs_per_100_balls < 60:
            batsman_points -= 6  # Below 60 runs per 100 balls

    return batsman_points

def calculate_bowler_points_t20(wickets, bowled_lbw, maidens, economy):
    bowler_points = 0

    # Wicket points
    bowler_points += wickets * 25  # 25 points per wicket

    # Bowled/LBW bonus points (8 points per wicket for Bowled or LBW)
    bowler_points += bowled_lbw * 8  # Each Bowled/LBW wicket adds 8 points

    # Wicket bonus points
    if wickets >= 5:
        bowler_points += 16  # 5 wickets = 16 points
    elif wickets == 4:
        bowler_points += 8   # 4 wickets = 8 points
    elif wickets == 3:
        bowler_points += 4   # 3 wickets = 4 points

    # Maiden Over points
    bowler_points += maidens * 12  # 12 points per maiden over

    # Economy points
    if economy < 5:
        bowler_points += 6  # Below 5 runs per over
    elif 5 <= economy < 6:
        bowler_points += 4  # Between 5 and 5.99 runs per over
    elif 6 <= economy < 7:
        bowler_points += 2  # Between 6 and 7 runs per over
    elif 10 <= economy < 11:
        bowler_points -= 2  # Between 10 and 11 runs per over
    elif 11.01 <= economy <= 12:
        bowler_points -= 4  # Between 11.01 and 12 runs per over
    elif economy > 12:
        bowler_points -= 6  # Above 12 runs per over

    return bowler_points

def calculate_bowler_points_odi(wickets, bowled_lbw, maidens, economy):
    bowler_points = 0

    # Wicket points (excluding run outs)
    bowler_points += wickets * 25  # 25 points per wicket

    # Bowled/LBW bonus points (8 points per wicket for Bowled or LBW)
    bowler_points += bowled_lbw * 8  # Each Bowled/LBW wicket adds 8 points

    # Wicket bonus points
    if wickets == 5:
        bowler_points += 8  # 5 wickets = 8 points
    elif wickets == 4:
        bowler_points += 4  # 4 wickets = 4 points

    # Maiden Over points
    bowler_points += maidens * 4  # 4 points per maiden over

    # Economy points
    if economy < 2.5:
        bowler_points += 6  # Below 2.5 runs per over
    elif 2.5 <= economy < 3.5:
        bowler_points += 4  # Between 2.5 and 3.49 runs per over
    elif 3.5 <= economy < 4.5:
        bowler_points += 2  # Between 3.5 and 4.5 runs per over
    elif 7 <= economy < 8:
        bowler_points -= 2  # Between 7 and 8 runs per over
    elif 8.01 <= economy <= 9:
        bowler_points -= 4  # Between 8.01 and 9 runs per over
    elif economy > 9:
        bowler_points -= 6  # Above 9 runs per over

    return bowler_points

def calculate_bowler_points_test(wickets, bowled_lbw, maidens, economy):
    bowler_points = 0

    # Wicket points (excluding run outs)
    bowler_points += wickets * 16  # 16 points per wicket

    # Bowled/LBW bonus points (8 points per wicket for Bowled or LBW)
    bowler_points += bowled_lbw * 8  # Each Bowled/LBW wicket adds 8 points

    # Wicket bonus points
    if wickets == 5:
        bowler_points += 8  # 5 wickets = 8 points
    elif wickets == 4:
        bowler_points += 4  # 4 wickets = 4 points

    return bowler_points

def calculate_bowler_points_t10(wickets, bowled_lbw, maidens, economy):
    bowler_points = 0

    # Wicket points (excluding run outs)
    bowler_points += wickets * 25  # 25 points per wicket

    # Bowled/LBW bonus points (8 points per wicket for Bowled or LBW)
    bowler_points += bowled_lbw * 8  # Each Bowled/LBW wicket adds 8 points

    # Wicket bonus points
    if wickets == 3:
        bowler_points += 16  # 3 wickets = 16 points
    elif wickets == 2:
        bowler_points += 8  # 2 wickets = 8 points

    # Maiden Over points
    bowler_points += maidens * 16  # 16 points per maiden over

    # Economy points
    if economy < 7:
        bowler_points += 6  # Below 7 runs per over
    elif 7 <= economy < 8:
        bowler_points += 4  # Between 7 and 7.99 runs per over
    elif 8 <= economy < 9:
        bowler_points += 2  # Between 8 and 9 runs per over
    elif 14 <= economy < 15:
        bowler_points -= 2  # Between 14 and 15 runs per over
    elif 15.01 <= economy <= 16:
        bowler_points -= 4  # Between 15.01 and 16 runs per over
    elif economy > 16:
        bowler_points -= 6  # Above 16 runs per over

    return bowler_points

def calculate_fielder_points_t20(catches, stumpings, runouts_direct, runouts_indirect):
    fielder_points = 0

    # Catches: +8 points for each catch
    fielder_points += catches * 8

    # 3 Catch Bonus: +4 points if 3 or more catches are taken
    if catches >= 3:
        fielder_points += 4

    # Stumpings: +12 points for each stumping
    fielder_points += stumpings * 12

    # Runouts (Direct Hit): +12 points for each direct runout
    fielder_points += runouts_direct * 12

    # Runouts (Not a Direct Hit): +6 points for each indirect runout
    fielder_points += runouts_indirect * 6

    return fielder_points

def calculate_fielder_points_odi(catches, stumpings, runouts_direct, runouts_indirect):
    fielder_points = 0

    # Catches: +8 points for each catch
    fielder_points += catches * 8

    # 3 Catch Bonus: +4 points if 3 or more catches are taken
    if catches >= 3:
        fielder_points += 4

    # Stumpings: +12 points for each stumping
    fielder_points += stumpings * 12

    # Runouts (Direct Hit): +12 points for each direct runout
    fielder_points += runouts_direct * 12

    # Runouts (Not a Direct Hit): +6 points for each indirect runout
    fielder_points += runouts_indirect * 6

    return fielder_points

def calculate_fielder_points_test(catches, stumpings, runouts_direct, runouts_indirect):
    fielder_points = 0

    # Catches: +8 points for each catch
    fielder_points += catches * 8

    # Stumpings: +12 points for each stumping
    fielder_points += stumpings * 12

    # Runouts (Direct Hit): +12 points for each direct runout
    fielder_points += runouts_direct * 12

    # Runouts (Not Direct Hit): +6 points for each indirect runout
    fielder_points += runouts_indirect * 6

    return fielder_points

def calculate_fielder_points_t10(catches, stumpings, runouts_direct, runouts_indirect):
    fielder_points = 0

    # Catches: +8 points for each catch
    fielder_points += catches * 8

    # 3 Catch Bonus: +4 points if 3 or more catches are taken
    if catches >= 3:
        fielder_points += 4

    # Stumpings: +12 points for each stumping
    fielder_points += stumpings * 12

    # Runouts (Direct Hit): +12 points for each direct runout
    fielder_points += runouts_direct * 12

    # Runouts (Not Direct Hit): +6 points for each indirect runout
    fielder_points += runouts_indirect * 6

    return fielder_points




def points_calculator(format, runs, boundaries, sixes, strike_rate, wickets, bowled_lbw, maidens, economy, catches, stumpings, runouts_direct, runouts_indirect):
    if format == "T20":
        total_points = (calculate_batsman_points_t20(runs, boundaries, sixes, strike_rate) +
                        calculate_bowler_points_t20(wickets, bowled_lbw, maidens, economy) +
                        calculate_fielder_points_t20(catches, stumpings, runouts_direct, runouts_indirect))

    elif format == "ODI":
        total_points = (calculate_batsman_points_odi(runs, boundaries, sixes, strike_rate) +
                        calculate_bowler_points_odi(wickets, bowled_lbw, maidens, economy) +
                        calculate_fielder_points_odi(catches, stumpings, runouts_direct, runouts_indirect))

    elif format == "TEST":
        total_points = (calculate_batsman_points_test(runs, boundaries, sixes, strike_rate) +
                        calculate_bowler_points_test(wickets, bowled_lbw, maidens, economy) +
                        calculate_fielder_points_test(catches, stumpings, runouts_direct, runouts_indirect))

    elif format == "T10":
        total_points = (calculate_batsman_points_t10(runs, boundaries, sixes, strike_rate) +
                        calculate_bowler_points_t10(wickets, bowled_lbw, maidens, economy) +
                        calculate_fielder_points_t10(catches, stumpings, runouts_direct, runouts_indirect))


    else:
        raise ValueError("Unsupported format")

    return total_points
