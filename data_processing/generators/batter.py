import pandas as pd
import yaml

import os
import time
import numpy as np
import warnings
import math

warnings.filterwarnings("ignore")  # Hide messy Numpy warnings

pace_list = [
    "Right-arm fast-medium",
    "Left-arm fast-medium",
    "Right-arm medium-fast",
    "Right-arm medium",
    "Right-arm fast",
    "Left-arm fast",
    "Right-arm slow",
    "Right-arm bowler",
    "Left-arm bowler",
    "Right-arm slow (roundarm)",
    "Right-arm fast (roundarm)",
    "Left-arm fast (roundarm)",
]

location = os.path.join("data", "raw", "additional_data", "combined.csv")
details = pd.read_csv(location)


def extract_details(filename):
    dict = yaml.load(open(filename), yaml.Loader)

    flag = False

    match_details = {}
    try:
        match_details["venue_name"] = dict["info"]["venue"]
    except:
        match_details["venue_name"] = ""
    try:
        match_details["format"] = dict["info"]["match_type"]
    except:
        match_details["format"] = ""
    try:
        match_details["city"] = dict["info"]["city"]
    except:
        match_details["city"] = ""
    try:
        match_details["date"] = dict["info"]["dates"][0]
    except:
        match_details["date"] = ""
    try:
        match_details["team1"] = dict["info"]["teams"][0]
    except:
        match_details["team1"] = ""
    try:
        match_details["team2"] = dict["info"]["teams"][1]
    except:
        match_details["team2"] = ""
    try:
        match_details["player_of_the_match"] = dict["info"]["player_of_match"][0]
    except:
        match_details["player_of_the_match"] = ""

    toss = 0

    if "winner" not in dict["info"]["outcome"]:
        match_details["winner"] = "no_result"
    else:
        match_details["winner"] = dict["info"]["outcome"]["winner"]
    if dict["info"]["toss"]["winner"] == match_details["team1"]:
        if dict["info"]["toss"]["decision"] == "bat":
            match_details["bat_first"] = [
                match_details["team1"],
                match_details["team2"],
            ]
            toss = 1
        else:
            match_details["bat_first"] = [
                match_details["team2"],
                match_details["team1"],
            ]
    else:
        if dict["info"]["toss"]["decision"] == "bat":
            match_details["bat_first"] = [
                match_details["team2"],
                match_details["team1"],
            ]
            toss = 1
        else:
            match_details["bat_first"] = [
                match_details["team1"],
                match_details["team2"],
            ]

    player_details = pd.DataFrame(
        columns=[
            "date",
            "team",
            "runs",
            "dots",
            "4s",
            "6s",
            "balls_involved",
            "balls",
            "not_out",
            "opposition_name",
            "bat_first",
            "toss_outcome",
            "batting_innings",
            "venue_name",
            "outcome",
        ]
    )
    madien = 0
    innings1 = dict["innings"][0]["1st innings"]["deliveries"]
    for ball in innings1:
        for delivery in ball:

            try:
                player_details.index.get_loc(ball[delivery]["batsman"])
            except:
                player_details.loc[ball[delivery]["batsman"], "bat_first"] = 1
                player_details.loc[ball[delivery]["batsman"], "toss_outcome"] = toss
                player_details.loc[ball[delivery]["batsman"], "runs"] = 0
                player_details.loc[ball[delivery]["batsman"], "balls"] = 0
                player_details.loc[ball[delivery]["batsman"], "balls_involved"] = 0
                player_details.loc[ball[delivery]["batsman"], "dots"] = 0
                player_details.loc[ball[delivery]["batsman"], "4s"] = 0
                player_details.loc[ball[delivery]["batsman"], "6s"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_runs_b1"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_runs_b2"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_runs_b3"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_runs_b1"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_runs_b2"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_runs_b3"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_balls_b1"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_balls_b2"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_balls_b3"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_balls_b1"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_balls_b2"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_balls_b3"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_wickets_b1"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_wickets_b2"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_wickets_b3"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_wickets_b1"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_wickets_b2"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_wickets_b3"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_6s_b1"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_6s_b2"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_6s_b3"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_6s_b1"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_6s_b2"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_6s_b3"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_4s_b1"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_4s_b2"] = 0
                player_details.loc[ball[delivery]["batsman"], "spin_4s_b3"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_4s_b1"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_4s_b2"] = 0
                player_details.loc[ball[delivery]["batsman"], "pace_4s_b3"] = 0
                player_details.loc[ball[delivery]["batsman"], "bowled_b1"] = 0
                player_details.loc[ball[delivery]["batsman"], "bowled_b2"] = 0
                player_details.loc[ball[delivery]["batsman"], "bowled_b3"] = 0
                player_details.loc[ball[delivery]["batsman"], "madien_b1"] = 0
                player_details.loc[ball[delivery]["batsman"], "madien_b2"] = 0
                player_details.loc[ball[delivery]["batsman"], "madien_b3"] = 0
                player_details.loc[ball[delivery]["batsman"], "lbw"] = 0
                player_details.loc[ball[delivery]["batsman"], "caught"] = 0
                player_details.loc[ball[delivery]["batsman"], "bowled"] = 0
                player_details.loc[ball[delivery]["batsman"], "stumped"] = 0
                player_details.loc[ball[delivery]["batsman"], "run out"] = 0
                player_details.loc[ball[delivery]["batsman"], "caught and bowled"] = 0
                player_details.loc[ball[delivery]["batsman"], "hit wicket"] = 0

            player_details.loc[ball[delivery]["batsman"], "date"] = match_details[
                "date"
            ]
            player_details.loc[ball[delivery]["batsman"], "team"] = match_details[
                "bat_first"
            ][0]
            player_details.loc[
                ball[delivery]["batsman"], "opposition_name"
            ] = match_details["bat_first"][1]
            player_details.loc[ball[delivery]["batsman"], "batting_innings"] = 1
            player_details.loc[ball[delivery]["batsman"], "venue_name"] = match_details[
                "venue_name"
            ]

            if (
                match_details["winner"]
                == player_details.loc[ball[delivery]["batsman"], "team"]
            ):
                player_details.loc[ball[delivery]["batsman"], "outcome"] = 1
            else:
                player_details.loc[ball[delivery]["batsman"], "outcome"] = 0
            if "wicket" in ball[delivery]:
                player_details.loc[ball[delivery]["batsman"], "not_out"] = 0

                try:
                    player_details.loc[
                        ball[delivery]["batsman"], ball[delivery]["wicket"]["kind"]
                    ] += 1
                except:
                    welp = 0
            else:
                player_details.loc[ball[delivery]["batsman"], "not_out"] = 1

            player_details.loc[ball[delivery]["batsman"], "runs"] += ball[delivery][
                "runs"
            ]["batsman"]

            player_details.loc[ball[delivery]["batsman"], "4s"] += (
                ball[delivery]["runs"]["batsman"] == 4
            )
            player_details.loc[ball[delivery]["batsman"], "6s"] += (
                ball[delivery]["runs"]["batsman"] == 6
            )
            player_details.loc[ball[delivery]["batsman"], "dots"] += (
                ball[delivery]["runs"]["batsman"] == 0
            )
            player_details.loc[ball[delivery]["batsman"], "balls"] += 1

            try:
                if (
                    details[details["unique_name"] == ball[delivery]["bowler"]][
                        "bowling_style"
                    ].values[0]
                    in pace_list
                ):
                    # print('pace')

                    if math.modf(delivery)[1] < 10:
                        player_details.loc[
                            ball[delivery]["batsman"], "pace_balls_b1"
                        ] += 1
                        player_details.loc[
                            ball[delivery]["batsman"], "pace_runs_b1"
                        ] += ball[delivery]["runs"]["batsman"]
                        player_details.loc[ball[delivery]["batsman"], "pace_4s_b1"] += (
                            ball[delivery]["runs"]["batsman"] == 4
                        )
                        player_details.loc[ball[delivery]["batsman"], "pace_6s_b1"] += (
                            ball[delivery]["runs"]["batsman"] == 6
                        )
                        if math.modf(delivery)[0] == 1 and madien == 0:
                            player_details.loc[
                                ball[delivery]["batsman"], "madien_b1"
                            ] += 1
                        if (
                            player_details.loc[ball[delivery]["batsman"], "not_out"]
                            == 0
                        ):
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_wickets_b1"
                            ] += 1
                            if (
                                ball[delivery]["wicket"]["kind"] == "bowled"
                                or ball[delivery]["wicket"]["kind"] == "lbw"
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "bowled_b1"
                                ] += 1
                    elif math.modf(delivery)[1] < 40:
                        player_details.loc[
                            ball[delivery]["batsman"], "pace_balls_b2"
                        ] += 1
                        player_details.loc[
                            ball[delivery]["batsman"], "pace_runs_b2"
                        ] += ball[delivery]["runs"]["batsman"]
                        player_details.loc[ball[delivery]["batsman"], "pace_4s_b2"] += (
                            ball[delivery]["runs"]["batsman"] == 4
                        )
                        player_details.loc[ball[delivery]["batsman"], "pace_6s_b2"] += (
                            ball[delivery]["runs"]["batsman"] == 6
                        )
                        if math.modf(delivery)[0] == 1 and madien == 0:
                            player_details.loc[
                                ball[delivery]["batsman"], "madien_b2"
                            ] += 1
                        if (
                            player_details.loc[ball[delivery]["batsman"], "not_out"]
                            == 0
                        ):
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_wickets_b2"
                            ] += 1
                            if (
                                ball[delivery]["wicket"]["kind"] == "bowled"
                                or ball[delivery]["wicket"]["kind"] == "lbw"
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "bowled_b2"
                                ] += 1
                    else:
                        player_details.loc[
                            ball[delivery]["batsman"], "pace_balls_b3"
                        ] += 1
                        player_details.loc[
                            ball[delivery]["batsman"], "pace_runs_b3"
                        ] += ball[delivery]["runs"]["batsman"]
                        player_details.loc[ball[delivery]["batsman"], "pace_4s_b3"] += (
                            ball[delivery]["runs"]["batsman"] == 4
                        )
                        player_details.loc[ball[delivery]["batsman"], "pace_6s_b3"] += (
                            ball[delivery]["runs"]["batsman"] == 6
                        )
                        if math.modf(delivery)[0] == 1 and madien == 0:
                            player_details.loc[
                                ball[delivery]["batsman"], "madien_b3"
                            ] += 1
                        if (
                            player_details.loc[ball[delivery]["batsman"], "not_out"]
                            == 0
                        ):
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_wickets_b3"
                            ] += 1
                            if (
                                ball[delivery]["wicket"]["kind"] == "bowled"
                                or ball[delivery]["wicket"]["kind"] == "lbw"
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "bowled_b3"
                                ] += 1
                else:
                    # print('spin')
                    if math.modf(delivery)[1] < 10:
                        player_details.loc[
                            ball[delivery]["batsman"], "spin_balls_b1"
                        ] += 1
                        player_details.loc[
                            ball[delivery]["batsman"], "spin_runs_b1"
                        ] += ball[delivery]["runs"]["batsman"]
                        player_details.loc[ball[delivery]["batsman"], "spin_4s_b1"] += (
                            ball[delivery]["runs"]["batsman"] == 4
                        )
                        player_details.loc[ball[delivery]["batsman"], "spin_6s_b1"] += (
                            ball[delivery]["runs"]["batsman"] == 6
                        )
                        if math.modf(delivery)[0] == 1 and madien == 0:
                            player_details.loc[
                                ball[delivery]["batsman"], "madien_b1"
                            ] += 1
                        if (
                            player_details.loc[ball[delivery]["batsman"], "not_out"]
                            == 0
                        ):
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_wickets_b1"
                            ] += 1
                            if (
                                ball[delivery]["wicket"]["kind"] == "bowled"
                                or ball[delivery]["wicket"]["kind"] == "lbw"
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "bowled_b1"
                                ] += 1
                    elif math.modf(delivery)[1] < 40:
                        player_details.loc[
                            ball[delivery]["batsman"], "spin_balls_b2"
                        ] += 1
                        player_details.loc[
                            ball[delivery]["batsman"], "spin_runs_b2"
                        ] += ball[delivery]["runs"]["batsman"]
                        player_details.loc[ball[delivery]["batsman"], "spin_4s_b2"] += (
                            ball[delivery]["runs"]["batsman"] == 4
                        )
                        player_details.loc[ball[delivery]["batsman"], "spin_6s_b2"] += (
                            ball[delivery]["runs"]["batsman"] == 6
                        )
                        if math.modf(delivery)[0] == 1 and madien == 0:
                            player_details.loc[
                                ball[delivery]["batsman"], "madien_b2"
                            ] += 1
                        if (
                            player_details.loc[ball[delivery]["batsman"], "not_out"]
                            == 0
                        ):
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_wickets_b2"
                            ] += 1
                            if (
                                ball[delivery]["wicket"]["kind"] == "bowled"
                                or ball[delivery]["wicket"]["kind"] == "lbw"
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "bowled_b2"
                                ] += 1
                    else:

                        player_details.loc[
                            ball[delivery]["batsman"], "spin_balls_b3"
                        ] += 1
                        player_details.loc[
                            ball[delivery]["batsman"], "spin_runs_b3"
                        ] += ball[delivery]["runs"]["batsman"]
                        player_details.loc[ball[delivery]["batsman"], "spin_4s_b3"] += (
                            ball[delivery]["runs"]["batsman"] == 4
                        )
                        player_details.loc[ball[delivery]["batsman"], "spin_6s_b3"] += (
                            ball[delivery]["runs"]["batsman"] == 6
                        )
                        if math.modf(delivery)[0] == 1 and madien == 0:
                            player_details.loc[
                                ball[delivery]["batsman"], "madien_b3"
                            ] += 1
                        if (
                            player_details.loc[ball[delivery]["batsman"], "not_out"]
                            == 0
                        ):
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_wickets_b3"
                            ] += 1
                            if (
                                ball[delivery]["wicket"]["kind"] == "bowled"
                                or ball[delivery]["wicket"]["kind"] == "lbw"
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "bowled_b3"
                                ] += 1
            except:
                w = 0
            player_details.loc[ball[delivery]["batsman"], "balls_involved"] += (
                ball[delivery]["runs"]["batsman"] != 0
            )
            if math.modf(delivery)[0] == 1:
                madien = 0
            madien += ball[delivery]["runs"]["batsman"]

    try:
        innings2 = dict["innings"][1]["2nd innings"]["deliveries"]
    except:
        flag = True
    else:
        for ball in innings2:
            for delivery in ball:

                try:
                    player_details.index.get_loc(ball[delivery]["batsman"])
                except:

                    player_details.loc[ball[delivery]["batsman"], "bat_first"] = 0
                    player_details.loc[ball[delivery]["batsman"], "toss_outcome"] = (
                        1 - toss
                    )
                    player_details.loc[ball[delivery]["batsman"], "runs"] = 0
                    player_details.loc[ball[delivery]["batsman"], "balls"] = 0
                    player_details.loc[ball[delivery]["batsman"], "balls_involved"] = 0
                    player_details.loc[ball[delivery]["batsman"], "dots"] = 0
                    player_details.loc[ball[delivery]["batsman"], "4s"] = 0
                    player_details.loc[ball[delivery]["batsman"], "6s"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_runs_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_runs_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_runs_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_runs_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_runs_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_runs_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_balls_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_balls_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_balls_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_balls_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_balls_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_balls_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_wickets_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_wickets_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_wickets_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_wickets_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_wickets_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_wickets_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_6s_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_6s_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_6s_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_6s_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_6s_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_6s_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_4s_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_4s_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_4s_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_4s_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_4s_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_4s_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "bowled_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "bowled_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "bowled_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "madien_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "madien_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "madien_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "lbw"] = 0
                    player_details.loc[ball[delivery]["batsman"], "caught"] = 0
                    player_details.loc[ball[delivery]["batsman"], "bowled"] = 0
                    player_details.loc[ball[delivery]["batsman"], "stumped"] = 0
                    player_details.loc[ball[delivery]["batsman"], "run out"] = 0
                    player_details.loc[
                        ball[delivery]["batsman"], "caught and bowled"
                    ] = 0
                    player_details.loc[ball[delivery]["batsman"], "hit wicket"] = 0
                player_details.loc[ball[delivery]["batsman"], "date"] = match_details[
                    "date"
                ]
                player_details.loc[ball[delivery]["batsman"], "team"] = match_details[
                    "bat_first"
                ][1]
                player_details.loc[
                    ball[delivery]["batsman"], "opposition_name"
                ] = match_details["bat_first"][0]
                player_details.loc[ball[delivery]["batsman"], "batting_innings"] = 2
                player_details.loc[
                    ball[delivery]["batsman"], "venue_name"
                ] = match_details["venue_name"]
                if (
                    match_details["winner"]
                    == player_details.loc[ball[delivery]["batsman"], "team"]
                ):
                    player_details.loc[ball[delivery]["batsman"], "outcome"] = 1
                else:
                    player_details.loc[ball[delivery]["batsman"], "outcome"] = 0
                if "wicket" in ball[delivery]:
                    player_details.loc[ball[delivery]["batsman"], "not_out"] = 0
                    try:
                        player_details.loc[
                            ball[delivery]["batsman"], ball[delivery]["wicket"]["kind"]
                        ] += 1
                    except:
                        welp = 0

                else:
                    player_details.loc[ball[delivery]["batsman"], "not_out"] = 1

                player_details.loc[ball[delivery]["batsman"], "runs"] += ball[delivery][
                    "runs"
                ]["batsman"]
                player_details.loc[ball[delivery]["batsman"], "4s"] += (
                    ball[delivery]["runs"]["batsman"] == 4
                )
                player_details.loc[ball[delivery]["batsman"], "6s"] += (
                    ball[delivery]["runs"]["batsman"] == 6
                )
                player_details.loc[ball[delivery]["batsman"], "dots"] += (
                    ball[delivery]["runs"]["batsman"] == 0
                )
                player_details.loc[ball[delivery]["batsman"], "balls"] += 1
                player_details.loc[ball[delivery]["batsman"], "balls_involved"] += (
                    ball[delivery]["runs"]["batsman"] != 0
                )
                try:
                    if (
                        details[details["unique_name"] == ball[delivery]["bowler"]][
                            "bowling_style"
                        ].values[0]
                        in pace_list
                    ):

                        # print('pace')
                        if math.modf(delivery)[1] < 10:
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_balls_b1"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_runs_b1"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_4s_b1"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_6s_b1"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b1"
                                ] += 1
                                if (
                                    player_details.loc[
                                        ball[delivery]["batsman"], "not_out"
                                    ]
                                    == 0
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "pace_wickets_b1"
                                    ] += 1
                                    if (
                                        ball[delivery]["wicket"]["kind"] == "bowled"
                                        or ball[delivery]["wicket"]["kind"] == "lbw"
                                    ):
                                        player_details.loc[
                                            ball[delivery]["batsman"], "bowled_b1"
                                        ] += 1
                        elif math.modf(delivery)[1] < 40:
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_balls_b2"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_runs_b2"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_4s_b2"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_6s_b2"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b2"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "pace_wickets_b2"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b2"
                                    ] += 1
                        else:
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_balls_b3"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_runs_b3"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_4s_b3"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_6s_b3"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b3"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "pace_wickets_b3"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b3"
                                    ] += 1
                    else:
                        if math.modf(delivery)[1] < 10:
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_balls_b1"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_runs_b1"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_4s_b1"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_6s_b1"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b1"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "spin_wickets_b1"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b1"
                                    ] += 1
                        elif math.modf(delivery)[1] < 40:
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_balls_b2"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_runs_b2"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_4s_b2"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_6s_b2"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b2"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "spin_wickets_b2"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b2"
                                    ] += 1
                        else:
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_balls_b3"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_runs_b3"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_4s_b3"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_6s_b3"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b3"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "spin_wickets_b3"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b3"
                                    ] += 1
                except:

                    # print('fail')
                    w = 0
                player_details.loc[ball[delivery]["batsman"], "balls_involved"] += (
                    ball[delivery]["runs"]["batsman"] != 0
                )
                if math.modf(delivery)[0] == 1:
                    madien = 0
                madien += ball[delivery]["runs"]["batsman"]

    try:
        innings3 = dict["innings"][2]["3rd innings"]["deliveries"]
    except:
        flag = True
    else:
        for ball in innings3:
            for delivery in ball:

                try:
                    player_details.index.get_loc(ball[delivery]["batsman"])
                except:
                    player_details.loc[ball[delivery]["batsman"], "bat_first"] = 1
                    player_details.loc[ball[delivery]["batsman"], "toss_outcome"] = toss
                    player_details.loc[ball[delivery]["batsman"], "runs"] = 0
                    player_details.loc[ball[delivery]["batsman"], "balls"] = 0
                    player_details.loc[ball[delivery]["batsman"], "balls_involved"] = 0
                    player_details.loc[ball[delivery]["batsman"], "dots"] = 0
                    player_details.loc[ball[delivery]["batsman"], "4s"] = 0
                    player_details.loc[ball[delivery]["batsman"], "6s"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_runs_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_runs_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_runs_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_runs_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_runs_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_runs_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_balls_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_balls_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_balls_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_balls_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_balls_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_balls_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_wickets_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_wickets_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_wickets_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_wickets_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_wickets_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_wickets_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_6s_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_6s_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_6s_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_6s_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_6s_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_6s_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_4s_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_4s_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_4s_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_4s_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_4s_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_4s_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "bowled_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "bowled_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "bowled_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "madien_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "madien_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "madien_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "lbw"] = 0
                    player_details.loc[ball[delivery]["batsman"], "caught"] = 0
                    player_details.loc[ball[delivery]["batsman"], "bowled"] = 0
                    player_details.loc[ball[delivery]["batsman"], "stumped"] = 0
                    player_details.loc[ball[delivery]["batsman"], "run out"] = 0
                    player_details.loc[
                        ball[delivery]["batsman"], "caught and bowled"
                    ] = 0
                    player_details.loc[ball[delivery]["batsman"], "hit wicket"] = 0

                player_details.loc[ball[delivery]["batsman"], "date"] = match_details[
                    "date"
                ]
                player_details.loc[ball[delivery]["batsman"], "team"] = match_details[
                    "bat_first"
                ][0]
                player_details.loc[
                    ball[delivery]["batsman"], "opposition_name"
                ] = match_details["bat_first"][1]
                player_details.loc[ball[delivery]["batsman"], "batting_innings"] = 1
                player_details.loc[
                    ball[delivery]["batsman"], "venue_name"
                ] = match_details["venue_name"]

                if (
                    match_details["winner"]
                    == player_details.loc[ball[delivery]["batsman"], "team"]
                ):
                    player_details.loc[ball[delivery]["batsman"], "outcome"] = 1
                else:
                    player_details.loc[ball[delivery]["batsman"], "outcome"] = 0
                if "wicket" in ball[delivery]:
                    player_details.loc[ball[delivery]["batsman"], "not_out"] = 0

                    try:
                        player_details.loc[
                            ball[delivery]["batsman"], ball[delivery]["wicket"]["kind"]
                        ] += 1
                    except:
                        welp = 0
                else:
                    player_details.loc[ball[delivery]["batsman"], "not_out"] = 1

                player_details.loc[ball[delivery]["batsman"], "runs"] += ball[delivery][
                    "runs"
                ]["batsman"]

                player_details.loc[ball[delivery]["batsman"], "4s"] += (
                    ball[delivery]["runs"]["batsman"] == 4
                )
                player_details.loc[ball[delivery]["batsman"], "6s"] += (
                    ball[delivery]["runs"]["batsman"] == 6
                )
                player_details.loc[ball[delivery]["batsman"], "dots"] += (
                    ball[delivery]["runs"]["batsman"] == 0
                )
                player_details.loc[ball[delivery]["batsman"], "balls"] += 1

                try:
                    if (
                        details[details["unique_name"] == ball[delivery]["bowler"]][
                            "bowling_style"
                        ].values[0]
                        in pace_list
                    ):

                        if math.modf(delivery)[1] < 10:
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_balls_b1"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_runs_b1"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_4s_b1"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_6s_b1"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b1"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "pace_wickets_b1"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b1"
                                    ] += 1
                        elif math.modf(delivery)[1] < 40:
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_balls_b2"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_runs_b2"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_4s_b2"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_6s_b2"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b2"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "pace_wickets_b2"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b2"
                                    ] += 1
                        else:
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_balls_b3"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_runs_b3"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_4s_b3"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_6s_b3"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b3"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "pace_wickets_b3"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b3"
                                    ] += 1
                    else:
                        if math.modf(delivery)[1] < 10:
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_balls_b1"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_runs_b1"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_4s_b1"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_6s_b1"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b1"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "spin_wickets_b1"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b1"
                                    ] += 1
                        elif math.modf(delivery)[1] < 40:
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_balls_b2"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_runs_b2"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_4s_b2"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_6s_b2"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b2"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "spin_wickets_b2"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b2"
                                    ] += 1
                        else:
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_balls_b3"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_runs_b3"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_4s_b3"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_6s_b3"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b3"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "spin_wickets_b3"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b3"
                                    ] += 1
                except:
                    w = 0
                player_details.loc[ball[delivery]["batsman"], "balls_involved"] += (
                    ball[delivery]["runs"]["batsman"] != 0
                )
                if math.modf(delivery)[0] == 1:
                    madien = 0
                madien += ball[delivery]["runs"]["batsman"]

    try:
        innings4 = dict["innings"][3]["4th innings"]["deliveries"]
    except:
        flag = True
    else:
        for ball in innings4:
            for delivery in ball:

                try:
                    player_details.index.get_loc(ball[delivery]["batsman"])
                except:

                    player_details.loc[ball[delivery]["batsman"], "bat_first"] = 0
                    player_details.loc[ball[delivery]["batsman"], "toss_outcome"] = (
                        1 - toss
                    )
                    player_details.loc[ball[delivery]["batsman"], "runs"] = 0
                    player_details.loc[ball[delivery]["batsman"], "balls"] = 0
                    player_details.loc[ball[delivery]["batsman"], "balls_involved"] = 0
                    player_details.loc[ball[delivery]["batsman"], "dots"] = 0
                    player_details.loc[ball[delivery]["batsman"], "4s"] = 0
                    player_details.loc[ball[delivery]["batsman"], "6s"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_runs_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_runs_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_runs_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_runs_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_runs_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_runs_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_balls_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_balls_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_balls_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_balls_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_balls_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_balls_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_wickets_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_wickets_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_wickets_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_wickets_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_wickets_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_wickets_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_6s_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_6s_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_6s_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_6s_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_6s_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_6s_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_4s_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_4s_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "spin_4s_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_4s_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_4s_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "pace_4s_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "bowled_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "bowled_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "bowled_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "madien_b1"] = 0
                    player_details.loc[ball[delivery]["batsman"], "madien_b2"] = 0
                    player_details.loc[ball[delivery]["batsman"], "madien_b3"] = 0
                    player_details.loc[ball[delivery]["batsman"], "lbw"] = 0
                    player_details.loc[ball[delivery]["batsman"], "caught"] = 0
                    player_details.loc[ball[delivery]["batsman"], "bowled"] = 0
                    player_details.loc[ball[delivery]["batsman"], "stumped"] = 0
                    player_details.loc[ball[delivery]["batsman"], "run out"] = 0
                    player_details.loc[
                        ball[delivery]["batsman"], "caught and bowled"
                    ] = 0
                    player_details.loc[ball[delivery]["batsman"], "hit wicket"] = 0
                player_details.loc[ball[delivery]["batsman"], "date"] = match_details[
                    "date"
                ]
                player_details.loc[ball[delivery]["batsman"], "team"] = match_details[
                    "bat_first"
                ][1]
                player_details.loc[
                    ball[delivery]["batsman"], "opposition_name"
                ] = match_details["bat_first"][0]
                player_details.loc[ball[delivery]["batsman"], "batting_innings"] = 2
                player_details.loc[
                    ball[delivery]["batsman"], "venue_name"
                ] = match_details["venue_name"]
                if (
                    match_details["winner"]
                    == player_details.loc[ball[delivery]["batsman"], "team"]
                ):
                    player_details.loc[ball[delivery]["batsman"], "outcome"] = 1
                else:
                    player_details.loc[ball[delivery]["batsman"], "outcome"] = 0
                if "wicket" in ball[delivery]:
                    player_details.loc[ball[delivery]["batsman"], "not_out"] = 0
                    try:
                        player_details.loc[
                            ball[delivery]["batsman"], ball[delivery]["wicket"]["kind"]
                        ] += 1
                    except:
                        welp = 0

                else:
                    player_details.loc[ball[delivery]["batsman"], "not_out"] = 1

                player_details.loc[ball[delivery]["batsman"], "runs"] += ball[delivery][
                    "runs"
                ]["batsman"]
                player_details.loc[ball[delivery]["batsman"], "4s"] += (
                    ball[delivery]["runs"]["batsman"] == 4
                )
                player_details.loc[ball[delivery]["batsman"], "6s"] += (
                    ball[delivery]["runs"]["batsman"] == 6
                )
                player_details.loc[ball[delivery]["batsman"], "dots"] += (
                    ball[delivery]["runs"]["batsman"] == 0
                )
                player_details.loc[ball[delivery]["batsman"], "balls"] += 1
                player_details.loc[ball[delivery]["batsman"], "balls_involved"] += (
                    ball[delivery]["runs"]["batsman"] != 0
                )
                try:
                    if (
                        details[details["unique_name"] == ball[delivery]["bowler"]][
                            "bowling_style"
                        ].values[0]
                        in pace_list
                    ):

                        # print('pace')
                        if math.modf(delivery)[1] < 10:
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_balls_b1"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_runs_b1"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_4s_b1"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_6s_b1"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b1"
                                ] += 1
                                if (
                                    player_details.loc[
                                        ball[delivery]["batsman"], "not_out"
                                    ]
                                    == 0
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "pace_wickets_b1"
                                    ] += 1
                                    if (
                                        ball[delivery]["wicket"]["kind"] == "bowled"
                                        or ball[delivery]["wicket"]["kind"] == "lbw"
                                    ):
                                        player_details.loc[
                                            ball[delivery]["batsman"], "bowled_b1"
                                        ] += 1
                        elif math.modf(delivery)[1] < 40:
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_balls_b2"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_runs_b2"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_4s_b2"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_6s_b2"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b2"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "pace_wickets_b2"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b2"
                                    ] += 1
                        else:
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_balls_b3"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_runs_b3"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_4s_b3"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "pace_6s_b3"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b3"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "pace_wickets_b3"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b3"
                                    ] += 1
                    else:
                        # print('spin')
                        if math.modf(delivery)[1] < 10:
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_balls_b1"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_runs_b1"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_4s_b1"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_6s_b1"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b1"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "spin_wickets_b1"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b1"
                                    ] += 1
                        elif math.modf(delivery)[1] < 40:
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_balls_b2"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_runs_b2"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_4s_b2"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_6s_b2"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b2"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "spin_wickets_b2"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b2"
                                    ] += 1
                        else:
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_balls_b3"
                            ] += 1
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_runs_b3"
                            ] += ball[delivery]["runs"]["batsman"]
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_4s_b3"
                            ] += (ball[delivery]["runs"]["batsman"] == 4)
                            player_details.loc[
                                ball[delivery]["batsman"], "spin_6s_b3"
                            ] += (ball[delivery]["runs"]["batsman"] == 6)
                            if math.modf(delivery)[0] == 1 and madien == 0:
                                player_details.loc[
                                    ball[delivery]["batsman"], "madien_b3"
                                ] += 1
                            if (
                                player_details.loc[ball[delivery]["batsman"], "not_out"]
                                == 0
                            ):
                                player_details.loc[
                                    ball[delivery]["batsman"], "spin_wickets_b3"
                                ] += 1
                                if (
                                    ball[delivery]["wicket"]["kind"] == "bowled"
                                    or ball[delivery]["wicket"]["kind"] == "lbw"
                                ):
                                    player_details.loc[
                                        ball[delivery]["batsman"], "bowled_b3"
                                    ] += 1
                except:

                    # print('fail')
                    w = 0
                player_details.loc[ball[delivery]["batsman"], "balls_involved"] += (
                    ball[delivery]["runs"]["batsman"] != 0
                )
                if math.modf(delivery)[0] == 1:
                    madien = 0
                madien += ball[delivery]["runs"]["batsman"]

    return match_details, player_details


def func(gender, location, formats, matchid_mapping):

    files = pd.read_csv(location)
    grouped = files.groupby("format")

    j = -1
    for format in formats:
        if format[0] == "W":
            form = format[1:]
        else:
            form = format
        date_file_pair = (grouped.get_group(form))["filename"]
        overall_batsman_details = pd.DataFrame(
            columns=[
                "team",
                "innings",
                "runs",
                "balls",
                "balls_involved",
                "outs",
                "average",
                "strike_rate",
                "centuries",
                "fifties",
                "thirties",
                "zeros",
                "4s",
                "6s",
            ]
        )
        match_batsman_details = pd.DataFrame(
            columns=[
                "index",
                "date",
                "match_id",
                "player_name",
                "player_id",
                "team",
                "opposition_name",
                "venue_name",
                "innings_played",
                "previous_balls",
                "previous_balls_involved",
                "previous_outs",
                "previous_average",
                "previous_strike_rate",
                "previous_centuries",
                "previous_fifties",
                "previous_thirties",
                "previous_zeros",
                "previous_runs",
                "previous_4s",
                "previous_6s",
                "runs",
                "dots",
                "4s",
                "6s",
                "balls_involved",
                "balls",
                "not_out",
                "average",
                "strike_rate",
                "highest_score",
                "match_runs",
                "match_4s",
                "match_6s",
                "match_strike_rate",
                "match_fantasy_points",
            ]
        )
        match_batsman_details.set_index("index", inplace=True)

        venue_dict = {}
        opposition_dict = {}

        player_highest_score = {}
        count = -1

        print("To process " + str(len(date_file_pair)) + " files for " + format)
        j += 1
        i = matchid_mapping[j]
        for ele in date_file_pair:
            i += 1
            if i % 10 == 0:
                print(i - matchid_mapping[j])
                # break

            location = os.path.join(
                "data", "raw", "cricsheet_data", "all_" + gender, ele
            )
            match_details, player_details = extract_details(location)
            for player in player_details.index:
                count += 1
                try:
                    overall_batsman_details.index.get_loc(player)
                except:
                    overall_batsman_details.loc[player, "team"] = player_details.loc[
                        player, "team"
                    ]
                    overall_batsman_details.loc[player, "innings"] = [0]
                    overall_batsman_details.loc[player, "runs"] = [0]
                    overall_batsman_details.loc[player, "balls"] = [0]
                    overall_batsman_details.loc[player, "balls_involved"] = [0]
                    overall_batsman_details.loc[player, "outs"] = [0]
                    overall_batsman_details.loc[player, "strike_rate"] = [0]
                    overall_batsman_details.loc[player, "average"] = [0]
                    overall_batsman_details.loc[player, "zeros"] = [0]
                    overall_batsman_details.loc[player, "thirties"] = [0]
                    overall_batsman_details.loc[player, "fifties"] = [0]
                    overall_batsman_details.loc[player, "centuries"] = [0]
                    overall_batsman_details.loc[player, "4s"] = [0]
                    overall_batsman_details.loc[player, "6s"] = [0]

                match_batsman_details.loc[count, "match_id"] = i
                match_batsman_details.loc[count, "date"] = player_details.loc[
                    player, "date"
                ]
                match_batsman_details.loc[count, "player_name"] = player
                match_batsman_details.loc[count, "team"] = player_details.loc[
                    player, "team"
                ]
                match_batsman_details.loc[
                    count, "opposition_name"
                ] = player_details.loc[player, "opposition_name"]
                match_batsman_details.loc[count, "venue_name"] = match_details[
                    "venue_name"
                ]
                match_batsman_details.loc[
                    count, "innings_played"
                ] = overall_batsman_details.loc[player, "innings"][-1]

                match_batsman_details.loc[
                    count, "previous_balls"
                ] = overall_batsman_details.loc[player, "balls"][-1]
                match_batsman_details.loc[
                    count, "previous_balls_involved"
                ] = overall_batsman_details.loc[player, "balls_involved"][-1]
                match_batsman_details.loc[
                    count, "previous_outs"
                ] = overall_batsman_details.loc[player, "outs"][-1]

                match_batsman_details.loc[
                    count, "previous_average"
                ] = overall_batsman_details.loc[player, "average"][-1]
                match_batsman_details.loc[
                    count, "previous_strike_rate"
                ] = overall_batsman_details.loc[player, "strike_rate"][-1]
                match_batsman_details.loc[
                    count, "previous_centuries"
                ] = overall_batsman_details.loc[player, "centuries"][-1]
                match_batsman_details.loc[
                    count, "previous_fifties"
                ] = overall_batsman_details.loc[player, "fifties"][-1]
                match_batsman_details.loc[
                    count, "previous_thirties"
                ] = overall_batsman_details.loc[player, "thirties"][-1]
                match_batsman_details.loc[
                    count, "previous_zeros"
                ] = overall_batsman_details.loc[player, "zeros"][-1]
                match_batsman_details.loc[
                    count, "previous_runs"
                ] = overall_batsman_details.loc[player, "runs"][-1]
                match_batsman_details.loc[
                    count, "previous_4s"
                ] = overall_batsman_details.loc[player, "4s"][-1]
                match_batsman_details.loc[
                    count, "previous_6s"
                ] = overall_batsman_details.loc[player, "6s"][-1]

                match_batsman_details.loc[count, "runs"] = player_details.loc[
                    player, "runs"
                ]
                match_batsman_details.loc[count, "dots"] = player_details.loc[
                    player, "dots"
                ]
                match_batsman_details.loc[count, "4s"] = player_details.loc[
                    player, "4s"
                ]
                match_batsman_details.loc[count, "6s"] = player_details.loc[
                    player, "6s"
                ]
                match_batsman_details.loc[count, "balls"] = player_details.loc[
                    player, "balls"
                ]

                match_batsman_details.loc[count, "balls_involved"] = player_details.loc[
                    player, "balls_involved"
                ]
                match_batsman_details.loc[count, "not_out"] = player_details.loc[
                    player, "not_out"
                ]

                match_batsman_details.loc[count, "strike_rate"] = (
                    match_batsman_details.loc[count, "runs"]
                    * 100.0
                    / match_batsman_details.loc[count, "balls"]
                )
                if (
                    match_batsman_details.loc[count, "previous_outs"]
                    + 1
                    - match_batsman_details.loc[count, "not_out"]
                ) == 0:
                    match_batsman_details.loc[count, "average"] = (
                        match_batsman_details.loc[count, "previous_runs"]
                        + match_batsman_details.loc[count, "runs"]
                    )
                else:
                    match_batsman_details.loc[count, "average"] = (
                        match_batsman_details.loc[count, "previous_runs"]
                        + match_batsman_details.loc[count, "runs"]
                    ) / (
                        match_batsman_details.loc[count, "previous_outs"]
                        + 1
                        - match_batsman_details.loc[count, "not_out"]
                    )

                try:
                    if (
                        match_batsman_details.loc[count, "runs"]
                        >= player_highest_score[
                            match_batsman_details.loc[count, "player_name"]
                        ]
                    ):
                        player_highest_score[
                            match_batsman_details.loc[count, "player_name"]
                        ] = match_batsman_details.loc[count, "runs"]
                except:
                    player_highest_score[
                        match_batsman_details.loc[count, "player_name"]
                    ] = match_batsman_details.loc[count, "runs"]
                match_batsman_details.loc[
                    count, "highest_score"
                ] = player_highest_score[
                    match_batsman_details.loc[count, "player_name"]
                ]

                overall_batsman_details.loc[player, "innings"].append(
                    overall_batsman_details.loc[player, "innings"][-1] + 1
                )
                overall_batsman_details.loc[player, "runs"].append(
                    overall_batsman_details.loc[player, "runs"][-1]
                    + player_details.loc[player, "runs"]
                )
                overall_batsman_details.loc[player, "balls"].append(
                    overall_batsman_details.loc[player, "balls"][-1]
                    + player_details.loc[player, "balls"]
                )
                overall_batsman_details.loc[player, "balls_involved"].append(
                    overall_batsman_details.loc[player, "balls_involved"][-1]
                    + player_details.loc[player, "balls_involved"]
                )
                overall_batsman_details.loc[player, "outs"].append(
                    overall_batsman_details.loc[player, "outs"][-1]
                    + 1
                    - player_details.loc[player, "not_out"]
                )
                # average over the innings
                overall_batsman_details.loc[player, "strike_rate"].append(
                    (
                        (
                            (
                                player_details.loc[player, "runs"]
                                / player_details.loc[player, "balls"]
                            )
                            * 100
                        )
                        + (
                            overall_batsman_details.loc[player, "strike_rate"][-1]
                            * (overall_batsman_details.loc[player, "innings"][-1])
                        )
                    )
                    / (overall_batsman_details.loc[player, "innings"][-1] + 1)
                )
                overall_batsman_details.loc[player, "average"].append(
                    (
                        (player_details.loc[player, "runs"])
                        + (
                            overall_batsman_details.loc[player, "average"][-1]
                            * (overall_batsman_details.loc[player, "innings"][-1])
                        )
                    )
                    / (overall_batsman_details.loc[player, "innings"][-1] + 1)
                )
                overall_batsman_details.loc[player, "4s"].append(
                    overall_batsman_details.loc[player, "4s"][-1]
                    + match_batsman_details.loc[count, "4s"]
                )
                overall_batsman_details.loc[player, "6s"].append(
                    overall_batsman_details.loc[player, "4s"][-1]
                    + match_batsman_details.loc[count, "4s"]
                )

                if player_details.loc[player, "runs"] == 0:
                    overall_batsman_details.loc[player, "zeros"].append(
                        overall_batsman_details.loc[player, "zeros"][-1] + 1
                    )
                else:
                    overall_batsman_details.loc[player, "zeros"].append(
                        overall_batsman_details.loc[player, "zeros"][-1]
                    )
                if (
                    player_details.loc[player, "runs"] >= 30
                    and player_details.loc[player, "runs"] < 50
                ):
                    overall_batsman_details.loc[player, "thirties"].append(
                        overall_batsman_details.loc[player, "thirties"][-1] + 1
                    )
                if (
                    player_details.loc[player, "runs"] >= 50
                    and player_details.loc[player, "runs"] < 100
                ):
                    overall_batsman_details.loc[player, "fifties"].append(
                        overall_batsman_details.loc[player, "fifties"][-1] + 1
                    )
                else:
                    overall_batsman_details.loc[player, "fifties"].append(
                        overall_batsman_details.loc[player, "fifties"][-1]
                    )
                if player_details.loc[player, "runs"] >= 100:
                    overall_batsman_details.loc[player, "centuries"].append(
                        overall_batsman_details.loc[player, "centuries"][-1] + 1
                    )
                else:
                    overall_batsman_details.loc[player, "centuries"].append(
                        overall_batsman_details.loc[player, "centuries"][-1]
                    )

                venue = match_details["venue_name"]
                # putting stuff in venue dict
                if player not in venue_dict:
                    venue_dict[player] = {}
                if venue not in venue_dict[player]:
                    venue_dict[player][venue] = {}
                    venue_dict[player][venue]["innings"] = 0
                    venue_dict[player][venue]["runs"] = 0
                    venue_dict[player][venue]["balls"] = 0
                    venue_dict[player][venue]["wickets"] = 0
                    venue_dict[player][venue]["strike_rate"] = 0
                    venue_dict[player][venue]["average"] = 0
                    venue_dict[player][venue]["centuries"] = 0
                    venue_dict[player][venue]["fifties"] = 0
                    venue_dict[player][venue]["thirties"] = 0
                    venue_dict[player][venue]["zeros"] = 0
                    venue_dict[player][venue]["high_score"] = 0
                venue_dict[player][venue]["innings"] += 1

                if venue_dict[player][venue]["balls"] != 0:
                    venue_dict[player][venue]["strike_rate"] = (
                        venue_dict[player][venue]["runs"]
                        * 100
                        / venue_dict[player][venue]["balls"]
                    )
                else:
                    venue_dict[player][venue]["strike_rate"] = venue_dict[player][
                        venue
                    ]["runs"]
                if venue_dict[player][venue]["wickets"] == 0:
                    venue_dict[player][venue]["average"] = venue_dict[player][venue][
                        "runs"
                    ]
                else:
                    venue_dict[player][venue]["average"] = (
                        venue_dict[player][venue]["runs"]
                        / venue_dict[player][venue]["wickets"]
                    )

                match_batsman_details.loc[count, "venue"] = (
                    0.4262 * venue_dict[player][venue]["average"]
                    + 0.2566 * venue_dict[player][venue]["innings"]
                    + 0.1510 * venue_dict[player][venue]["strike_rate"]
                    + 0.0787 * venue_dict[player][venue]["centuries"]
                    + 0.0556 * venue_dict[player][venue]["fifties"]
                    + 0.0328 * venue_dict[player][venue]["high_score"]
                )

                match_batsman_details.loc[count, "venue_avg"] = venue_dict[player][
                    venue
                ]["average"]

                venue_dict[player][venue]["runs"] += player_details.loc[player, "runs"]
                venue_dict[player][venue]["balls"] += player_details.loc[
                    player, "balls"
                ]
                venue_dict[player][venue]["wickets"] += (
                    1 - player_details.loc[player, "not_out"]
                )
                if player_details.loc[player, "runs"] >= 100:
                    venue_dict[player][venue]["centuries"] += 1
                elif player_details.loc[player, "runs"] >= 50:
                    venue_dict[player][venue]["fifties"] += 1
                elif player_details.loc[player, "runs"] >= 30:
                    venue_dict[player][venue]["thirties"] += 1
                elif player_details.loc[player, "runs"] == 0:
                    venue_dict[player][venue]["zeros"] += 1
                if (
                    player_details.loc[player, "runs"]
                    > venue_dict[player][venue]["high_score"]
                ):
                    venue_dict[player][venue]["high_score"] = player_details.loc[
                        player, "runs"
                    ]

                opposition = player_details.loc[player, "opposition_name"]
                # putting stuff in opposition dict
                if player not in opposition_dict:
                    opposition_dict[player] = {}
                if opposition not in opposition_dict[player]:
                    opposition_dict[player][opposition] = {}
                    opposition_dict[player][opposition]["innings"] = 0
                    opposition_dict[player][opposition]["runs"] = 0
                    opposition_dict[player][opposition]["balls"] = 0
                    opposition_dict[player][opposition]["wickets"] = 0
                    opposition_dict[player][opposition]["strike_rate"] = 0
                    opposition_dict[player][opposition]["average"] = 0
                    opposition_dict[player][opposition]["centuries"] = 0
                    opposition_dict[player][opposition]["fifties"] = 0
                    opposition_dict[player][opposition]["thirties"] = 0
                    opposition_dict[player][opposition]["zeros"] = 0
                    opposition_dict[player][opposition]["high_score"] = 0

                if opposition_dict[player][opposition]["balls"] != 0:
                    opposition_dict[player][opposition]["strike_rate"] = (
                        opposition_dict[player][opposition]["runs"]
                        * 100
                        / opposition_dict[player][opposition]["balls"]
                    )
                else:
                    opposition_dict[player][opposition][
                        "strike_rate"
                    ] = opposition_dict[player][opposition]["runs"]
                if opposition_dict[player][opposition]["wickets"] == 0:
                    opposition_dict[player][opposition]["average"] = opposition_dict[
                        player
                    ][opposition]["runs"]
                else:
                    opposition_dict[player][opposition]["average"] = (
                        opposition_dict[player][opposition]["runs"]
                        / opposition_dict[player][opposition]["wickets"]
                    )

                match_batsman_details.loc[count, "opposition"] = (
                    0.4262 * opposition_dict[player][opposition]["average"]
                    + 0.2566 * opposition_dict[player][opposition]["innings"]
                    + 0.1510 * opposition_dict[player][opposition]["strike_rate"]
                    + 0.0787 * opposition_dict[player][opposition]["centuries"]
                    + 0.0556 * opposition_dict[player][opposition]["fifties"]
                    + 0.0328 * opposition_dict[player][opposition]["zeros"]
                )
                # if match_batsman_details.loc[count,'opposition'] > 0:
                #     print('hi')
                opposition_dict[player][opposition]["innings"] += 1
                opposition_dict[player][opposition]["runs"] += player_details.loc[
                    player, "runs"
                ]
                opposition_dict[player][opposition]["balls"] += player_details.loc[
                    player, "balls"
                ]
                opposition_dict[player][opposition]["wickets"] += (
                    1 - player_details.loc[player, "not_out"]
                )
                if player_details.loc[player, "runs"] >= 100:
                    opposition_dict[player][opposition]["centuries"] += 1
                elif player_details.loc[player, "runs"] >= 50:
                    opposition_dict[player][opposition]["fifties"] += 1
                elif player_details.loc[player, "runs"] >= 30:
                    opposition_dict[player][opposition]["thirties"] += 1
                elif player_details.loc[player, "runs"] == 0:
                    opposition_dict[player][opposition]["zeros"] += 1
                if (
                    player_details.loc[player, "runs"]
                    > opposition_dict[player][opposition]["high_score"]
                ):
                    opposition_dict[player][opposition][
                        "high_score"
                    ] = player_details.loc[player, "runs"]

                match_batsman_details.loc[count, "consistency"] = (
                    0.4262 * match_batsman_details.loc[count, "previous_average"]
                    + 0.2566 * match_batsman_details.loc[count, "innings_played"]
                    + 0.1510 * match_batsman_details.loc[count, "previous_strike_rate"]
                    + 0.0787 * match_batsman_details.loc[count, "previous_centuries"]
                    + 0.0556 * match_batsman_details.loc[count, "previous_fifties"]
                    - 0.0328 * match_batsman_details.loc[count, "previous_zeros"]
                )
                indices = match_batsman_details[
                    (match_batsman_details["player_name"] == player)
                    & (match_batsman_details.index < count)
                ].index
                if len(indices) == 0:
                    match_batsman_details.loc[count, "form"] = 0
                else:
                    cur = match_batsman_details.loc[count]
                    old = match_batsman_details.loc[count - min(10, len(indices))]
                    try:
                        avg = (cur["previous_runs"] - old["previous_runs"]) / (
                            cur["previous_outs"] - old["previous_outs"]
                        )
                    except:
                        avg = 0
                    try:
                        sr = (
                            (cur["previous_runs"] - old["previous_runs"])
                            * 100
                            / (cur["previous_balls"] - old["previous_balls"])
                        )
                    except:
                        sr = 0
                    cent = cur["previous_centuries"] - old["previous_centuries"]
                    fift = cur["previous_fifties"] - old["previous_fifties"]
                    zer = cur["previous_zeros"] - old["previous_zeros"]
                    inn = min(10, len(indices))
                    match_batsman_details.loc[count, "form"] = (
                        0.4262 * avg
                        + 0.2566 * inn
                        + 0.1510 * sr
                        + 0.0787 * cent
                        + 0.0556 * fift
                        - 0.0328 * (zer)
                    )

                # match_batsman_details.loc[count,'form']=0.4262*tokenize(match_batsman_details.loc[count,'previous_average'],{0:1,10:2,20:3,30:4,40:5})+0.2566*tokenize(match_batsman_details.loc[count,'innings_played'],{1:1,5:2,10:3,12:4,15:5})+0.1510*tokenize(match_batsman_details.loc[count,'previous_strike_rate'],{0:1,50:2,60:3,80:4,100:5})+0.0787*tokenize(match_batsman_details.loc[count,'previous_centuries'],{0:1,2:2,3:3,4:4,5:5})+0.0556*tokenize(match_batsman_details.loc[count,'previous_fifties'],{0:1,3:2,5:3,7:4,10:5})-0.0328*tokenize(match_batsman_details.loc[count,'previous_zeros'],{0:1,2:2,3:3,4:4,5:5})

                match_batsman_details.loc[
                    count, "match_runs"
                ] = match_batsman_details.loc[count, "runs"]
                match_batsman_details.loc[
                    count, "match_4s"
                ] = match_batsman_details.loc[count, "4s"]
                match_batsman_details.loc[
                    count, "match_6s"
                ] = match_batsman_details.loc[count, "6s"]
                match_batsman_details.loc[count, "match_strike_rate"] = (
                    (
                        player_details.loc[player, "runs"]
                        * 100
                        / player_details.loc[player, "balls"]
                    )
                    if player_details.loc[player, "balls"] != 0
                    else 0
                )
                bonus = 0
                if match_batsman_details.loc[count, "match_runs"] >= 100:
                    bonus = 16
                elif match_batsman_details.loc[count, "match_runs"] >= 50:
                    bonus = 8
                elif match_batsman_details.loc[count, "match_runs"] >= 30:
                    bonus = 4
                elif match_batsman_details.loc[count, "match_runs"] == 0:
                    bonus = -2
                sr = 0
                try:
                    sr = (
                        player_details.loc[player, "runs"]
                        * 100
                        / player_details.loc[player, "balls"]
                    )
                except:
                    pass
                if player_details.loc[player, "balls"] >= 10:
                    if sr >= 170:
                        bonus += 6
                    elif sr >= 150:
                        bonus += 4
                    elif sr >= 130:
                        bonus += 2
                    if sr < 50:
                        bonus -= 6
                    elif sr < 60:
                        bonus -= 4
                    elif sr < 70:
                        bonus -= 2
                match_batsman_details.loc[count, "match_fantasy_points"] = (
                    match_batsman_details.loc[count, "match_runs"]
                    + match_batsman_details.loc[count, "match_4s"]
                    + 2 * match_batsman_details.loc[count, "match_6s"]
                    + bonus
                )

        overall_batsman_details.index.name = "player_name"

        # UNCOMMENT TO ADD IDS

        location = os.path.join(
            "data", "raw", "additional_data", "people_with_images_and_countries.csv"
        )
        mapping = pd.read_csv(location)

        for i in range(len(match_batsman_details)):
            name = match_batsman_details.iloc[i]["player_name"]
            matched = mapping[mapping["unique_name"] == name]

            if not matched.empty:
                match_batsman_details.iloc[
                    i, match_batsman_details.columns.get_loc("player_id")
                ] = matched["identifier"].values[0]
            else:
                # print(f"No matching entry for {name}: {len(mapping[mapping['unique_name'] == name])} matches")
                match_batsman_details.iloc[
                    i, match_batsman_details.columns.get_loc("player_id")
                ] = "xxxxxxxx"

        target_columns = [
            "match_runs",
            "match_4s",
            "match_6s",
            "match_strike_rate",
            "match_fantasy_points",
        ]
        for target_column in target_columns:
            if target_column in match_batsman_details.columns:
                new_column_name = f"{format}_{target_column}"
                match_batsman_details.rename(
                    columns={target_column: new_column_name}, inplace=True
                )
            else:
                print(f"Column '{target_column}' not found in batsman. Skipping...")

        folder = os.path.join("data", "interim", format)
        os.makedirs(folder, exist_ok=True)
        file_name = "simple_match_batsman_details_1_withids.csv"
        match_batsman_details.to_csv(os.path.join(folder, file_name))

    j = -1
    for format in formats:
        if format[0] == "W":
            form = format[1:]
        else:
            form = format
        date_file_pair = (grouped.get_group(form))["filename"]
        overall_batsman_details = pd.DataFrame(
            columns=[
                "team",
                "innings",
                "runs",
                "balls",
                "balls_involved",
                "outs",
                "average",
                "strike_rate",
                "centuries",
                "fifties",
                "thirties",
                "zeros",
                "4s",
                "6s",
                "spin_runs_b1",
                "spin_runs_b2",
                "spin_runs_b3",
                "pace_runs_b1",
                "pace_runs_b2",
                "pace_runs_b3",
                "spin_balls_b1",
                "spin_balls_b2",
                "spin_balls_b3",
                "pace_balls_b1",
                "pace_balls_b2",
                "pace_balls_b3",
                "spin_wickets_b1",
                "spin_wickets_b2",
                "spin_wickets_b3",
                "pace_wickets_b1",
                "pace_wickets_b2",
                "pace_wickets_b3",
                "spin_4s_b1",
                "spin_4s_b2",
                "spin_4s_b3",
                "pace_4s_b1",
                "pace_4s_b2",
                "pace_4s_b3",
                "spin_6s_b1",
                "spin_6s_b2",
                "spin_6s_b3",
                "pace_6s_b1",
                "pace_6s_b2",
                "pace_6s_b3",
            ]
        )
        match_batsman_details = pd.DataFrame(
            columns=[
                "date",
                "match_id",
                "player_name",
                "player_id",
                "team",
                "opposition_name",
                "venue_name",
                "innings_played",
                "previous_balls",
                "previous_balls_involved",
                "previous_outs",
                "previous_average",
                "previous_strike_rate",
                "previous_centuries",
                "previous_fifties",
                "previous_thirties",
                "previous_zeros",
                "previous_runs",
                "previous_4s",
                "previous_6s",
                "runs",
                "dots",
                "4s",
                "6s",
                "balls_involved",
                "balls",
                "not_out",
                "average",
                "strike_rate",
                "highest_score",
                "match_runs",
                "match_4s",
                "match_6s",
                "match_strike_rate",
                "match_fantasy_points",
            ]
        )

        venue_dict = {}
        venue_player_dict = {}
        venue_player_df = pd.DataFrame()
        player_highest_score = {}
        count = -1

        print("To process " + str(len(date_file_pair)) + " files for " + format)
        j += 1
        i = matchid_mapping[j]
        for ele in date_file_pair:
            i += 1
            if i % 10 == 0:
                print(i - matchid_mapping[j])
                # break

            location = os.path.join(
                "data", "raw", "cricsheet_data", "all_" + gender, ele
            )
            match_details, player_details = extract_details(location)

            for player in player_details.index:
                count += 1
                try:
                    overall_batsman_details.index.get_loc(player)
                except:
                    overall_batsman_details.loc[player, "team"] = player_details.loc[
                        player, "team"
                    ]
                    overall_batsman_details.loc[player, "innings"] = [0]
                    overall_batsman_details.loc[player, "runs"] = [0]
                    overall_batsman_details.loc[player, "balls"] = [0]
                    overall_batsman_details.loc[player, "balls_involved"] = [0]
                    overall_batsman_details.loc[player, "outs"] = [0]
                    overall_batsman_details.loc[player, "strike_rate"] = [0]
                    overall_batsman_details.loc[player, "average"] = [0]
                    overall_batsman_details.loc[player, "zeros"] = [0]
                    overall_batsman_details.loc[player, "thirties"] = [0]
                    overall_batsman_details.loc[player, "fifties"] = [0]
                    overall_batsman_details.loc[player, "centuries"] = [0]
                    overall_batsman_details.loc[player, "4s"] = [0]
                    overall_batsman_details.loc[player, "6s"] = [0]

                    overall_batsman_details.loc[player, "spin_runs_b1"] = [0]
                    overall_batsman_details.loc[player, "spin_runs_b2"] = [0]
                    overall_batsman_details.loc[player, "spin_runs_b3"] = [0]
                    overall_batsman_details.loc[player, "pace_runs_b1"] = [0]
                    overall_batsman_details.loc[player, "pace_runs_b2"] = [0]
                    overall_batsman_details.loc[player, "pace_runs_b3"] = [0]
                    overall_batsman_details.loc[player, "spin_balls_b1"] = [0]
                    overall_batsman_details.loc[player, "spin_balls_b2"] = [0]
                    overall_batsman_details.loc[player, "spin_balls_b3"] = [0]
                    overall_batsman_details.loc[player, "pace_balls_b1"] = [0]
                    overall_batsman_details.loc[player, "pace_balls_b2"] = [0]
                    overall_batsman_details.loc[player, "pace_balls_b3"] = [0]
                    overall_batsman_details.loc[player, "spin_wickets_b1"] = [0]
                    overall_batsman_details.loc[player, "spin_wickets_b2"] = [0]
                    overall_batsman_details.loc[player, "spin_wickets_b3"] = [0]
                    overall_batsman_details.loc[player, "pace_wickets_b1"] = [0]
                    overall_batsman_details.loc[player, "pace_wickets_b2"] = [0]
                    overall_batsman_details.loc[player, "pace_wickets_b3"] = [0]
                    overall_batsman_details.loc[player, "spin_4s_b1"] = [0]
                    overall_batsman_details.loc[player, "spin_4s_b2"] = [0]
                    overall_batsman_details.loc[player, "spin_4s_b3"] = [0]
                    overall_batsman_details.loc[player, "pace_4s_b1"] = [0]
                    overall_batsman_details.loc[player, "pace_4s_b2"] = [0]
                    overall_batsman_details.loc[player, "pace_4s_b3"] = [0]
                    overall_batsman_details.loc[player, "spin_6s_b1"] = [0]
                    overall_batsman_details.loc[player, "spin_6s_b2"] = [0]
                    overall_batsman_details.loc[player, "spin_6s_b3"] = [0]
                    overall_batsman_details.loc[player, "pace_6s_b1"] = [0]
                    overall_batsman_details.loc[player, "pace_6s_b2"] = [0]
                    overall_batsman_details.loc[player, "pace_6s_b3"] = [0]

                match_batsman_details.loc[count, "date"] = player_details.loc[
                    player, "date"
                ]
                match_batsman_details.loc[count, "name"] = player
                match_batsman_details.loc[count, "team"] = player_details.loc[
                    player, "team"
                ]
                match_batsman_details.loc[
                    count, "opposition_name"
                ] = player_details.loc[player, "opposition_name"]
                match_batsman_details.loc[count, "venue_name"] = match_details[
                    "venue_name"
                ]
                match_batsman_details.loc[count, "city"] = match_details["city"]
                match_batsman_details.loc[
                    count, "innings_played"
                ] = overall_batsman_details.loc[player, "innings"][-1]
                match_batsman_details.loc[
                    count, "previous_balls"
                ] = overall_batsman_details.loc[player, "balls"][-1]
                match_batsman_details.loc[
                    count, "previous_balls_involved"
                ] = overall_batsman_details.loc[player, "balls_involved"][-1]
                match_batsman_details.loc[
                    count, "previous_outs"
                ] = overall_batsman_details.loc[player, "outs"][-1]

                match_batsman_details.loc[count, "hist_spin_runs_b1"] = sum(
                    overall_batsman_details.loc[player, "spin_runs_b1"]
                )
                match_batsman_details.loc[count, "hist_spin_runs_b2"] = sum(
                    overall_batsman_details.loc[player, "spin_runs_b2"]
                )
                match_batsman_details.loc[count, "hist_spin_runs_b3"] = sum(
                    overall_batsman_details.loc[player, "spin_runs_b3"]
                )
                match_batsman_details.loc[count, "hist_pace_runs_b1"] = sum(
                    overall_batsman_details.loc[player, "pace_runs_b1"]
                )
                match_batsman_details.loc[count, "hist_pace_runs_b2"] = sum(
                    overall_batsman_details.loc[player, "pace_runs_b2"]
                )
                match_batsman_details.loc[count, "hist_pace_runs_b3"] = sum(
                    overall_batsman_details.loc[player, "pace_runs_b3"]
                )
                match_batsman_details.loc[count, "hist_spin_balls_b1"] = sum(
                    overall_batsman_details.loc[player, "spin_balls_b1"]
                )
                match_batsman_details.loc[count, "hist_spin_balls_b2"] = sum(
                    overall_batsman_details.loc[player, "spin_balls_b2"]
                )
                match_batsman_details.loc[count, "hist_spin_balls_b3"] = sum(
                    overall_batsman_details.loc[player, "spin_balls_b3"]
                )
                match_batsman_details.loc[count, "hist_pace_balls_b1"] = sum(
                    overall_batsman_details.loc[player, "pace_balls_b1"]
                )
                match_batsman_details.loc[count, "hist_pace_balls_b2"] = sum(
                    overall_batsman_details.loc[player, "pace_balls_b2"]
                )
                match_batsman_details.loc[count, "hist_pace_balls_b3"] = sum(
                    overall_batsman_details.loc[player, "pace_balls_b3"]
                )
                match_batsman_details.loc[count, "tbaHs_dismissals_1"] = sum(
                    overall_batsman_details.loc[player, "spin_wickets_b1"]
                )
                match_batsman_details.loc[count, "tbaHs_dismissals_2"] = sum(
                    overall_batsman_details.loc[player, "spin_wickets_b2"]
                )
                match_batsman_details.loc[count, "tbaHs_dismissals_3"] = sum(
                    overall_batsman_details.loc[player, "spin_wickets_b3"]
                )
                match_batsman_details.loc[count, "tbaHp_dismissals_1"] = sum(
                    overall_batsman_details.loc[player, "pace_wickets_b1"]
                )
                match_batsman_details.loc[count, "tbaHp_dismissals_2"] = sum(
                    overall_batsman_details.loc[player, "pace_wickets_b2"]
                )
                match_batsman_details.loc[count, "tbaHp_dismissals_3"] = sum(
                    overall_batsman_details.loc[player, "pace_wickets_b3"]
                )
                match_batsman_details.loc[count, "tbaHs_6s_1"] = sum(
                    overall_batsman_details.loc[player, "spin_6s_b1"]
                )
                match_batsman_details.loc[count, "tbaHs_6s_2"] = sum(
                    overall_batsman_details.loc[player, "spin_6s_b2"]
                )
                match_batsman_details.loc[count, "tbaHs_6s_3"] = sum(
                    overall_batsman_details.loc[player, "spin_6s_b3"]
                )
                match_batsman_details.loc[count, "tbaHp_6s_1"] = sum(
                    overall_batsman_details.loc[player, "pace_6s_b1"]
                )
                match_batsman_details.loc[count, "tbaHp_6s_2"] = sum(
                    overall_batsman_details.loc[player, "pace_6s_b2"]
                )
                match_batsman_details.loc[count, "tbaHp_6s_3"] = sum(
                    overall_batsman_details.loc[player, "pace_6s_b3"]
                )
                match_batsman_details.loc[count, "tbaHs_4s_1"] = sum(
                    overall_batsman_details.loc[player, "spin_4s_b1"]
                )
                match_batsman_details.loc[count, "tbaHs_4s_2"] = sum(
                    overall_batsman_details.loc[player, "spin_4s_b2"]
                )
                match_batsman_details.loc[count, "tbaHs_4s_3"] = sum(
                    overall_batsman_details.loc[player, "spin_4s_b3"]
                )
                match_batsman_details.loc[count, "tbaHp_4s_1"] = sum(
                    overall_batsman_details.loc[player, "pace_4s_b1"]
                )
                match_batsman_details.loc[count, "tbaHp_4s_2"] = sum(
                    overall_batsman_details.loc[player, "pace_4s_b2"]
                )
                match_batsman_details.loc[count, "tbaHp_4s_3"] = sum(
                    overall_batsman_details.loc[player, "pace_4s_b3"]
                )
                match_batsman_details.loc[
                    count, "tbaHs_economy_1"
                ] = match_batsman_details.loc[count, "hist_spin_runs_b1"] / (
                    match_batsman_details.loc[count, "hist_spin_balls_b1"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHs_economy_2"
                ] = match_batsman_details.loc[count, "hist_spin_runs_b2"] / (
                    match_batsman_details.loc[count, "hist_spin_balls_b2"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHs_economy_3"
                ] = match_batsman_details.loc[count, "hist_spin_runs_b3"] / (
                    match_batsman_details.loc[count, "hist_spin_balls_b3"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHp_economy_1"
                ] = match_batsman_details.loc[count, "hist_pace_runs_b1"] / (
                    match_batsman_details.loc[count, "hist_pace_balls_b1"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHp_economy_2"
                ] = match_batsman_details.loc[count, "hist_pace_runs_b2"] / (
                    match_batsman_details.loc[count, "hist_pace_balls_b2"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHp_economy_3"
                ] = match_batsman_details.loc[count, "hist_pace_runs_b3"] / (
                    match_batsman_details.loc[count, "hist_pace_balls_b3"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHr_economy_1"
                ] = match_batsman_details.loc[count, "tbaHs_economy_1"] / (
                    match_batsman_details.loc[count, "tbaHp_economy_1"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHr_economy_2"
                ] = match_batsman_details.loc[count, "tbaHs_economy_2"] / (
                    match_batsman_details.loc[count, "tbaHp_economy_2"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHr_economy_3"
                ] = match_batsman_details.loc[count, "tbaHs_economy_3"] / (
                    match_batsman_details.loc[count, "tbaHp_economy_3"] + 0.1
                )

                match_batsman_details.loc[
                    count, "tbaHr_4s_1"
                ] = match_batsman_details.loc[count, "tbaHs_4s_1"] / (
                    match_batsman_details.loc[count, "tbaHp_4s_1"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHr_4s_2"
                ] = match_batsman_details.loc[count, "tbaHs_4s_2"] / (
                    match_batsman_details.loc[count, "tbaHp_4s_2"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHr_4s_3"
                ] = match_batsman_details.loc[count, "tbaHs_4s_3"] / (
                    match_batsman_details.loc[count, "tbaHp_4s_3"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHr_6s_1"
                ] = match_batsman_details.loc[count, "tbaHs_6s_1"] / (
                    match_batsman_details.loc[count, "tbaHp_6s_1"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHr_6s_2"
                ] = match_batsman_details.loc[count, "tbaHs_6s_2"] / (
                    match_batsman_details.loc[count, "tbaHp_6s_2"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHr_6s_3"
                ] = match_batsman_details.loc[count, "tbaHs_6s_3"] / (
                    match_batsman_details.loc[count, "tbaHp_6s_3"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHr_dismissals_1"
                ] = match_batsman_details.loc[count, "tbaHs_dismissals_1"] / (
                    match_batsman_details.loc[count, "tbaHp_dismissals_1"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHr_dismissals_2"
                ] = match_batsman_details.loc[count, "tbaHs_dismissals_2"] / (
                    match_batsman_details.loc[count, "tbaHp_dismissals_2"] + 0.1
                )
                match_batsman_details.loc[
                    count, "tbaHr_dismissals_3"
                ] = match_batsman_details.loc[count, "tbaHs_dismissals_3"] / (
                    match_batsman_details.loc[count, "tbaHp_dismissals_3"] + 0.1
                )
                match_batsman_details.loc[count, "tbaHs_economy_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in [
                            "hist_spin_runs_b1",
                            "hist_spin_runs_b2",
                            "hist_spin_runs_b3",
                        ]
                    ]
                ) / (
                    sum(
                        [
                            match_batsman_details.loc[count, i]
                            for i in [
                                "hist_spin_balls_b1",
                                "hist_spin_balls_b2",
                                "hist_spin_balls_b3",
                            ]
                        ]
                    )
                    + 0.1
                )
                match_batsman_details.loc[count, "tbaHp_economy_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in [
                            "hist_pace_runs_b1",
                            "hist_pace_runs_b2",
                            "hist_pace_runs_b3",
                        ]
                    ]
                ) / (
                    sum(
                        [
                            match_batsman_details.loc[count, i]
                            for i in [
                                "hist_pace_balls_b1",
                                "hist_pace_balls_b2",
                                "hist_pace_balls_b3",
                            ]
                        ]
                    )
                    + 0.1
                )
                match_batsman_details.loc[count, "tbaHr_economy_agg"] = (
                    match_batsman_details.loc[count, "tbaHs_economy_agg"]
                    / match_batsman_details.loc[count, "tbaHp_economy_agg"]
                )
                match_batsman_details.loc[count, "tbaHs_4s_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in ["tbaHs_4s_1", "tbaHs_4s_2", "tbaHs_4s_3"]
                    ]
                )
                match_batsman_details.loc[count, "tbaHp_4s_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in ["tbaHp_4s_1", "tbaHp_4s_2", "tbaHp_4s_3"]
                    ]
                )
                match_batsman_details.loc[count, "tbaHr_4s_agg"] = (
                    match_batsman_details.loc[count, "tbaHs_4s_agg"]
                    / match_batsman_details.loc[count, "tbaHp_4s_agg"]
                )
                match_batsman_details.loc[count, "tbaHs_6s_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in ["tbaHs_6s_1", "tbaHs_6s_2", "tbaHs_6s_3"]
                    ]
                )
                match_batsman_details.loc[count, "tbaHp_6s_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in ["tbaHp_6s_1", "tbaHp_6s_2", "tbaHp_6s_3"]
                    ]
                )
                match_batsman_details.loc[count, "tbaHr_6s_agg"] = (
                    match_batsman_details.loc[count, "tbaHs_6s_agg"]
                    / match_batsman_details.loc[count, "tbaHp_6s_agg"]
                )
                match_batsman_details.loc[count, "tbaHs_dismissals_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in [
                            "tbaHs_dismissals_1",
                            "tbaHs_dismissals_2",
                            "tbaHs_dismissals_3",
                        ]
                    ]
                )
                match_batsman_details.loc[count, "tbaHp_dismissals_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in [
                            "tbaHp_dismissals_1",
                            "tbaHp_dismissals_2",
                            "tbaHp_dismissals_3",
                        ]
                    ]
                )
                match_batsman_details.loc[count, "tbaHr_dismissals_agg"] = (
                    match_batsman_details.loc[count, "tbaHs_dismissals_agg"]
                    / match_batsman_details.loc[count, "tbaHp_dismissals_agg"]
                )

                match_batsman_details.loc[count, "form_spin_runs_b1"] = sum(
                    overall_batsman_details.loc[player, "spin_runs_b1"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "form_spin_runs_b2"] = sum(
                    overall_batsman_details.loc[player, "spin_runs_b2"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "form_spin_runs_b3"] = sum(
                    overall_batsman_details.loc[player, "spin_runs_b3"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "form_pace_runs_b1"] = sum(
                    overall_batsman_details.loc[player, "pace_runs_b1"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "form_pace_runs_b2"] = sum(
                    overall_batsman_details.loc[player, "pace_runs_b2"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "form_pace_runs_b3"] = sum(
                    overall_batsman_details.loc[player, "pace_runs_b3"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "form_spin_balls_b1"] = sum(
                    overall_batsman_details.loc[player, "spin_balls_b1"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "form_spin_balls_b2"] = sum(
                    overall_batsman_details.loc[player, "spin_balls_b2"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "form_spin_balls_b3"] = sum(
                    overall_batsman_details.loc[player, "spin_balls_b3"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "form_pace_balls_b1"] = sum(
                    overall_batsman_details.loc[player, "pace_balls_b1"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "form_pace_balls_b2"] = sum(
                    overall_batsman_details.loc[player, "pace_balls_b2"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "form_pace_balls_b3"] = sum(
                    overall_batsman_details.loc[player, "pace_balls_b3"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHs_dismissal_1"] = sum(
                    overall_batsman_details.loc[player, "spin_wickets_b1"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHs_dismissal_2"] = sum(
                    overall_batsman_details.loc[player, "spin_wickets_b2"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHs_dismissal_3"] = sum(
                    overall_batsman_details.loc[player, "spin_wickets_b3"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHp_dismissal_1"] = sum(
                    overall_batsman_details.loc[player, "pace_wickets_b1"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHp_dismissal_2"] = sum(
                    overall_batsman_details.loc[player, "pace_wickets_b2"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHp_dismissal_3"] = sum(
                    overall_batsman_details.loc[player, "pace_wickets_b3"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHs_6s_1"] = sum(
                    overall_batsman_details.loc[player, "spin_6s_b1"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHs_6s_2"] = sum(
                    overall_batsman_details.loc[player, "spin_6s_b2"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHs_6s_3"] = sum(
                    overall_batsman_details.loc[player, "spin_6s_b3"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHp_6s_1"] = sum(
                    overall_batsman_details.loc[player, "pace_6s_b1"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHp_6s_2"] = sum(
                    overall_batsman_details.loc[player, "pace_6s_b2"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHp_6s_3"] = sum(
                    overall_batsman_details.loc[player, "pace_6s_b3"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHs_4s_1"] = sum(
                    overall_batsman_details.loc[player, "spin_4s_b1"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHs_4s_2"] = sum(
                    overall_batsman_details.loc[player, "spin_4s_b2"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHs_4s_3"] = sum(
                    overall_batsman_details.loc[player, "spin_4s_b3"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHp_4s_1"] = sum(
                    overall_batsman_details.loc[player, "pace_4s_b1"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHp_4s_2"] = sum(
                    overall_batsman_details.loc[player, "pace_4s_b2"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )
                match_batsman_details.loc[count, "fbaHp_4s_3"] = sum(
                    overall_batsman_details.loc[player, "pace_4s_b3"][
                        -1
                        * min(
                            10, len(overall_batsman_details.loc[player, "spin_runs_b1"])
                        ) :
                    ]
                )

                match_batsman_details.loc[
                    count, "fbaHs_economy_1"
                ] = match_batsman_details.loc[count, "form_spin_runs_b1"] / (
                    match_batsman_details.loc[count, "form_spin_balls_b1"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHs_economy_2"
                ] = match_batsman_details.loc[count, "form_spin_runs_b2"] / (
                    match_batsman_details.loc[count, "form_spin_balls_b2"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHs_economy_3"
                ] = match_batsman_details.loc[count, "form_spin_runs_b3"] / (
                    match_batsman_details.loc[count, "form_spin_balls_b3"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHp_economy_1"
                ] = match_batsman_details.loc[count, "form_pace_runs_b1"] / (
                    match_batsman_details.loc[count, "form_pace_balls_b1"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHp_economy_2"
                ] = match_batsman_details.loc[count, "form_pace_runs_b2"] / (
                    match_batsman_details.loc[count, "form_pace_balls_b2"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHp_economy_3"
                ] = match_batsman_details.loc[count, "form_pace_runs_b3"] / (
                    match_batsman_details.loc[count, "form_pace_balls_b3"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHr_economy_1"
                ] = match_batsman_details.loc[count, "fbaHs_economy_1"] / (
                    match_batsman_details.loc[count, "fbaHp_economy_1"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHr_economy_2"
                ] = match_batsman_details.loc[count, "fbaHs_economy_2"] / (
                    match_batsman_details.loc[count, "fbaHp_economy_2"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHr_economy_3"
                ] = match_batsman_details.loc[count, "fbaHs_economy_3"] / (
                    match_batsman_details.loc[count, "fbaHp_economy_3"] + 0.1
                )

                match_batsman_details.loc[
                    count, "fbaHr_4s_1"
                ] = match_batsman_details.loc[count, "fbaHs_4s_1"] / (
                    match_batsman_details.loc[count, "fbaHp_4s_1"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHr_4s_2"
                ] = match_batsman_details.loc[count, "fbaHs_4s_2"] / (
                    match_batsman_details.loc[count, "fbaHp_4s_2"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHr_4s_3"
                ] = match_batsman_details.loc[count, "fbaHs_4s_3"] / (
                    match_batsman_details.loc[count, "fbaHp_4s_3"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHr_6s_1"
                ] = match_batsman_details.loc[count, "fbaHs_6s_1"] / (
                    match_batsman_details.loc[count, "fbaHp_6s_1"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHr_6s_2"
                ] = match_batsman_details.loc[count, "fbaHs_6s_2"] / (
                    match_batsman_details.loc[count, "fbaHp_6s_2"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHr_6s_3"
                ] = match_batsman_details.loc[count, "fbaHs_6s_3"] / (
                    match_batsman_details.loc[count, "fbaHp_6s_3"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHr_dismissals_1"
                ] = match_batsman_details.loc[count, "fbaHs_dismissal_1"] / (
                    match_batsman_details.loc[count, "fbaHp_dismissal_1"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHr_dismissals_2"
                ] = match_batsman_details.loc[count, "fbaHs_dismissal_2"] / (
                    match_batsman_details.loc[count, "fbaHp_dismissal_2"] + 0.1
                )
                match_batsman_details.loc[
                    count, "fbaHr_dismissals_3"
                ] = match_batsman_details.loc[count, "fbaHs_dismissal_3"] / (
                    match_batsman_details.loc[count, "fbaHp_dismissal_3"] + 0.1
                )
                match_batsman_details.loc[count, "fbaHs_economy_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in [
                            "form_spin_runs_b1",
                            "form_spin_runs_b2",
                            "form_spin_runs_b3",
                        ]
                    ]
                ) / (
                    sum(
                        [
                            match_batsman_details.loc[count, i]
                            for i in [
                                "form_spin_balls_b1",
                                "form_spin_balls_b2",
                                "form_spin_balls_b3",
                            ]
                        ]
                    )
                    + 0.1
                )
                match_batsman_details.loc[count, "fbaHp_economy_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in [
                            "form_pace_runs_b1",
                            "form_pace_runs_b2",
                            "form_pace_runs_b3",
                        ]
                    ]
                ) / (
                    sum(
                        [
                            match_batsman_details.loc[count, i]
                            for i in [
                                "form_pace_balls_b1",
                                "form_pace_balls_b2",
                                "form_pace_balls_b3",
                            ]
                        ]
                    )
                    + 0.1
                )
                match_batsman_details.loc[count, "fbaHr_economy_agg"] = (
                    match_batsman_details.loc[count, "fbaHs_economy_agg"]
                    / match_batsman_details.loc[count, "fbaHp_economy_agg"]
                )
                match_batsman_details.loc[count, "fbaHs_4s_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in ["fbaHs_4s_1", "fbaHs_4s_2", "fbaHs_4s_3"]
                    ]
                )
                match_batsman_details.loc[count, "fbaHp_4s_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in ["fbaHp_4s_1", "fbaHp_4s_2", "fbaHp_4s_3"]
                    ]
                )
                match_batsman_details.loc[count, "fbaHr_4s_agg"] = (
                    match_batsman_details.loc[count, "fbaHs_4s_agg"]
                    / match_batsman_details.loc[count, "fbaHp_4s_agg"]
                )
                match_batsman_details.loc[count, "fbaHs_6s_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in ["fbaHs_6s_1", "fbaHs_6s_2", "fbaHs_6s_3"]
                    ]
                )
                match_batsman_details.loc[count, "fbaHp_6s_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in ["fbaHp_6s_1", "fbaHp_6s_2", "fbaHp_6s_3"]
                    ]
                )
                match_batsman_details.loc[count, "fbaHr_6s_agg"] = (
                    match_batsman_details.loc[count, "fbaHs_6s_agg"]
                    / match_batsman_details.loc[count, "fbaHp_6s_agg"]
                )
                match_batsman_details.loc[count, "fbaHs_dismissals_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in [
                            "fbaHs_dismissal_1",
                            "fbaHs_dismissal_2",
                            "fbaHs_dismissal_3",
                        ]
                    ]
                )
                match_batsman_details.loc[count, "fbaHp_dismissals_agg"] = sum(
                    [
                        match_batsman_details.loc[count, i]
                        for i in [
                            "fbaHp_dismissal_1",
                            "fbaHp_dismissal_2",
                            "fbaHp_dismissal_3",
                        ]
                    ]
                )
                match_batsman_details.loc[count, "fbaHr_dismissals_agg"] = (
                    match_batsman_details.loc[count, "fbaHs_dismissals_agg"]
                    / match_batsman_details.loc[count, "fbaHp_dismissals_agg"]
                )

                overall_batsman_details.loc[player, "spin_runs_b1"].append(
                    player_details.loc[player, "spin_runs_b1"]
                )
                overall_batsman_details.loc[player, "spin_runs_b2"].append(
                    player_details.loc[player, "spin_runs_b2"]
                )
                overall_batsman_details.loc[player, "spin_runs_b3"].append(
                    player_details.loc[player, "spin_runs_b3"]
                )
                overall_batsman_details.loc[player, "pace_runs_b1"].append(
                    player_details.loc[player, "pace_runs_b1"]
                )
                overall_batsman_details.loc[player, "pace_runs_b2"].append(
                    player_details.loc[player, "pace_runs_b2"]
                )
                overall_batsman_details.loc[player, "pace_runs_b3"].append(
                    player_details.loc[player, "pace_runs_b3"]
                )
                overall_batsman_details.loc[player, "spin_balls_b1"].append(
                    player_details.loc[player, "spin_balls_b1"]
                )
                overall_batsman_details.loc[player, "spin_balls_b2"].append(
                    player_details.loc[player, "spin_balls_b2"]
                )
                overall_batsman_details.loc[player, "spin_balls_b3"].append(
                    player_details.loc[player, "spin_balls_b3"]
                )
                overall_batsman_details.loc[player, "pace_balls_b1"].append(
                    player_details.loc[player, "pace_balls_b1"]
                )
                overall_batsman_details.loc[player, "pace_balls_b2"].append(
                    player_details.loc[player, "pace_balls_b2"]
                )
                overall_batsman_details.loc[player, "pace_balls_b3"].append(
                    player_details.loc[player, "pace_balls_b3"]
                )
                overall_batsman_details.loc[player, "spin_wickets_b1"].append(
                    player_details.loc[player, "spin_wickets_b1"]
                )
                overall_batsman_details.loc[player, "spin_wickets_b2"].append(
                    player_details.loc[player, "spin_wickets_b2"]
                )
                overall_batsman_details.loc[player, "spin_wickets_b3"].append(
                    player_details.loc[player, "spin_wickets_b3"]
                )
                overall_batsman_details.loc[player, "pace_wickets_b1"].append(
                    player_details.loc[player, "pace_wickets_b1"]
                )
                overall_batsman_details.loc[player, "pace_wickets_b2"].append(
                    player_details.loc[player, "pace_wickets_b2"]
                )
                overall_batsman_details.loc[player, "pace_wickets_b3"].append(
                    player_details.loc[player, "pace_wickets_b3"]
                )
                overall_batsman_details.loc[player, "spin_6s_b1"].append(
                    player_details.loc[player, "spin_6s_b1"]
                )
                overall_batsman_details.loc[player, "spin_6s_b2"].append(
                    player_details.loc[player, "spin_6s_b2"]
                )
                overall_batsman_details.loc[player, "spin_6s_b3"].append(
                    player_details.loc[player, "spin_6s_b3"]
                )
                overall_batsman_details.loc[player, "pace_6s_b1"].append(
                    player_details.loc[player, "pace_6s_b1"]
                )
                overall_batsman_details.loc[player, "pace_6s_b2"].append(
                    player_details.loc[player, "pace_6s_b2"]
                )
                overall_batsman_details.loc[player, "pace_6s_b3"].append(
                    player_details.loc[player, "pace_6s_b3"]
                )
                overall_batsman_details.loc[player, "spin_4s_b1"].append(
                    player_details.loc[player, "spin_4s_b1"]
                )
                overall_batsman_details.loc[player, "spin_4s_b2"].append(
                    player_details.loc[player, "spin_4s_b2"]
                )
                overall_batsman_details.loc[player, "spin_4s_b3"].append(
                    player_details.loc[player, "spin_4s_b3"]
                )
                overall_batsman_details.loc[player, "pace_4s_b1"].append(
                    player_details.loc[player, "pace_4s_b1"]
                )
                overall_batsman_details.loc[player, "pace_4s_b2"].append(
                    player_details.loc[player, "pace_4s_b2"]
                )
                overall_batsman_details.loc[player, "pace_4s_b3"].append(
                    player_details.loc[player, "pace_4s_b3"]
                )
                match_batsman_details.loc[
                    count, "spin_runs_b1"
                ] = overall_batsman_details.loc[player, "spin_runs_b1"][-1]
                match_batsman_details.loc[
                    count, "spin_runs_b2"
                ] = overall_batsman_details.loc[player, "spin_runs_b2"][-1]
                match_batsman_details.loc[
                    count, "spin_runs_b3"
                ] = overall_batsman_details.loc[player, "spin_runs_b3"][-1]
                match_batsman_details.loc[
                    count, "pace_runs_b1"
                ] = overall_batsman_details.loc[player, "pace_runs_b1"][-1]
                match_batsman_details.loc[
                    count, "pace_runs_b2"
                ] = overall_batsman_details.loc[player, "pace_runs_b2"][-1]
                match_batsman_details.loc[
                    count, "pace_runs_b3"
                ] = overall_batsman_details.loc[player, "pace_runs_b3"][-1]
                match_batsman_details.loc[
                    count, "spin_balls_b1"
                ] = overall_batsman_details.loc[player, "spin_balls_b1"][-1]
                match_batsman_details.loc[
                    count, "spin_balls_b2"
                ] = overall_batsman_details.loc[player, "spin_balls_b2"][-1]
                match_batsman_details.loc[
                    count, "spin_balls_b3"
                ] = overall_batsman_details.loc[player, "spin_balls_b3"][-1]
                match_batsman_details.loc[
                    count, "pace_balls_b1"
                ] = overall_batsman_details.loc[player, "pace_balls_b1"][-1]
                match_batsman_details.loc[
                    count, "pace_balls_b2"
                ] = overall_batsman_details.loc[player, "pace_balls_b2"][-1]
                match_batsman_details.loc[
                    count, "pace_balls_b3"
                ] = overall_batsman_details.loc[player, "pace_balls_b3"][-1]
                match_batsman_details.loc[
                    count, "spin_wickets_b1"
                ] = overall_batsman_details.loc[player, "spin_wickets_b1"][-1]
                match_batsman_details.loc[
                    count, "spin_wickets_b2"
                ] = overall_batsman_details.loc[player, "spin_wickets_b2"][-1]
                match_batsman_details.loc[
                    count, "spin_wickets_b3"
                ] = overall_batsman_details.loc[player, "spin_wickets_b3"][-1]
                match_batsman_details.loc[
                    count, "pace_wickets_b1"
                ] = overall_batsman_details.loc[player, "pace_wickets_b1"][-1]
                match_batsman_details.loc[
                    count, "pace_wickets_b2"
                ] = overall_batsman_details.loc[player, "pace_wickets_b2"][-1]
                match_batsman_details.loc[
                    count, "pace_wickets_b3"
                ] = overall_batsman_details.loc[player, "pace_wickets_b3"][-1]
                match_batsman_details.loc[
                    count, "spin_6s_b1"
                ] = overall_batsman_details.loc[player, "spin_6s_b1"][-1]
                match_batsman_details.loc[
                    count, "spin_6s_b2"
                ] = overall_batsman_details.loc[player, "spin_6s_b2"][-1]
                match_batsman_details.loc[
                    count, "spin_6s_b3"
                ] = overall_batsman_details.loc[player, "spin_6s_b3"][-1]
                match_batsman_details.loc[
                    count, "pace_6s_b1"
                ] = overall_batsman_details.loc[player, "pace_6s_b1"][-1]
                match_batsman_details.loc[
                    count, "pace_6s_b2"
                ] = overall_batsman_details.loc[player, "pace_6s_b2"][-1]
                match_batsman_details.loc[
                    count, "pace_6s_b3"
                ] = overall_batsman_details.loc[player, "pace_6s_b3"][-1]
                match_batsman_details.loc[
                    count, "spin_4s_b1"
                ] = overall_batsman_details.loc[player, "spin_4s_b1"][-1]
                match_batsman_details.loc[
                    count, "spin_4s_b2"
                ] = overall_batsman_details.loc[player, "spin_4s_b2"][-1]
                match_batsman_details.loc[
                    count, "spin_4s_b3"
                ] = overall_batsman_details.loc[player, "spin_4s_b3"][-1]
                match_batsman_details.loc[
                    count, "pace_4s_b1"
                ] = overall_batsman_details.loc[player, "pace_4s_b1"][-1]
                match_batsman_details.loc[
                    count, "pace_4s_b2"
                ] = overall_batsman_details.loc[player, "pace_4s_b2"][-1]
                match_batsman_details.loc[
                    count, "pace_4s_b3"
                ] = overall_batsman_details.loc[player, "pace_4s_b3"][-1]

                venue = match_details["venue_name"]

                # putting stuff in venue dict
                if venue not in venue_player_dict.keys():
                    venue_player_dict[venue] = {}
                if player not in venue_player_dict[venue].keys():
                    venue_player_dict[venue][player] = {}
                    venue_player_dict[venue][player]["date"] = ""
                    venue_player_dict[venue][player]["name"] = ""
                    venue_player_dict[venue][player]["opposition_name"] = ""

                    venue_player_dict[venue][player]["venue_name"] = ""
                    venue_player_dict[venue][player]["team"] = ""
                    venue_player_dict[venue][player]["innings"] = 0
                    venue_player_dict[venue][player]["vbaHr_4s_agg"] = 0
                    venue_player_dict[venue][player]["vbaHr_6s_agg"] = 0
                    venue_player_dict[venue][player]["s4/inning"] = 0
                    venue_player_dict[venue][player]["s6/inning"] = 0
                    venue_player_dict[venue][player]["p6/inning"] = 0
                    venue_player_dict[venue][player]["p4/inning"] = 0
                    venue_player_dict[venue][player]["sw/pw"] = 0
                    venue_player_dict[venue][player]["spe/pe"] = 0
                    venue_player_dict[venue][player]["caught"] = 0
                    venue_player_dict[venue][player]["runouts"] = 0
                    venue_player_dict[venue][player]["stumpings"] = 0
                    venue_player_dict[venue][player]["bowled"] = 0
                    venue_player_dict[venue][player]["total_wicks"] = 0
                    venue_player_dict[venue][player]["dismissals/innings"] = 0
                    venue_player_dict[venue][player]["dismissals_b1/innings"] = 0
                    venue_player_dict[venue][player]["dismissals_b2/innings"] = 0
                    venue_player_dict[venue][player]["dismissals_b3/innings"] = 0
                    venue_player_dict[venue][player]["bowled_b1/innings"] = 0
                    venue_player_dict[venue][player]["bowled_b2/innings"] = 0
                    venue_player_dict[venue][player]["bowled_b3/innings"] = 0
                    venue_player_dict[venue][player]["madien_b1/innings"] = 0
                    venue_player_dict[venue][player]["madien_b2/innings"] = 0
                    venue_player_dict[venue][player]["madien_b3/innings"] = 0
                    venue_player_dict[venue][player]["dismissals/innings"] = 0
                    venue_player_dict[venue][player]["dismissals_b1"] = 0
                    venue_player_dict[venue][player]["dismissals_b2"] = 0
                    venue_player_dict[venue][player]["dismissals_b3"] = 0
                    venue_player_dict[venue][player]["bowled_b1"] = 0
                    venue_player_dict[venue][player]["bowled_b2"] = 0
                    venue_player_dict[venue][player]["bowled_b3"] = 0
                    venue_player_dict[venue][player]["madien_b1"] = 0
                    venue_player_dict[venue][player]["madien_b2"] = 0
                    venue_player_dict[venue][player]["madien_b3"] = 0
                    venue_player_dict[venue][player]["runouts/i"] = 0
                    venue_player_dict[venue][player]["caught/i"] = 0
                    venue_player_dict[venue][player]["stumped/i"] = 0
                    venue_player_dict[venue][player]["bowled/i"] = 0
                    venue_player_dict[venue][player]["spin_runs_b1"] = 0
                    venue_player_dict[venue][player]["spin_runs_b2"] = 0
                    venue_player_dict[venue][player]["spin_runs_b3"] = 0
                    venue_player_dict[venue][player]["vbaHs_4s_1"] = 0
                    venue_player_dict[venue][player]["vbaHs_4s_2"] = 0
                    venue_player_dict[venue][player]["vbaHs_4s_3"] = 0
                    venue_player_dict[venue][player]["vbaHs_6s_1"] = 0
                    venue_player_dict[venue][player]["vbaHs_6s_2"] = 0
                    venue_player_dict[venue][player]["vbaHs_6s_3"] = 0
                    venue_player_dict[venue][player]["vbaHs_dismissals_1"] = 0
                    venue_player_dict[venue][player]["vbaHs_dismissals_2"] = 0
                    venue_player_dict[venue][player]["vbaHs_dismissals_3"] = 0
                    venue_player_dict[venue][player]["spin_balls_b1"] = 0
                    venue_player_dict[venue][player]["spin_balls_b2"] = 0
                    venue_player_dict[venue][player]["spin_balls_b3"] = 0
                    venue_player_dict[venue][player]["pace_runs_b1"] = 0
                    venue_player_dict[venue][player]["pace_runs_b2"] = 0
                    venue_player_dict[venue][player]["pace_runs_b3"] = 0
                    venue_player_dict[venue][player]["vbaHp_dismissals_1"] = 0
                    venue_player_dict[venue][player]["vbaHp_dismissals_2"] = 0
                    venue_player_dict[venue][player]["vbaHp_dismissals_3"] = 0
                    venue_player_dict[venue][player]["pace_balls_b1"] = 0
                    venue_player_dict[venue][player]["pace_balls_b2"] = 0
                    venue_player_dict[venue][player]["pace_balls_b3"] = 0
                    venue_player_dict[venue][player]["vbaHp_6s_1"] = 0
                    venue_player_dict[venue][player]["vbaHp_6s_2"] = 0
                    venue_player_dict[venue][player]["vbaHp_6s_3"] = 0
                    venue_player_dict[venue][player]["vbaHp_4s_1"] = 0
                    venue_player_dict[venue][player]["vbaHp_4s_2"] = 0
                    venue_player_dict[venue][player]["vbaHp_4s_3"] = 0
                    venue_player_dict[venue][player]["vbaHs_economy_1"] = 0
                    venue_player_dict[venue][player]["vbaHp_economy_1"] = 0
                    venue_player_dict[venue][player]["vbaHs_economy_2"] = 0
                    venue_player_dict[venue][player]["vbaHp_economy_2"] = 0
                    venue_player_dict[venue][player]["vbaHs_economy_3"] = 0
                    venue_player_dict[venue][player]["vbaHp_economy_3"] = 0
                    venue_player_dict[venue][player]["vbaHr_economy_1"] = 0
                    venue_player_dict[venue][player]["vbaHr_economy_2"] = 0
                    venue_player_dict[venue][player]["vbaHr_economy_3"] = 0
                    venue_player_dict[venue][player]["vbaHr_4s_1"] = 0
                    venue_player_dict[venue][player]["vbaHr_4s_2"] = 0
                    venue_player_dict[venue][player]["vbaHr_4s_3"] = 0
                    venue_player_dict[venue][player]["vbaHr_6s_1"] = 0
                    venue_player_dict[venue][player]["vbaHr_6s_2"] = 0
                    venue_player_dict[venue][player]["vbaHr_6s_3"] = 0
                    venue_player_dict[venue][player]["vbaHr_dismissals_1"] = 0
                    venue_player_dict[venue][player]["vbaHr_dismissals_2"] = 0
                    venue_player_dict[venue][player]["vbaHr_dismissals_3"] = 0
                    venue_player_dict[venue][player]["vbaHs_economy_agg"] = 0
                    venue_player_dict[venue][player]["vbaHp_economy_agg"] = 0
                    venue_player_dict[venue][player]["vbaHr_economy_agg"] = 0
                    venue_player_dict[venue][player]["vbaHs_4s_agg"] = 0
                    venue_player_dict[venue][player]["vbaHp_4s_agg"] = 0
                    venue_player_dict[venue][player]["vbaHr_4s_agg"] = 0
                    venue_player_dict[venue][player]["vbaHs_dismissals_agg"] = 0
                    venue_player_dict[venue][player]["vbaHp_dismissals_agg"] = 0
                    venue_player_dict[venue][player]["vbaHr_dismissals_agg"] = 0
                    venue_player_dict[venue][player]["vbaHs_6s_agg"] = 0
                    venue_player_dict[venue][player]["vbaHp_6s_agg"] = 0
                    venue_player_dict[venue][player]["vbaHr_6s_agg"] = 0
                    venue_player_dict[venue][player]["average"] = 0
                    venue_player_dict[venue][player]["average_4s"] = 0
                    venue_player_dict[venue][player]["average_6s"] = 0
                    venue_player_dict[venue][player]["average_balls_involved"] = 0
                    venue_player_dict[venue][player]["balls_involved"] = 0
                    venue_player_dict[venue][player]["balls"] = 0
                venue_player_dict[venue][player]["date"] = player_details.loc[
                    player, "date"
                ]
                venue_player_dict[venue][player]["name"] = player
                venue_player_dict[venue][player]["team"] = player_details.loc[
                    player, "team"
                ]
                venue_player_dict[venue][player][
                    "opposition_name"
                ] = player_details.loc[player, "opposition_name"]
                venue_player_dict[venue][player]["venue_name"] = match_details[
                    "venue_name"
                ]
                venue_player_dict[venue][player][
                    "dismissals_b1/innings"
                ] = venue_player_dict[venue][player]["dismissals_b1"] / (
                    venue_player_dict[venue][player]["innings"] + 0.1
                )
                venue_player_dict[venue][player][
                    "dismissals_b2/innings"
                ] = venue_player_dict[venue][player]["dismissals_b2"] / (
                    venue_player_dict[venue][player]["innings"] + 0.1
                )
                venue_player_dict[venue][player][
                    "dismissals_b3/innings"
                ] = venue_player_dict[venue][player]["dismissals_b3"] / (
                    venue_player_dict[venue][player]["innings"] + 0.1
                )
                venue_player_dict[venue][player][
                    "bowled_b1/innings"
                ] = venue_player_dict[venue][player]["bowled_b1"] / (
                    venue_player_dict[venue][player]["innings"] + 0.1
                )
                venue_player_dict[venue][player][
                    "bowled_b2/innings"
                ] = venue_player_dict[venue][player]["bowled_b2"] / (
                    venue_player_dict[venue][player]["innings"] + 0.1
                )
                venue_player_dict[venue][player][
                    "bowled_b3/innings"
                ] = venue_player_dict[venue][player]["bowled_b3"] / (
                    venue_player_dict[venue][player]["innings"] + 0.1
                )
                venue_player_dict[venue][player][
                    "madien_b1/innings"
                ] = venue_player_dict[venue][player]["madien_b1"] / (
                    venue_player_dict[venue][player]["innings"] + 0.1
                )
                venue_player_dict[venue][player][
                    "madien_b2/innings"
                ] = venue_player_dict[venue][player]["madien_b2"] / (
                    venue_player_dict[venue][player]["innings"] + 0.1
                )
                venue_player_dict[venue][player][
                    "madien_b3/innings"
                ] = venue_player_dict[venue][player]["madien_b3"] / (
                    venue_player_dict[venue][player]["innings"] + 0.1
                )

                venue_player_dict[venue][player]["runouts/i"] = venue_player_dict[
                    venue
                ][player]["runouts"] / (
                    venue_player_dict[venue][player]["innings"] + 0.1
                )
                venue_player_dict[venue][player]["caught/i"] = venue_player_dict[venue][
                    player
                ]["caught"] / (venue_player_dict[venue][player]["innings"] + 0.1)
                venue_player_dict[venue][player]["stumped/i"] = venue_player_dict[
                    venue
                ][player]["stumpings"] / (
                    venue_player_dict[venue][player]["innings"] + 0.1
                )
                venue_player_dict[venue][player]["bowled/i"] = venue_player_dict[venue][
                    player
                ]["bowled"] / (venue_player_dict[venue][player]["innings"] + 0.1)
                venue_player_dict[venue][player][
                    "dismissals/innings"
                ] = venue_player_dict[venue][player]["total_wicks"] / (
                    venue_player_dict[venue][player]["innings"] + 0.1
                )

                venue_player_dict[venue][player]["vbaHr_4s_agg"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in ["vbaHs_4s_1", "vbaHs_4s_2", "vbaHs_4s_3"]
                    ]
                ) / (
                    sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in ["vbaHp_4s_1", "vbaHp_4s_2", "vbaHp_4s_3"]
                        ]
                    )
                    + 0.1
                )
                venue_player_dict[venue][player]["vbaHr_6s_agg"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in ["vbaHs_6s_1", "vbaHs_6s_2", "vbaHs_6s_3"]
                    ]
                ) / (
                    sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in ["vbaHp_6s_1", "vbaHp_6s_2", "vbaHp_6s_3"]
                        ]
                    )
                    + 0.1
                )

                venue_player_dict[venue][player]["s4/inning"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in ["vbaHs_4s_1", "vbaHs_4s_2", "vbaHs_4s_3"]
                    ]
                ) / (venue_player_dict[venue][player]["innings"] + 0.1)
                venue_player_dict[venue][player]["p4/inning"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in ["vbaHp_4s_1", "vbaHp_4s_2", "vbaHp_4s_3"]
                    ]
                ) / (venue_player_dict[venue][player]["innings"] + 0.1)
                venue_player_dict[venue][player]["p6/inning"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in ["vbaHp_6s_1", "vbaHp_6s_2", "vbaHp_6s_3"]
                    ]
                ) / (venue_player_dict[venue][player]["innings"] + 0.1)

                venue_player_dict[venue][player]["s6/inning"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in ["vbaHs_6s_1", "vbaHs_6s_2", "vbaHs_6s_3"]
                    ]
                ) / (venue_player_dict[venue][player]["innings"] + 0.1)
                venue_player_dict[venue][player]["sw/pw"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in [
                            "vbaHs_dismissals_1",
                            "vbaHs_dismissals_2",
                            "vbaHs_dismissals_3",
                        ]
                    ]
                ) / (
                    sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in [
                                "vbaHp_dismissals_1",
                                "vbaHp_dismissals_2",
                                "vbaHp_dismissals_3",
                            ]
                        ]
                    )
                    + 0.1
                )
                venue_player_dict[venue][player]["spe/pe"] = (
                    sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in ["spin_runs_b1", "spin_runs_b2", "spin_runs_b3"]
                        ]
                    )
                    / (
                        sum(
                            [
                                venue_player_dict[venue][player][i]
                                for i in [
                                    "spin_balls_b1",
                                    "spin_balls_b2",
                                    "spin_balls_b3",
                                ]
                            ]
                        )
                        + 0.1
                    )
                    / (
                        sum(
                            [
                                venue_player_dict[venue][player][i]
                                for i in [
                                    "pace_runs_b1",
                                    "pace_runs_b2",
                                    "pace_runs_b3",
                                ]
                            ]
                        )
                        + 0.1
                    )
                    * sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in ["pace_balls_b1", "pace_balls_b2", "pace_balls_b3"]
                        ]
                    )
                )
                venue_player_dict[venue][player]["vbaHs_economy_1"] = venue_player_dict[
                    venue
                ][player]["spin_runs_b1"] / (
                    venue_player_dict[venue][player]["spin_balls_b1"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHs_economy_2"] = venue_player_dict[
                    venue
                ][player]["spin_runs_b2"] / (
                    venue_player_dict[venue][player]["spin_balls_b2"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHs_economy_3"] = venue_player_dict[
                    venue
                ][player]["spin_runs_b3"] / (
                    venue_player_dict[venue][player]["spin_balls_b3"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHp_economy_1"] = venue_player_dict[
                    venue
                ][player]["pace_runs_b1"] / (
                    venue_player_dict[venue][player]["pace_balls_b1"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHp_economy_2"] = venue_player_dict[
                    venue
                ][player]["pace_runs_b2"] / (
                    venue_player_dict[venue][player]["pace_balls_b2"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHp_economy_3"] = venue_player_dict[
                    venue
                ][player]["pace_runs_b3"] / (
                    venue_player_dict[venue][player]["pace_balls_b3"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHr_economy_1"] = venue_player_dict[
                    venue
                ][player]["vbaHs_economy_1"] / (
                    venue_player_dict[venue][player]["vbaHp_economy_1"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHr_economy_2"] = venue_player_dict[
                    venue
                ][player]["vbaHs_economy_2"] / (
                    venue_player_dict[venue][player]["vbaHp_economy_2"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHr_economy_3"] = venue_player_dict[
                    venue
                ][player]["vbaHs_economy_3"] / (
                    venue_player_dict[venue][player]["vbaHp_economy_3"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHr_4s_1"] = venue_player_dict[
                    venue
                ][player]["vbaHs_4s_1"] / (
                    venue_player_dict[venue][player]["vbaHp_4s_1"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHr_4s_2"] = venue_player_dict[
                    venue
                ][player]["vbaHs_4s_2"] / (
                    venue_player_dict[venue][player]["vbaHp_4s_2"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHr_4s_3"] = venue_player_dict[
                    venue
                ][player]["vbaHs_4s_3"] / (
                    venue_player_dict[venue][player]["vbaHp_4s_3"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHr_6s_1"] = venue_player_dict[
                    venue
                ][player]["vbaHs_6s_1"] / (
                    venue_player_dict[venue][player]["vbaHp_6s_1"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHr_6s_2"] = venue_player_dict[
                    venue
                ][player]["vbaHs_6s_2"] / (
                    venue_player_dict[venue][player]["vbaHp_6s_2"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHr_6s_3"] = venue_player_dict[
                    venue
                ][player]["vbaHs_6s_3"] / (
                    venue_player_dict[venue][player]["vbaHp_6s_3"] + 0.1
                )
                venue_player_dict[venue][player][
                    "vbaHr_dismissals_1"
                ] = venue_player_dict[venue][player]["vbaHs_dismissals_1"] / (
                    venue_player_dict[venue][player]["vbaHp_dismissals_1"] + 0.1
                )
                venue_player_dict[venue][player][
                    "vbaHr_dismissals_2"
                ] = venue_player_dict[venue][player]["vbaHs_dismissals_2"] / (
                    venue_player_dict[venue][player]["vbaHp_dismissals_2"] + 0.1
                )
                venue_player_dict[venue][player][
                    "vbaHr_dismissals_3"
                ] = venue_player_dict[venue][player]["vbaHs_dismissals_3"] / (
                    venue_player_dict[venue][player]["vbaHp_dismissals_3"] + 0.1
                )
                venue_player_dict[venue][player]["vbaHr_economy_agg"] = (
                    sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in ["spin_runs_b1", "spin_runs_b2", "spin_runs_b3"]
                        ]
                    )
                    / (
                        sum(
                            [
                                venue_player_dict[venue][player][i]
                                for i in [
                                    "spin_balls_b1",
                                    "spin_balls_b2",
                                    "spin_balls_b3",
                                ]
                            ]
                        )
                        + 0.1
                    )
                    / (
                        sum(
                            [
                                venue_player_dict[venue][player][i]
                                for i in [
                                    "pace_runs_b1",
                                    "pace_runs_b2",
                                    "pace_runs_b3",
                                ]
                            ]
                        )
                        + 0.1
                    )
                    * sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in ["pace_balls_b1", "pace_balls_b2", "pace_balls_b3"]
                        ]
                    )
                )
                venue_player_dict[venue][player]["vbaHs_economy_agg"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in ["spin_runs_b1", "spin_runs_b2", "spin_runs_b3"]
                    ]
                ) / (
                    sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in ["spin_balls_b1", "spin_balls_b2", "spin_balls_b3"]
                        ]
                    )
                    + 0.1
                )
                venue_player_dict[venue][player]["vbaHp_economy_agg"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in ["pace_runs_b1", "pace_runs_b2", "pace_runs_b3"]
                    ]
                ) / (
                    sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in ["pace_balls_b1", "pace_balls_b2", "pace_balls_b3"]
                        ]
                    )
                    + 0.1
                )
                venue_player_dict[venue][player]["vbaHs_4s_agg"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in ["vbaHp_4s_1", "vbaHp_4s_2", "vbaHp_4s_3"]
                    ]
                )
                venue_player_dict[venue][player]["vbaHp_4s_agg"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in ["vbaHs_4s_1", "vbaHs_4s_2", "vbaHs_4s_3"]
                    ]
                )
                venue_player_dict[venue][player]["vbaHr_4s_agg"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in ["vbaHp_4s_1", "vbaHp_4s_2", "vbaHp_4s_3"]
                    ]
                ) / (
                    sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in ["vbaHs_4s_1", "vbaHs_4s_2", "vbaHs_4s_3"]
                        ]
                    )
                    + 0.1
                )
                venue_player_dict[venue][player]["vbaHs_6s_agg"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in ["vbaHp_6s_1", "vbaHp_6s_2", "vbaHp_6s_3"]
                    ]
                )
                venue_player_dict[venue][player]["vbaHp_6s_agg"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in ["vbaHs_6s_1", "vbaHs_6s_2", "vbaHs_6s_3"]
                    ]
                )
                venue_player_dict[venue][player]["average"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in [
                            "spin_runs_b1",
                            "spin_runs_b2",
                            "spin_runs_b3",
                            "pace_runs_b1",
                            "pace_runs_b2",
                            "pace_runs_b3",
                        ]
                    ]
                ) / (
                    sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in [
                                "spin_balls_b1",
                                "spin_balls_b2",
                                "spin_balls_b3",
                                "pace_balls_b1",
                                "pace_balls_b2",
                                "pace_balls_b3",
                            ]
                        ]
                    )
                    + 0.1
                )
                venue_player_dict[venue][player]["average_4s"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in [
                            "vbaHs_4s_1",
                            "vbaHs_4s_2",
                            "vbaHs_4s_3",
                            "vbaHp_4s_1",
                            "vbaHp_4s_2",
                            "vbaHp_4s_3",
                        ]
                    ]
                ) / (
                    sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in [
                                "spin_balls_b1",
                                "spin_balls_b2",
                                "spin_balls_b3",
                                "pace_balls_b1",
                                "pace_balls_b2",
                                "pace_balls_b3",
                            ]
                        ]
                    )
                    + 0.1
                )
                venue_player_dict[venue][player][
                    "average_balls_involved"
                ] = venue_player_dict[venue][player]["balls_involved"] / (
                    venue_player_dict[venue][player]["balls_involved"] + 0.1
                )
                venue_player_dict[venue][player]["average_6s"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in [
                            "vbaHs_6s_1",
                            "vbaHs_6s_2",
                            "vbaHs_6s_3",
                            "vbaHp_6s_1",
                            "vbaHp_6s_2",
                            "vbaHp_6s_3",
                        ]
                    ]
                ) / (
                    sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in [
                                "spin_balls_b1",
                                "spin_balls_b2",
                                "spin_balls_b3",
                                "pace_balls_b1",
                                "pace_balls_b2",
                                "pace_balls_b3",
                            ]
                        ]
                    )
                    + 0.1
                )
                venue_player_dict[venue][player]["vbaHr_6s_agg"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in ["vbaHp_6s_1", "vbaHp_6s_2", "vbaHp_6s_3"]
                    ]
                ) / (
                    sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in ["vbaHs_6s_1", "vbaHs_6s_2", "vbaHs_6s_3"]
                        ]
                    )
                    + 0.1
                )
                venue_player_dict[venue][player]["vbaHs_dismissals_agg"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in [
                            "vbaHp_dismissals_1",
                            "vbaHp_dismissals_2",
                            "vbaHp_dismissals_3",
                        ]
                    ]
                )
                venue_player_dict[venue][player]["vbaHp_dismissals_agg"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in [
                            "vbaHs_dismissals_1",
                            "vbaHs_dismissals_2",
                            "vbaHs_dismissals_3",
                        ]
                    ]
                )
                venue_player_dict[venue][player]["vbaHr_dismissals_agg"] = sum(
                    [
                        venue_player_dict[venue][player][i]
                        for i in [
                            "vbaHp_dismissals_1",
                            "vbaHp_dismissals_2",
                            "vbaHp_dismissals_3",
                        ]
                    ]
                ) / (
                    sum(
                        [
                            venue_player_dict[venue][player][i]
                            for i in [
                                "vbaHs_dismissals_1",
                                "vbaHs_dismissals_2",
                                "vbaHs_dismissals_3",
                            ]
                        ]
                    )
                    + 0.1
                )
                venue_player_dict[venue][player]["innings"] += 1
                venue_player_dict[venue][player]["runouts"] += player_details.loc[
                    player, "run out"
                ]
                venue_player_dict[venue][player]["caught"] += (
                    player_details.loc[player, "caught"]
                    + player_details.loc[player, "caught and bowled"]
                )
                venue_player_dict[venue][player]["stumpings"] += player_details.loc[
                    player, "stumped"
                ]
                venue_player_dict[venue][player]["bowled"] += (
                    player_details.loc[player, "bowled"]
                    + player_details.loc[player, "lbw"]
                )
                venue_player_dict[venue][player]["total_wicks"] += (
                    player_details.loc[player, "run out"]
                    + player_details.loc[player, "caught"]
                    + player_details.loc[player, "caught and bowled"]
                    + player_details.loc[player, "stumped"]
                    + player_details.loc[player, "bowled"]
                    + player_details.loc[player, "lbw"]
                    + player_details.loc[player, "hit wicket"]
                )
                # venue_player_dict[venue][player]['dismissals_b1']+=player_details.loc[player,'vbaHs_dismissals_1']+player_details.loc[player,'vbaHp_dismissals_1']
                # venue_player_dict[venue][player]['dismissals_b2']+=player_details.loc[player,'vbaHs_dismissals_2']+player_details.loc[player,'vbaHp_dismissals_2']
                # venue_player_dict[venue][player]['dismissals_b3']+=player_details.loc[player,'vbaHs_dismissals_3']+player_details.loc[player,'vbaHp_dismissals_3']
                venue_player_dict[venue][player]["bowled_b1"] += player_details.loc[
                    player, "bowled_b1"
                ]
                venue_player_dict[venue][player]["bowled_b2"] += player_details.loc[
                    player, "bowled_b2"
                ]
                venue_player_dict[venue][player]["bowled_b3"] += player_details.loc[
                    player, "bowled_b3"
                ]
                venue_player_dict[venue][player]["madien_b1"] += player_details.loc[
                    player, "madien_b1"
                ]
                venue_player_dict[venue][player]["madien_b2"] += player_details.loc[
                    player, "madien_b2"
                ]
                venue_player_dict[venue][player]["madien_b3"] += player_details.loc[
                    player, "madien_b3"
                ]
                venue_player_dict[venue][player]["spin_runs_b1"] += player_details.loc[
                    player, "spin_runs_b1"
                ]
                venue_player_dict[venue][player]["spin_runs_b2"] += player_details.loc[
                    player, "spin_runs_b2"
                ]
                venue_player_dict[venue][player]["spin_runs_b3"] += player_details.loc[
                    player, "spin_runs_b3"
                ]
                venue_player_dict[venue][player]["vbaHs_4s_1"] += player_details.loc[
                    player, "spin_4s_b1"
                ]
                venue_player_dict[venue][player]["vbaHs_4s_2"] += player_details.loc[
                    player, "spin_4s_b2"
                ]
                venue_player_dict[venue][player]["vbaHs_4s_3"] += player_details.loc[
                    player, "spin_4s_b3"
                ]
                venue_player_dict[venue][player]["vbaHs_6s_1"] += player_details.loc[
                    player, "spin_6s_b1"
                ]
                venue_player_dict[venue][player]["vbaHs_6s_2"] += player_details.loc[
                    player, "spin_6s_b2"
                ]
                venue_player_dict[venue][player]["vbaHs_6s_3"] += player_details.loc[
                    player, "spin_6s_b3"
                ]
                venue_player_dict[venue][player][
                    "vbaHs_dismissals_1"
                ] += player_details.loc[player, "spin_wickets_b1"]
                venue_player_dict[venue][player][
                    "vbaHs_dismissals_2"
                ] += player_details.loc[player, "spin_wickets_b2"]
                venue_player_dict[venue][player][
                    "vbaHs_dismissals_3"
                ] += player_details.loc[player, "spin_wickets_b3"]
                venue_player_dict[venue][player]["spin_balls_b1"] += player_details.loc[
                    player, "spin_balls_b1"
                ]
                venue_player_dict[venue][player]["spin_balls_b2"] += player_details.loc[
                    player, "spin_balls_b2"
                ]
                venue_player_dict[venue][player]["spin_balls_b3"] += player_details.loc[
                    player, "spin_balls_b3"
                ]
                venue_player_dict[venue][player]["pace_runs_b1"] += player_details.loc[
                    player, "pace_runs_b1"
                ]
                venue_player_dict[venue][player]["pace_runs_b2"] += player_details.loc[
                    player, "pace_runs_b2"
                ]
                venue_player_dict[venue][player]["pace_runs_b3"] += player_details.loc[
                    player, "pace_runs_b3"
                ]
                venue_player_dict[venue][player][
                    "vbaHp_dismissals_1"
                ] += player_details.loc[player, "pace_wickets_b1"]
                venue_player_dict[venue][player][
                    "vbaHp_dismissals_2"
                ] += player_details.loc[player, "pace_wickets_b2"]
                venue_player_dict[venue][player][
                    "vbaHp_dismissals_3"
                ] += player_details.loc[player, "pace_wickets_b3"]
                venue_player_dict[venue][player]["pace_balls_b1"] += player_details.loc[
                    player, "pace_balls_b1"
                ]
                venue_player_dict[venue][player]["pace_balls_b2"] += player_details.loc[
                    player, "pace_balls_b2"
                ]
                venue_player_dict[venue][player]["pace_balls_b3"] += player_details.loc[
                    player, "pace_balls_b3"
                ]
                venue_player_dict[venue][player]["vbaHp_6s_1"] += player_details.loc[
                    player, "pace_6s_b1"
                ]
                venue_player_dict[venue][player]["vbaHp_6s_2"] += player_details.loc[
                    player, "pace_6s_b2"
                ]
                venue_player_dict[venue][player]["vbaHp_6s_3"] += player_details.loc[
                    player, "pace_6s_b2"
                ]
                venue_player_dict[venue][player]["vbaHp_4s_1"] += player_details.loc[
                    player, "pace_4s_b1"
                ]
                venue_player_dict[venue][player]["vbaHp_4s_2"] += player_details.loc[
                    player, "pace_4s_b2"
                ]
                venue_player_dict[venue][player]["vbaHp_4s_3"] += player_details.loc[
                    player, "pace_4s_b3"
                ]
                venue_player_dict[venue][player][
                    "balls_involved"
                ] += player_details.loc[player, "balls_involved"]
                venue_player_dict[venue][player]["balls"] += player_details.loc[
                    player, "balls"
                ]
                venue_player_df = pd.concat(
                    [venue_player_df, pd.DataFrame([venue_player_dict[venue][player]])]
                )
                # print(venue_player_dict[venue][player])

        final_df = pd.merge(
            match_batsman_details,
            venue_player_df,
            on=["date", "name", "team", "opposition_name"],
        )

        folder = os.path.join("data", "interim", format)
        os.makedirs(folder, exist_ok=True)
        file_name = "batsman.csv"
        final_df.to_csv(os.path.join(folder, file_name))

    loc_baseline = os.path.join(
        "data", "raw", "additional_data", "batter_data_odi.xlsx"
    )
    df3 = pd.read_excel(loc_baseline)

    k = -1
    for format in formats:
        k += 1
        batter_csv = os.path.join("data", "interim", format, "batsman.csv")
        df1 = pd.read_csv(batter_csv)
        df1 = df1.fillna(0)
        for i in list(df1):
            if "dismissal_" in i:
                df1[i.replace("dismissal", "dismissals")] = df1[i]
                df1.drop(i, axis=1, inplace=True)
        df1.replace([np.inf, -np.inf], 0, inplace=True)
        simple_batsman = os.path.join(
            "data", "interim", format, "simple_match_batsman_details_1_withids.csv"
        )
        df2 = pd.read_csv(simple_batsman)
        for i in list(df1):
            if i[-2:] == "_x" or i[-2:] == "_y":
                df1[i[:-2]] = df1[i]
                df1 = df1.drop(i, axis=1)
        df4 = pd.DataFrame()
        for i in list(df1):
            if (
                i not in list(df2)
                and "ball" not in i
                and i not in list(df3)
                and "dismissal" not in i
            ):
                df1 = df1.drop(i, axis=1)
            elif i in list(df2):
                df1[i] = df2[i]
            elif "ball" in i:
                df4[i] = df1[i]
                df1 = df1.drop(i, axis=1)
        lst1 = [i for i in list(df2) if i not in list(df1)]
        for i in lst1:
            df1[i] = df2[i]
        checklist = [i[:-1] for i in list(df1) if "1" in i or "2" in i or "3" in i]

        checklist = list(pd.Series(checklist).unique())
        for j in checklist:
            if j[4] == "s":
                df1["W" + j[:-1]] = (
                    df1[j + "1"] * df4["hist_spin_balls_b1"]
                    + df1[j + "2"] * df4["hist_spin_balls_b2"]
                    + df1[j + "3"] * df4["hist_spin_balls_b3"]
                ) / (
                    df4["hist_spin_balls_b1"]
                    + df4["hist_spin_balls_b2"]
                    + df4["hist_spin_balls_b3"]
                )
                df1["W" + j[:4] + j[5:-1]] = (
                    df1[j + "1"] * df4["hist_spin_balls_b1"]
                    + df1[j + "2"] * df4["hist_spin_balls_b2"]
                    + df1[j + "3"] * df4["hist_spin_balls_b3"]
                    + df1[j + "1"] * df4["hist_pace_balls_b1"]
                    + df1[j + "2"] * df4["hist_pace_balls_b2"]
                    + df1[j + "3"] * df4["hist_pace_balls_b3"]
                ) / (
                    df4["hist_spin_balls_b1"]
                    + df4["hist_spin_balls_b2"]
                    + df4["hist_spin_balls_b3"]
                    + df4["hist_pace_balls_b1"]
                    + df4["hist_pace_balls_b2"]
                    + df4["hist_pace_balls_b3"]
                )

            if j[4] == "p":
                df1["W" + j[:-1]] = (
                    df1[j + "1"] * df4["hist_pace_balls_b1"]
                    + df1[j + "2"] * df4["hist_pace_balls_b2"]
                    + df1[j + "3"] * df4["hist_pace_balls_b3"]
                ) / (
                    df4["hist_pace_balls_b1"]
                    + df4["hist_pace_balls_b2"]
                    + df4["hist_pace_balls_b3"]
                )

            if j[4] == "r":
                df1["W" + j[:-1]] = (
                    df1[j + "1"]
                    * (df4["hist_spin_balls_b1"] + df4["hist_pace_balls_b1"])
                    + df1[j + "2"]
                    * (df4["hist_pace_balls_b2"] + df4["hist_spin_balls_b2"])
                    + df1[j + "3"]
                    * (df4["hist_spin_balls_b3"] + df4["hist_pace_balls_b3"])
                ) / (
                    df4["hist_spin_balls_b1"]
                    + df4["hist_spin_balls_b2"]
                    + df4["hist_spin_balls_b3"]
                    + df4["hist_pace_balls_b1"]
                    + df4["hist_pace_balls_b2"]
                    + df4["hist_pace_balls_b3"]
                )

        df1 = df1.fillna(0)
        df1.replace([np.inf, -np.inf], 0, inplace=True)
        df1["diffExP_venue"] = df1["consistency"] - df1["venue"]
        df1["diffExP_form"] = df1["consistency"] - df1["form"]
        df1["diffExP_opposition"] = df1["consistency"] - df1["opposition"]
        v = 20 * df1["previous_centuries"] + 5 * df1["previous_fifties"]
        w = v * 0.3 + 0.7 * df1["previous_average"]
        df1["career_score"] = w * df1["innings_played"]
        df1["recent_score"] = df1["WfbaHp_economy"] + df1["WfbaHs_economy"]
        df1["combined_score"] = 0.65 * df1["career_score"] + 0.35 * df1["recent_score"]

        folder = os.path.join("data", "processed", format)
        os.makedirs(folder, exist_ok=True)
        file_name = "batter.csv"
        df1.to_csv(os.path.join(folder, file_name))

    return


import argparse


def main():
    parser = argparse.ArgumentParser(description="Process some inputs.")

    parser.add_argument("name", type=str, help="type of processing")
    args = parser.parse_args()

    if args.name == "male_t20":
        location = os.path.join(
            "data", "interim", "sorted_acc_to_date_and_format_male.csv"
        )
        formats = ["T20"]
        matchid_mapping = [10000]
        func("male", location, formats, matchid_mapping)
    elif args.name == "male_others":
        location = os.path.join(
            "data", "interim", "sorted_acc_to_date_and_format_male.csv"
        )
        formats = ["ODI", "MDM", "ODM", "Test", "IT20"]
        matchid_mapping = [20000, 30000, 40000, 50000, 60000]
        func("male", location, formats, matchid_mapping)
    elif args.name == "female":
        location = os.path.join(
            "data", "interim", "sorted_acc_to_date_and_format_female.csv"
        )
        formats = ["WT20", "WODI", "WODM", "WTest", "WIT20"]
        matchid_mapping = [70000, 75000, 80000, 85000, 90000]
        func("female", location, formats, matchid_mapping)


if __name__ == "__main__":
    main()
