import pandas as pd
import yaml
import os
import time
import numpy as np
import math
import warnings

warnings.filterwarnings("ignore")  # Hide messy Numpy warnings


def extract_details(filename):
    dict = yaml.load(open(filename), yaml.Loader)

    match_details = {}
    try:
        match_details["match_id"] = dict["info"]["match_type_number"]
    except:
        match_details["match_id"] = ""
    try:
        match_details["venue"] = dict["info"]["venue"]
    except:
        match_details["venue"] = ""
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
        match_details["winner"] = "no result"
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

    # print(match_details)

    wickets = {}
    wickets["caught"] = 0
    wickets["run_out"] = 0
    wickets["stumped"] = 0
    wickets["wickets"] = 0

    player_details = pd.DataFrame(
        columns=[
            "date",
            "team",
            "runs",
            "1s",
            "2s",
            "4s",
            "6s",
            "balls",
            "dots",
            "maidens",
            "wickets",
            "caught",
            "bowledlbw",
            "bowledlbw_1",
            "bowledlbw_2",
            "bowledlbw_3",
            "wickets_1",
            "wickets_2",
            "wickets_3",
            "maidens_1",
            "maidens_2",
            "maidens_3",
            "runs_1",
            "runs_2",
            "runs_3",
            "balls_1",
            "balls_2",
            "balls_3",
            "extras",
            "opposition",
            "bowl_first",
            "toss_outcome",
            "venue",
            "bat_innings",
            "outcome",
            "overs",
        ]
    )

    innings1 = dict["innings"][0]["1st innings"]["deliveries"]
    runs_this_over = 0
    for ball in innings1:
        for delivery in ball:

            if "wicket" in ball[delivery]:
                wickets["wickets"] += 1
                if "kind" in ball[delivery]["wicket"]:
                    if "caught" in ball[delivery]["wicket"]["kind"]:
                        wickets["caught"] += 1
                    if ball[delivery]["wicket"]["kind"] == "run out":
                        wickets["run_out"] += 1
                    if ball[delivery]["wicket"]["kind"] == "stumped":
                        wickets["stumped"] += 1
                else:
                    for x in ball[delivery]["wicket"]:
                        if "caught" in x["kind"]:
                            wickets["caught"] += 1
                        if x["kind"] == "run out":
                            wickets["run_out"] += 1
                        if x["kind"] == "stumped":
                            wickets["stumped"] += 1

            try:
                player_details.index.get_loc(ball[delivery]["bowler"])
            except:
                player_details.loc[ball[delivery]["bowler"], "bowl_first"] = 1
                player_details.loc[ball[delivery]["bowler"], "toss_outcome"] = toss
                player_details.loc[ball[delivery]["bowler"], "runs"] = 0
                player_details.loc[ball[delivery]["bowler"], "1s"] = 0
                player_details.loc[ball[delivery]["bowler"], "2s"] = 0
                player_details.loc[ball[delivery]["bowler"], "4s"] = 0
                player_details.loc[ball[delivery]["bowler"], "6s"] = 0
                player_details.loc[ball[delivery]["bowler"], "balls"] = 0
                player_details.loc[ball[delivery]["bowler"], "dots"] = 0
                player_details.loc[ball[delivery]["bowler"], "maidens"] = 0
                player_details.loc[ball[delivery]["bowler"], "wickets"] = 0
                player_details.loc[ball[delivery]["bowler"], "caught"] = 0
                player_details.loc[ball[delivery]["bowler"], "bowledlbw"] = 0
                player_details.loc[ball[delivery]["bowler"], "extras"] = 0
                player_details.loc[ball[delivery]["bowler"], "overs"] = 0

                player_details.loc[ball[delivery]["bowler"], "bowledlbw_1"] = 0
                player_details.loc[ball[delivery]["bowler"], "wickets_1"] = 0
                player_details.loc[ball[delivery]["bowler"], "maidens_1"] = 0
                player_details.loc[ball[delivery]["bowler"], "bowledlbw_2"] = 0
                player_details.loc[ball[delivery]["bowler"], "wickets_2"] = 0
                player_details.loc[ball[delivery]["bowler"], "maidens_2"] = 0
                player_details.loc[ball[delivery]["bowler"], "bowledlbw_3"] = 0
                player_details.loc[ball[delivery]["bowler"], "wickets_3"] = 0
                player_details.loc[ball[delivery]["bowler"], "maidens_3"] = 0
                player_details.loc[ball[delivery]["bowler"], "runs_1"] = 0
                player_details.loc[ball[delivery]["bowler"], "balls_1"] = 0
                player_details.loc[ball[delivery]["bowler"], "runs_2"] = 0
                player_details.loc[ball[delivery]["bowler"], "balls_2"] = 0
                player_details.loc[ball[delivery]["bowler"], "runs_3"] = 0
                player_details.loc[ball[delivery]["bowler"], "balls_3"] = 0

            ball_no, over_no = math.modf(delivery)
            if abs(ball_no - 0.1) < 1e-6:
                player_details.loc[ball[delivery]["bowler"], "overs"] += 1
                runs_this_over = 0
            runs_this_over += ball[delivery]["runs"]["total"]
            if abs(ball_no - 0.6) < 1e-6:
                if runs_this_over == 0:
                    player_details.loc[ball[delivery]["bowler"], "maidens"] += 1
                    if over_no < 10:
                        player_details.loc[ball[delivery]["bowler"], "maidens_1"] += 1
                    elif over_no < 40:
                        player_details.loc[ball[delivery]["bowler"], "maidens_2"] += 1
                    else:
                        player_details.loc[ball[delivery]["bowler"], "maidens_3"] += 1

            player_details.loc[ball[delivery]["bowler"], "date"] = match_details["date"]
            player_details.loc[ball[delivery]["bowler"], "team"] = match_details[
                "bat_first"
            ][1]
            player_details.loc[ball[delivery]["bowler"], "opposition"] = match_details[
                "bat_first"
            ][0]
            player_details.loc[ball[delivery]["bowler"], "bat_innings"] = 1
            player_details.loc[ball[delivery]["bowler"], "venue"] = match_details[
                "venue"
            ]

            if (
                match_details["winner"]
                == player_details.loc[ball[delivery]["bowler"], "team"]
            ):
                player_details.loc[ball[delivery]["bowler"], "outcome"] = 1
            else:
                player_details.loc[ball[delivery]["bowler"], "outcome"] = 0

            if "wicket" in ball[delivery]:
                player_details.loc[ball[delivery]["bowler"], "wickets"] += 1
                if over_no < 10:
                    player_details.loc[ball[delivery]["bowler"], "wickets_1"] += 1
                elif over_no < 40:
                    player_details.loc[ball[delivery]["bowler"], "wickets_2"] += 1
                else:
                    player_details.loc[ball[delivery]["bowler"], "wickets_3"] += 1
                if "kind" in ball[delivery]["wicket"]:
                    if "caught" in ball[delivery]["wicket"]["kind"]:
                        player_details.loc[ball[delivery]["bowler"], "caught"] += 1
                    if (
                        ball[delivery]["wicket"]["kind"] == "bowled"
                        or ball[delivery]["wicket"]["kind"] == "lbw"
                    ):
                        player_details.loc[ball[delivery]["bowler"], "bowledlbw"] += 1
                        if over_no < 10:
                            player_details.loc[
                                ball[delivery]["bowler"], "bowledlbw_1"
                            ] += 1
                        elif over_no < 40:
                            player_details.loc[
                                ball[delivery]["bowler"], "bowledlbw_2"
                            ] += 1
                        else:
                            player_details.loc[
                                ball[delivery]["bowler"], "bowledlbw_3"
                            ] += 1
                else:
                    for x in ball[delivery]["wicket"]:
                        if "caught" in x["kind"]:
                            player_details.loc[ball[delivery]["bowler"], "caught"] += 1
                        if x["kind"] == "bowled" or x["kind"] == "lbw":
                            player_details.loc[
                                ball[delivery]["bowler"], "bowledlbw"
                            ] += 1
                            if over_no < 10:
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw_1"
                                ] += 1
                            elif over_no < 40:
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw_2"
                                ] += 1
                            else:
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw_3"
                                ] += 1

            if "extras" in ball[delivery]:
                player_details.loc[ball[delivery]["bowler"], "extras"] += ball[
                    delivery
                ]["runs"]["extras"]

            if over_no < 10:
                player_details.loc[ball[delivery]["bowler"], "balls_1"] += 1
                player_details.loc[ball[delivery]["bowler"], "runs_1"] += ball[
                    delivery
                ]["runs"]["total"]
            elif over_no < 40:
                player_details.loc[ball[delivery]["bowler"], "balls_2"] += 1
                player_details.loc[ball[delivery]["bowler"], "runs_2"] += ball[
                    delivery
                ]["runs"]["total"]
            else:
                player_details.loc[ball[delivery]["bowler"], "balls_3"] += 1
                player_details.loc[ball[delivery]["bowler"], "runs_3"] += ball[
                    delivery
                ]["runs"]["total"]

            player_details.loc[ball[delivery]["bowler"], "runs"] += ball[delivery][
                "runs"
            ]["total"]
            player_details.loc[ball[delivery]["bowler"], "dots"] += (
                player_details.loc[ball[delivery]["bowler"], "runs"] == 0
            )
            player_details.loc[ball[delivery]["bowler"], "1s"] += (
                player_details.loc[ball[delivery]["bowler"], "runs"] == 1
            )
            player_details.loc[ball[delivery]["bowler"], "2s"] += (
                player_details.loc[ball[delivery]["bowler"], "runs"] == 2
            )
            player_details.loc[ball[delivery]["bowler"], "4s"] += (
                player_details.loc[ball[delivery]["bowler"], "runs"] == 4
            )
            player_details.loc[ball[delivery]["bowler"], "6s"] += (
                player_details.loc[ball[delivery]["bowler"], "runs"] == 6
            )
            player_details.loc[ball[delivery]["bowler"], "balls"] += 1

    try:
        innings2 = dict["innings"][1]["2nd innings"]["deliveries"]
    except:
        flag = True
    else:
        for ball in innings2:
            for delivery in ball:

                if "wicket" in ball[delivery]:
                    wickets["wickets"] += 1
                    if "kind" in ball[delivery]["wicket"]:
                        if "caught" in ball[delivery]["wicket"]["kind"]:
                            wickets["caught"] += 1
                        if ball[delivery]["wicket"]["kind"] == "run out":
                            wickets["run_out"] += 1
                        if ball[delivery]["wicket"]["kind"] == "stumped":
                            wickets["stumped"] += 1
                    else:
                        for x in ball[delivery]["wicket"]:
                            if "caught" in x["kind"]:
                                wickets["caught"] += 1
                            if x["kind"] == "run out":
                                wickets["run_out"] += 1
                            if x["kind"] == "stumped":
                                wickets["stumped"] += 1

                try:
                    player_details.index.get_loc(ball[delivery]["bowler"])
                except:
                    player_details.loc[ball[delivery]["bowler"], "bowl_first"] = 0
                    player_details.loc[ball[delivery]["bowler"], "toss_outcome"] = (
                        1 - toss
                    )
                    player_details.loc[ball[delivery]["bowler"], "runs"] = 0
                    player_details.loc[ball[delivery]["bowler"], "1s"] = 0
                    player_details.loc[ball[delivery]["bowler"], "2s"] = 0
                    player_details.loc[ball[delivery]["bowler"], "4s"] = 0
                    player_details.loc[ball[delivery]["bowler"], "6s"] = 0
                    player_details.loc[ball[delivery]["bowler"], "balls"] = 0
                    player_details.loc[ball[delivery]["bowler"], "dots"] = 0
                    player_details.loc[ball[delivery]["bowler"], "maidens"] = 0
                    player_details.loc[ball[delivery]["bowler"], "wickets"] = 0
                    player_details.loc[ball[delivery]["bowler"], "caught"] = 0
                    player_details.loc[ball[delivery]["bowler"], "bowledlbw"] = 0
                    player_details.loc[ball[delivery]["bowler"], "extras"] = 0
                    player_details.loc[ball[delivery]["bowler"], "overs"] = 0

                    player_details.loc[ball[delivery]["bowler"], "bowledlbw_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "wickets_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "maidens_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "bowledlbw_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "wickets_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "maidens_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "bowledlbw_3"] = 0
                    player_details.loc[ball[delivery]["bowler"], "wickets_3"] = 0
                    player_details.loc[ball[delivery]["bowler"], "maidens_3"] = 0
                    player_details.loc[ball[delivery]["bowler"], "runs_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "balls_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "runs_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "balls_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "runs_3"] = 0
                    player_details.loc[ball[delivery]["bowler"], "balls_3"] = 0

                ball_no, over_no = math.modf(delivery)
                if abs(ball_no - 0.1) < 1e-6:
                    player_details.loc[ball[delivery]["bowler"], "overs"] += 1
                    runs_this_over = 0
                runs_this_over += ball[delivery]["runs"]["total"]
                if abs(ball_no - 0.6) < 1e-6:
                    if runs_this_over == 0:
                        player_details.loc[ball[delivery]["bowler"], "maidens"] += 1
                        if over_no < 10:
                            player_details.loc[
                                ball[delivery]["bowler"], "maidens_1"
                            ] += 1
                        elif over_no < 40:
                            player_details.loc[
                                ball[delivery]["bowler"], "maidens_2"
                            ] += 1
                        else:
                            player_details.loc[
                                ball[delivery]["bowler"], "maidens_3"
                            ] += 1

                player_details.loc[ball[delivery]["bowler"], "date"] = match_details[
                    "date"
                ]
                player_details.loc[ball[delivery]["bowler"], "team"] = match_details[
                    "bat_first"
                ][0]
                player_details.loc[
                    ball[delivery]["bowler"], "opposition"
                ] = match_details["bat_first"][1]
                player_details.loc[ball[delivery]["bowler"], "bat_innings"] = 2
                player_details.loc[ball[delivery]["bowler"], "venue"] = match_details[
                    "venue"
                ]

                if (
                    match_details["winner"]
                    == player_details.loc[ball[delivery]["bowler"], "team"]
                ):
                    player_details.loc[ball[delivery]["bowler"], "outcome"] = 1
                else:
                    player_details.loc[ball[delivery]["bowler"], "outcome"] = 0

                if "wicket" in ball[delivery]:
                    player_details.loc[ball[delivery]["bowler"], "wickets"] += 1
                    if over_no < 10:
                        player_details.loc[ball[delivery]["bowler"], "wickets_1"] += 1
                    elif over_no < 40:
                        player_details.loc[ball[delivery]["bowler"], "wickets_2"] += 1
                    else:
                        player_details.loc[ball[delivery]["bowler"], "wickets_3"] += 1
                    if "kind" in ball[delivery]["wicket"]:
                        if "caught" in ball[delivery]["wicket"]["kind"]:
                            player_details.loc[ball[delivery]["bowler"], "caught"] += 1
                        if (
                            ball[delivery]["wicket"]["kind"] == "bowled"
                            or ball[delivery]["wicket"]["kind"] == "lbw"
                        ):
                            player_details.loc[
                                ball[delivery]["bowler"], "bowledlbw"
                            ] += 1
                            if over_no < 10:
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw_1"
                                ] += 1
                            elif over_no < 40:
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw_2"
                                ] += 1
                            else:
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw_3"
                                ] += 1
                    else:
                        for x in ball[delivery]["wicket"]:
                            if "caught" in x["kind"]:
                                player_details.loc[
                                    ball[delivery]["bowler"], "caught"
                                ] += 1
                            if x["kind"] == "bowled" or x["kind"] == "lbw":
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw"
                                ] += 1
                                if over_no < 10:
                                    player_details.loc[
                                        ball[delivery]["bowler"], "bowledlbw_1"
                                    ] += 1
                                elif over_no < 40:
                                    player_details.loc[
                                        ball[delivery]["bowler"], "bowledlbw_2"
                                    ] += 1
                                else:
                                    player_details.loc[
                                        ball[delivery]["bowler"], "bowledlbw_3"
                                    ] += 1

                if "extras" in ball[delivery]:
                    player_details.loc[ball[delivery]["bowler"], "extras"] += ball[
                        delivery
                    ]["runs"]["extras"]

                if over_no < 10:
                    player_details.loc[ball[delivery]["bowler"], "balls_1"] += 1
                    player_details.loc[ball[delivery]["bowler"], "runs_1"] += ball[
                        delivery
                    ]["runs"]["total"]
                elif over_no < 40:
                    player_details.loc[ball[delivery]["bowler"], "balls_2"] += 1
                    player_details.loc[ball[delivery]["bowler"], "runs_2"] += ball[
                        delivery
                    ]["runs"]["total"]
                else:
                    player_details.loc[ball[delivery]["bowler"], "balls_3"] += 1
                    player_details.loc[ball[delivery]["bowler"], "runs_3"] += ball[
                        delivery
                    ]["runs"]["total"]

                player_details.loc[ball[delivery]["bowler"], "runs"] += ball[delivery][
                    "runs"
                ]["total"]
                player_details.loc[ball[delivery]["bowler"], "dots"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 0
                )
                player_details.loc[ball[delivery]["bowler"], "1s"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 1
                )
                player_details.loc[ball[delivery]["bowler"], "2s"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 2
                )
                player_details.loc[ball[delivery]["bowler"], "4s"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 4
                )
                player_details.loc[ball[delivery]["bowler"], "6s"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 6
                )
                player_details.loc[ball[delivery]["bowler"], "balls"] += 1

    try:
        innings3 = dict["innings"][2]["3rd innings"]["deliveries"]
    except:
        flag = True
    else:
        runs_this_over = 0
        for ball in innings3:
            for delivery in ball:

                if "wicket" in ball[delivery]:
                    wickets["wickets"] += 1
                    if "kind" in ball[delivery]["wicket"]:
                        if "caught" in ball[delivery]["wicket"]["kind"]:
                            wickets["caught"] += 1
                        if ball[delivery]["wicket"]["kind"] == "run out":
                            wickets["run_out"] += 1
                        if ball[delivery]["wicket"]["kind"] == "stumped":
                            wickets["stumped"] += 1
                    else:
                        for x in ball[delivery]["wicket"]:
                            if "caught" in x["kind"]:
                                wickets["caught"] += 1
                            if x["kind"] == "run out":
                                wickets["run_out"] += 1
                            if x["kind"] == "stumped":
                                wickets["stumped"] += 1

                try:
                    player_details.index.get_loc(ball[delivery]["bowler"])
                except:
                    player_details.loc[ball[delivery]["bowler"], "bowl_first"] = 1
                    player_details.loc[ball[delivery]["bowler"], "toss_outcome"] = toss
                    player_details.loc[ball[delivery]["bowler"], "runs"] = 0
                    player_details.loc[ball[delivery]["bowler"], "1s"] = 0
                    player_details.loc[ball[delivery]["bowler"], "2s"] = 0
                    player_details.loc[ball[delivery]["bowler"], "4s"] = 0
                    player_details.loc[ball[delivery]["bowler"], "6s"] = 0
                    player_details.loc[ball[delivery]["bowler"], "balls"] = 0
                    player_details.loc[ball[delivery]["bowler"], "dots"] = 0
                    player_details.loc[ball[delivery]["bowler"], "maidens"] = 0
                    player_details.loc[ball[delivery]["bowler"], "wickets"] = 0
                    player_details.loc[ball[delivery]["bowler"], "caught"] = 0
                    player_details.loc[ball[delivery]["bowler"], "bowledlbw"] = 0
                    player_details.loc[ball[delivery]["bowler"], "extras"] = 0
                    player_details.loc[ball[delivery]["bowler"], "overs"] = 0

                    player_details.loc[ball[delivery]["bowler"], "bowledlbw_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "wickets_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "maidens_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "bowledlbw_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "wickets_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "maidens_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "bowledlbw_3"] = 0
                    player_details.loc[ball[delivery]["bowler"], "wickets_3"] = 0
                    player_details.loc[ball[delivery]["bowler"], "maidens_3"] = 0
                    player_details.loc[ball[delivery]["bowler"], "runs_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "balls_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "runs_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "balls_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "runs_3"] = 0
                    player_details.loc[ball[delivery]["bowler"], "balls_3"] = 0

                ball_no, over_no = math.modf(delivery)
                if abs(ball_no - 0.1) < 1e-6:
                    player_details.loc[ball[delivery]["bowler"], "overs"] += 1
                    runs_this_over = 0
                runs_this_over += ball[delivery]["runs"]["total"]
                if abs(ball_no - 0.6) < 1e-6:
                    if runs_this_over == 0:
                        player_details.loc[ball[delivery]["bowler"], "maidens"] += 1
                        if over_no < 10:
                            player_details.loc[
                                ball[delivery]["bowler"], "maidens_1"
                            ] += 1
                        elif over_no < 40:
                            player_details.loc[
                                ball[delivery]["bowler"], "maidens_2"
                            ] += 1
                        else:
                            player_details.loc[
                                ball[delivery]["bowler"], "maidens_3"
                            ] += 1

                player_details.loc[ball[delivery]["bowler"], "date"] = match_details[
                    "date"
                ]
                player_details.loc[ball[delivery]["bowler"], "team"] = match_details[
                    "bat_first"
                ][1]
                player_details.loc[
                    ball[delivery]["bowler"], "opposition"
                ] = match_details["bat_first"][0]
                player_details.loc[ball[delivery]["bowler"], "bat_innings"] = 1
                player_details.loc[ball[delivery]["bowler"], "venue"] = match_details[
                    "venue"
                ]

                if (
                    match_details["winner"]
                    == player_details.loc[ball[delivery]["bowler"], "team"]
                ):
                    player_details.loc[ball[delivery]["bowler"], "outcome"] = 1
                else:
                    player_details.loc[ball[delivery]["bowler"], "outcome"] = 0

                if "wicket" in ball[delivery]:
                    player_details.loc[ball[delivery]["bowler"], "wickets"] += 1
                    if over_no < 10:
                        player_details.loc[ball[delivery]["bowler"], "wickets_1"] += 1
                    elif over_no < 40:
                        player_details.loc[ball[delivery]["bowler"], "wickets_2"] += 1
                    else:
                        player_details.loc[ball[delivery]["bowler"], "wickets_3"] += 1
                    if "kind" in ball[delivery]["wicket"]:
                        if "caught" in ball[delivery]["wicket"]["kind"]:
                            player_details.loc[ball[delivery]["bowler"], "caught"] += 1
                        if (
                            ball[delivery]["wicket"]["kind"] == "bowled"
                            or ball[delivery]["wicket"]["kind"] == "lbw"
                        ):
                            player_details.loc[
                                ball[delivery]["bowler"], "bowledlbw"
                            ] += 1
                            if over_no < 10:
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw_1"
                                ] += 1
                            elif over_no < 40:
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw_2"
                                ] += 1
                            else:
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw_3"
                                ] += 1
                    else:
                        for x in ball[delivery]["wicket"]:
                            if "caught" in x["kind"]:
                                player_details.loc[
                                    ball[delivery]["bowler"], "caught"
                                ] += 1
                            if x["kind"] == "bowled" or x["kind"] == "lbw":
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw"
                                ] += 1
                                if over_no < 10:
                                    player_details.loc[
                                        ball[delivery]["bowler"], "bowledlbw_1"
                                    ] += 1
                                elif over_no < 40:
                                    player_details.loc[
                                        ball[delivery]["bowler"], "bowledlbw_2"
                                    ] += 1
                                else:
                                    player_details.loc[
                                        ball[delivery]["bowler"], "bowledlbw_3"
                                    ] += 1

                if "extras" in ball[delivery]:
                    player_details.loc[ball[delivery]["bowler"], "extras"] += ball[
                        delivery
                    ]["runs"]["extras"]

                if over_no < 10:
                    player_details.loc[ball[delivery]["bowler"], "balls_1"] += 1
                    player_details.loc[ball[delivery]["bowler"], "runs_1"] += ball[
                        delivery
                    ]["runs"]["total"]
                elif over_no < 40:
                    player_details.loc[ball[delivery]["bowler"], "balls_2"] += 1
                    player_details.loc[ball[delivery]["bowler"], "runs_2"] += ball[
                        delivery
                    ]["runs"]["total"]
                else:
                    player_details.loc[ball[delivery]["bowler"], "balls_3"] += 1
                    player_details.loc[ball[delivery]["bowler"], "runs_3"] += ball[
                        delivery
                    ]["runs"]["total"]

                player_details.loc[ball[delivery]["bowler"], "runs"] += ball[delivery][
                    "runs"
                ]["total"]
                player_details.loc[ball[delivery]["bowler"], "dots"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 0
                )
                player_details.loc[ball[delivery]["bowler"], "1s"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 1
                )
                player_details.loc[ball[delivery]["bowler"], "2s"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 2
                )
                player_details.loc[ball[delivery]["bowler"], "4s"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 4
                )
                player_details.loc[ball[delivery]["bowler"], "6s"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 6
                )
                player_details.loc[ball[delivery]["bowler"], "balls"] += 1

    try:
        innings4 = dict["innings"][3]["4th innings"]["deliveries"]
    except:
        flag = True
    else:
        for ball in innings4:
            for delivery in ball:

                if "wicket" in ball[delivery]:
                    wickets["wickets"] += 1
                    if "kind" in ball[delivery]["wicket"]:
                        if "caught" in ball[delivery]["wicket"]["kind"]:
                            wickets["caught"] += 1
                        if ball[delivery]["wicket"]["kind"] == "run out":
                            wickets["run_out"] += 1
                        if ball[delivery]["wicket"]["kind"] == "stumped":
                            wickets["stumped"] += 1
                    else:
                        for x in ball[delivery]["wicket"]:
                            if "caught" in x["kind"]:
                                wickets["caught"] += 1
                            if x["kind"] == "run out":
                                wickets["run_out"] += 1
                            if x["kind"] == "stumped":
                                wickets["stumped"] += 1

                try:
                    player_details.index.get_loc(ball[delivery]["bowler"])
                except:
                    player_details.loc[ball[delivery]["bowler"], "bowl_first"] = 0
                    player_details.loc[ball[delivery]["bowler"], "toss_outcome"] = (
                        1 - toss
                    )
                    player_details.loc[ball[delivery]["bowler"], "runs"] = 0
                    player_details.loc[ball[delivery]["bowler"], "1s"] = 0
                    player_details.loc[ball[delivery]["bowler"], "2s"] = 0
                    player_details.loc[ball[delivery]["bowler"], "4s"] = 0
                    player_details.loc[ball[delivery]["bowler"], "6s"] = 0
                    player_details.loc[ball[delivery]["bowler"], "balls"] = 0
                    player_details.loc[ball[delivery]["bowler"], "dots"] = 0
                    player_details.loc[ball[delivery]["bowler"], "maidens"] = 0
                    player_details.loc[ball[delivery]["bowler"], "wickets"] = 0
                    player_details.loc[ball[delivery]["bowler"], "caught"] = 0
                    player_details.loc[ball[delivery]["bowler"], "bowledlbw"] = 0
                    player_details.loc[ball[delivery]["bowler"], "extras"] = 0
                    player_details.loc[ball[delivery]["bowler"], "overs"] = 0

                    player_details.loc[ball[delivery]["bowler"], "bowledlbw_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "wickets_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "maidens_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "bowledlbw_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "wickets_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "maidens_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "bowledlbw_3"] = 0
                    player_details.loc[ball[delivery]["bowler"], "wickets_3"] = 0
                    player_details.loc[ball[delivery]["bowler"], "maidens_3"] = 0
                    player_details.loc[ball[delivery]["bowler"], "runs_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "balls_1"] = 0
                    player_details.loc[ball[delivery]["bowler"], "runs_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "balls_2"] = 0
                    player_details.loc[ball[delivery]["bowler"], "runs_3"] = 0
                    player_details.loc[ball[delivery]["bowler"], "balls_3"] = 0

                ball_no, over_no = math.modf(delivery)
                if abs(ball_no - 0.1) < 1e-6:
                    player_details.loc[ball[delivery]["bowler"], "overs"] += 1
                    runs_this_over = 0
                runs_this_over += ball[delivery]["runs"]["total"]
                if abs(ball_no - 0.6) < 1e-6:
                    if runs_this_over == 0:
                        player_details.loc[ball[delivery]["bowler"], "maidens"] += 1
                        if over_no < 10:
                            player_details.loc[
                                ball[delivery]["bowler"], "maidens_1"
                            ] += 1
                        elif over_no < 40:
                            player_details.loc[
                                ball[delivery]["bowler"], "maidens_2"
                            ] += 1
                        else:
                            player_details.loc[
                                ball[delivery]["bowler"], "maidens_3"
                            ] += 1

                player_details.loc[ball[delivery]["bowler"], "date"] = match_details[
                    "date"
                ]
                player_details.loc[ball[delivery]["bowler"], "team"] = match_details[
                    "bat_first"
                ][0]
                player_details.loc[
                    ball[delivery]["bowler"], "opposition"
                ] = match_details["bat_first"][1]
                player_details.loc[ball[delivery]["bowler"], "bat_innings"] = 2
                player_details.loc[ball[delivery]["bowler"], "venue"] = match_details[
                    "venue"
                ]

                if (
                    match_details["winner"]
                    == player_details.loc[ball[delivery]["bowler"], "team"]
                ):
                    player_details.loc[ball[delivery]["bowler"], "outcome"] = 1
                else:
                    player_details.loc[ball[delivery]["bowler"], "outcome"] = 0

                if "wicket" in ball[delivery]:
                    player_details.loc[ball[delivery]["bowler"], "wickets"] += 1
                    if over_no < 10:
                        player_details.loc[ball[delivery]["bowler"], "wickets_1"] += 1
                    elif over_no < 40:
                        player_details.loc[ball[delivery]["bowler"], "wickets_2"] += 1
                    else:
                        player_details.loc[ball[delivery]["bowler"], "wickets_3"] += 1
                    if "kind" in ball[delivery]["wicket"]:
                        if "caught" in ball[delivery]["wicket"]["kind"]:
                            player_details.loc[ball[delivery]["bowler"], "caught"] += 1
                        if (
                            ball[delivery]["wicket"]["kind"] == "bowled"
                            or ball[delivery]["wicket"]["kind"] == "lbw"
                        ):
                            player_details.loc[
                                ball[delivery]["bowler"], "bowledlbw"
                            ] += 1
                            if over_no < 10:
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw_1"
                                ] += 1
                            elif over_no < 40:
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw_2"
                                ] += 1
                            else:
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw_3"
                                ] += 1
                    else:
                        for x in ball[delivery]["wicket"]:
                            if "caught" in x["kind"]:
                                player_details.loc[
                                    ball[delivery]["bowler"], "caught"
                                ] += 1
                            if x["kind"] == "bowled" or x["kind"] == "lbw":
                                player_details.loc[
                                    ball[delivery]["bowler"], "bowledlbw"
                                ] += 1
                                if over_no < 10:
                                    player_details.loc[
                                        ball[delivery]["bowler"], "bowledlbw_1"
                                    ] += 1
                                elif over_no < 40:
                                    player_details.loc[
                                        ball[delivery]["bowler"], "bowledlbw_2"
                                    ] += 1
                                else:
                                    player_details.loc[
                                        ball[delivery]["bowler"], "bowledlbw_3"
                                    ] += 1

                if "extras" in ball[delivery]:
                    player_details.loc[ball[delivery]["bowler"], "extras"] += ball[
                        delivery
                    ]["runs"]["extras"]

                if over_no < 10:
                    player_details.loc[ball[delivery]["bowler"], "balls_1"] += 1
                    player_details.loc[ball[delivery]["bowler"], "runs_1"] += ball[
                        delivery
                    ]["runs"]["total"]
                elif over_no < 40:
                    player_details.loc[ball[delivery]["bowler"], "balls_2"] += 1
                    player_details.loc[ball[delivery]["bowler"], "runs_2"] += ball[
                        delivery
                    ]["runs"]["total"]
                else:
                    player_details.loc[ball[delivery]["bowler"], "balls_3"] += 1
                    player_details.loc[ball[delivery]["bowler"], "runs_3"] += ball[
                        delivery
                    ]["runs"]["total"]

                player_details.loc[ball[delivery]["bowler"], "runs"] += ball[delivery][
                    "runs"
                ]["total"]
                player_details.loc[ball[delivery]["bowler"], "dots"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 0
                )
                player_details.loc[ball[delivery]["bowler"], "1s"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 1
                )
                player_details.loc[ball[delivery]["bowler"], "2s"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 2
                )
                player_details.loc[ball[delivery]["bowler"], "4s"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 4
                )
                player_details.loc[ball[delivery]["bowler"], "6s"] += (
                    player_details.loc[ball[delivery]["bowler"], "runs"] == 6
                )
                player_details.loc[ball[delivery]["bowler"], "balls"] += 1

    return match_details, player_details, wickets


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

        overall_bowler_details = pd.DataFrame(
            columns=[
                "team",
                "innings",
                "runs",
                "extras",
                "balls",
                "1s",
                "2s",
                "4s",
                "6s",
                "dots",
                "balls_1",
                "balls_2",
                "balls_3",
                "bowledlbw",
                "bowledlbw_1",
                "bowledlbw_2",
                "bowledlbw_3",
                "wickets",
                "wickets_1",
                "wickets_2",
                "wickets_3",
                "maidens",
                "maidens_1",
                "maidens_2",
                "maidens_3",
                "average",
                "strike_rate",
                "economy",
                "1haul",
                "3haul",
                "5haul",
            ]
        )
        match_bowler_details = pd.DataFrame(
            columns=[
                "index",
                "match_id",
                "date",
                "player_id",
                "player_name",
                "team_name",
                "opposition_name",
                "venue_name",
                "innings_played",
                "format",
                "previous_balls_involved",
                "previous_average",
                "previous_strike_rate",
                "runs_1",
                "runs_2",
                "runs_3",
                "balls_1",
                "balls_2",
                "balls_3",
                "wickets_1",
                "wickets_2",
                "wickets_3",
                "bowledlbw_1",
                "bowledlbw_2",
                "bowledlbw_3",
                "maidens_1",
                "maidens_2",
                "maidens_3",
                "venue_dismissals",
                "venue_innings",
                "venue_economy",
                "venue_average",
                "venue_maidens",
                "venue_bowledlbw",
                "previous_wickets",
                "previous_wickets_1",
                "previous_wickets_2",
                "previous_wickets_3",
                "previous_maidens",
                "previous_maidens_1",
                "previous_maidens_2",
                "previous_maidens_3",
                "previous_bowledlbw",
                "previous_bowledlbw_1",
                "previous_bowledlbw_2",
                "previous_bowledlbw_3",
                "previous_economy",
                "previous_1haul",
                "previous_3haul",
                "previous_5haul",
                "runs",
                "extras",
                "balls",
                "1s",
                "2s",
                "4s",
                "6s",
                "balls_involved",
                "maidens",
                "wickets",
                "bowledlbw",
                "average",
                "strike_rate",
                "economy",
                "strike_rate_1",
                "strike_rate_2",
                "strike_rate_3",
                "vboDa_economy_1",
                "vboDa_dismissals_1",
                "vboDa_bowledlbw_1",
                "vboDa_maidens_1",
                "vboDa_economy_2",
                "vboDa_dismissals_2",
                "vboDa_bowledlbw_2",
                "vboDa_maidens_2",
                "vboDa_economy_3",
                "vboDa_dismissals_3",
                "vboDa_bowledlbw_3",
                "vboDa_maidens_3",
                "vboDa_economy_agg",
                "vboDa_dismissals_agg",
                "vboDa_bowledlbw_agg",
                "vboDa_maidens_agg",
                "tboDa_economy_1",
                "tboDa_dismissals_1",
                "tboDa_bowledlbw_1",
                "tboDa_maidens_1",
                "tboDa_economy_2",
                "tboDa_dismissals_2",
                "tboDa_maidens_2",
                "tboDa_bowledlbw_2",
                "tboDa_economy_3",
                "tboDa_dismissals_3",
                "tboDa_bowledlbw_3",
                "tboDa_maidens_3",
                "tboDa_economy_agg",
                "tboDa_dismissals_agg",
                "tboDa_bowledlbw_agg",
                "tboDa_maidens_agg",
                "fboDa_economy_1",
                "fboDa_dismissals_1",
                "fboDa_bowledlbw_1",
                "fboDa_maidens_1",
                "fboDa_economy_2",
                "fboDa_dismissals_2",
                "fboDa_maidens_2",
                "fboDa_bowledlbw_2",
                "fboDa_economy_3",
                "fboDa_dismissals_3",
                "fboDa_bowledlbw_3",
                "fboDa_maidens_3",
                "fboDa_economy_agg",
                "fboDa_dismissals_agg",
                "fboDa_bowledlbw_agg",
                "fboDa_maidens_agg",
                "match_wickets",
                "match_bowledlbw",
                "match_economy",
                "match_maidens",
            ]
        )
        match_bowler_details.set_index("index", inplace=True)
        count = -1

        venue_dict = {}

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
            match_details, player_details, wickets = extract_details(location)

            temp = {}
            temp["caught"] = 0
            temp["run_out"] = 0
            temp["stumped"] = 0
            temp["wickets"] = 0
            temp["bowledlbw"] = 0
            temp["maidens"] = 0
            temp["runs"] = 0
            temp["balls"] = 0
            for player in player_details.index:
                count += 1

                venue = match_details["venue"]

                try:
                    overall_bowler_details.index.get_loc(player)
                except:
                    overall_bowler_details.loc[player, "team"] = player_details.loc[
                        player, "team"
                    ]
                    overall_bowler_details.loc[player, "innings"] = 0
                    overall_bowler_details.loc[player, "runs"] = 0
                    overall_bowler_details.loc[player, "extras"] = 0
                    overall_bowler_details.loc[player, "balls"] = 0
                    overall_bowler_details.loc[player, "1s"] = 0
                    overall_bowler_details.loc[player, "2s"] = 0
                    overall_bowler_details.loc[player, "4s"] = 0
                    overall_bowler_details.loc[player, "6s"] = 0
                    overall_bowler_details.loc[player, "dots"] = 0
                    overall_bowler_details.loc[player, "maidens"] = 0
                    overall_bowler_details.loc[player, "maidens_1"] = 0
                    overall_bowler_details.loc[player, "maidens_2"] = 0
                    overall_bowler_details.loc[player, "maidens_3"] = 0
                    overall_bowler_details.loc[player, "wickets"] = 0
                    overall_bowler_details.loc[player, "wickets_1"] = 0
                    overall_bowler_details.loc[player, "wickets_2"] = 0
                    overall_bowler_details.loc[player, "wickets_3"] = 0
                    overall_bowler_details.loc[player, "bowledlbw"] = 0
                    overall_bowler_details.loc[player, "bowledlbw_1"] = 0
                    overall_bowler_details.loc[player, "bowledlbw_2"] = 0
                    overall_bowler_details.loc[player, "bowledlbw_3"] = 0
                    overall_bowler_details.loc[player, "average"] = 0
                    overall_bowler_details.loc[player, "strike_rate"] = 0
                    overall_bowler_details.loc[player, "economy"] = 0
                    overall_bowler_details.loc[player, "1haul"] = 0
                    overall_bowler_details.loc[player, "3haul"] = 0
                    overall_bowler_details.loc[player, "5haul"] = 0
                    overall_bowler_details.loc[player, "balls_1"] = 0
                    overall_bowler_details.loc[player, "balls_2"] = 0
                    overall_bowler_details.loc[player, "balls_3"] = 0

                ours = match_bowler_details[
                    (match_bowler_details["venue_name"] == venue)
                    & (match_bowler_details["player_name"] == player)
                ]
                if ours.empty:
                    match_bowler_details.loc[count, "vboDa_economy_1"] = 0
                    match_bowler_details.loc[count, "vboDa_economy_2"] = 0
                    match_bowler_details.loc[count, "vboDa_economy_3"] = 0
                    match_bowler_details.loc[count, "vboDa_economy_agg"] = 0
                    match_bowler_details.loc[count, "vboDa_dismissals_1"] = 0
                    match_bowler_details.loc[count, "vboDa_dismissals_2"] = 0
                    match_bowler_details.loc[count, "vboDa_dismissals_3"] = 0
                    match_bowler_details.loc[count, "vboDa_dismissals_agg"] = 0
                    match_bowler_details.loc[count, "vboDa_bowledlbw_1"] = 0
                    match_bowler_details.loc[count, "vboDa_bowledlbw_2"] = 0
                    match_bowler_details.loc[count, "vboDa_bowledlbw_3"] = 0
                    match_bowler_details.loc[count, "vboDa_bowledlbw_agg"] = 0
                    match_bowler_details.loc[count, "vboDa_maidens_1"] = 0
                    match_bowler_details.loc[count, "vboDa_maidens_2"] = 0
                    match_bowler_details.loc[count, "vboDa_maidens_3"] = 0
                    match_bowler_details.loc[count, "vboDa_maidens_agg"] = 0
                else:
                    match_bowler_details.loc[count, "vboDa_economy_1"] = (
                        sum(ours["runs_1"])
                        * 6
                        / (sum(ours["balls_1"]) if sum(ours["balls_1"]) != 0 else 1)
                    )
                    match_bowler_details.loc[count, "vboDa_economy_2"] = (
                        sum(ours["runs_2"])
                        * 6
                        / (sum(ours["balls_2"]) if sum(ours["balls_2"]) != 0 else 1)
                    )
                    match_bowler_details.loc[count, "vboDa_economy_3"] = (
                        sum(ours["runs_3"])
                        * 6
                        / (sum(ours["balls_3"]) if sum(ours["balls_3"]) != 0 else 1)
                    )
                    match_bowler_details.loc[count, "vboDa_economy_agg"] = (
                        sum(ours["runs"])
                        * 6
                        / (sum(ours["balls"]) if sum(ours["balls"]) != 0 else 1)
                    )
                    match_bowler_details.loc[count, "vboDa_dismissals_1"] = ours[
                        "wickets_1"
                    ].mean()
                    match_bowler_details.loc[count, "vboDa_dismissals_2"] = ours[
                        "wickets_2"
                    ].mean()
                    match_bowler_details.loc[count, "vboDa_dismissals_3"] = ours[
                        "wickets_3"
                    ].mean()
                    match_bowler_details.loc[count, "vboDa_dismissals_agg"] = ours[
                        "wickets"
                    ].mean()
                    match_bowler_details.loc[count, "vboDa_bowledlbw_1"] = ours[
                        "bowledlbw_1"
                    ].mean()
                    match_bowler_details.loc[count, "vboDa_bowledlbw_2"] = ours[
                        "bowledlbw_2"
                    ].mean()
                    match_bowler_details.loc[count, "vboDa_bowledlbw_3"] = ours[
                        "bowledlbw_3"
                    ].mean()
                    match_bowler_details.loc[count, "vboDa_bowledlbw_agg"] = ours[
                        "bowledlbw"
                    ].mean()
                    match_bowler_details.loc[count, "vboDa_maidens_1"] = ours[
                        "maidens_1"
                    ].mean()
                    match_bowler_details.loc[count, "vboDa_maidens_2"] = ours[
                        "maidens_2"
                    ].mean()
                    match_bowler_details.loc[count, "vboDa_maidens_3"] = ours[
                        "maidens_3"
                    ].mean()
                    match_bowler_details.loc[count, "vboDa_maidens_agg"] = ours[
                        "maidens"
                    ].mean()

                ours = match_bowler_details[
                    (match_bowler_details["player_name"] == player)
                ]
                if ours.empty:
                    match_bowler_details.loc[count, "tboDa_economy_1"] = 0
                    match_bowler_details.loc[count, "tboDa_economy_2"] = 0
                    match_bowler_details.loc[count, "tboDa_economy_3"] = 0
                    match_bowler_details.loc[count, "tboDa_economy_agg"] = 0
                    match_bowler_details.loc[count, "tboDa_dismissals_1"] = 0
                    match_bowler_details.loc[count, "tboDa_dismissals_2"] = 0
                    match_bowler_details.loc[count, "tboDa_dismissals_3"] = 0
                    match_bowler_details.loc[count, "tboDa_dismissals_agg"] = 0
                    match_bowler_details.loc[count, "tboDa_bowledlbw_1"] = 0
                    match_bowler_details.loc[count, "tboDa_bowledlbw_2"] = 0
                    match_bowler_details.loc[count, "tboDa_bowledlbw_3"] = 0
                    match_bowler_details.loc[count, "tboDa_bowledlbw_agg"] = 0
                    match_bowler_details.loc[count, "tboDa_maidens_1"] = 0
                    match_bowler_details.loc[count, "tboDa_maidens_2"] = 0
                    match_bowler_details.loc[count, "tboDa_maidens_3"] = 0
                    match_bowler_details.loc[count, "tboDa_maidens_agg"] = 0
                else:
                    match_bowler_details.loc[count, "tboDa_economy_1"] = (
                        sum(ours["runs_1"])
                        * 6
                        / (sum(ours["balls_1"]) if sum(ours["balls_1"]) != 0 else 1)
                    )
                    match_bowler_details.loc[count, "tboDa_economy_2"] = (
                        sum(ours["runs_2"])
                        * 6
                        / (sum(ours["balls_2"]) if sum(ours["balls_2"]) != 0 else 1)
                    )
                    match_bowler_details.loc[count, "tboDa_economy_3"] = (
                        sum(ours["runs_3"])
                        * 6
                        / (sum(ours["balls_3"]) if sum(ours["balls_3"]) != 0 else 1)
                    )
                    match_bowler_details.loc[count, "tboDa_economy_agg"] = (
                        sum(ours["runs"])
                        * 6
                        / (sum(ours["balls"]) if sum(ours["balls"]) != 0 else 1)
                    )
                    match_bowler_details.loc[count, "tboDa_dismissals_1"] = ours[
                        "wickets_1"
                    ].mean()
                    match_bowler_details.loc[count, "tboDa_dismissals_2"] = ours[
                        "wickets_2"
                    ].mean()
                    match_bowler_details.loc[count, "tboDa_dismissals_3"] = ours[
                        "wickets_3"
                    ].mean()
                    match_bowler_details.loc[count, "tboDa_dismissals_agg"] = ours[
                        "wickets"
                    ].mean()
                    match_bowler_details.loc[count, "tboDa_bowledlbw_1"] = ours[
                        "bowledlbw_1"
                    ].mean()
                    match_bowler_details.loc[count, "tboDa_bowledlbw_2"] = ours[
                        "bowledlbw_2"
                    ].mean()
                    match_bowler_details.loc[count, "tboDa_bowledlbw_3"] = ours[
                        "bowledlbw_3"
                    ].mean()
                    match_bowler_details.loc[count, "tboDa_bowledlbw_agg"] = ours[
                        "bowledlbw"
                    ].mean()
                    match_bowler_details.loc[count, "tboDa_maidens_1"] = ours[
                        "maidens_1"
                    ].mean()
                    match_bowler_details.loc[count, "tboDa_maidens_2"] = ours[
                        "maidens_2"
                    ].mean()
                    match_bowler_details.loc[count, "tboDa_maidens_3"] = ours[
                        "maidens_3"
                    ].mean()
                    match_bowler_details.loc[count, "tboDa_maidens_agg"] = ours[
                        "maidens"
                    ].mean()

                ours = match_bowler_details[
                    (match_bowler_details["player_name"] == player)
                ].tail(10)
                if ours.empty:
                    match_bowler_details.loc[count, "fboDa_economy_1"] = 0
                    match_bowler_details.loc[count, "fboDa_economy_2"] = 0
                    match_bowler_details.loc[count, "fboDa_economy_3"] = 0
                    match_bowler_details.loc[count, "fboDa_economy_agg"] = 0
                    match_bowler_details.loc[count, "fboDa_dismissals_1"] = 0
                    match_bowler_details.loc[count, "fboDa_dismissals_2"] = 0
                    match_bowler_details.loc[count, "fboDa_dismissals_3"] = 0
                    match_bowler_details.loc[count, "fboDa_dismissals_agg"] = 0
                    match_bowler_details.loc[count, "fboDa_bowledlbw_1"] = 0
                    match_bowler_details.loc[count, "fboDa_bowledlbw_2"] = 0
                    match_bowler_details.loc[count, "fboDa_bowledlbw_3"] = 0
                    match_bowler_details.loc[count, "fboDa_bowledlbw_agg"] = 0
                    match_bowler_details.loc[count, "fboDa_maidens_1"] = 0
                    match_bowler_details.loc[count, "fboDa_maidens_2"] = 0
                    match_bowler_details.loc[count, "fboDa_maidens_3"] = 0
                    match_bowler_details.loc[count, "fboDa_maidens_agg"] = 0
                else:
                    match_bowler_details.loc[count, "fboDa_economy_1"] = (
                        sum(ours["runs_1"])
                        * 6
                        / (sum(ours["balls_1"]) if sum(ours["balls_1"]) != 0 else 1)
                    )
                    match_bowler_details.loc[count, "fboDa_economy_2"] = (
                        sum(ours["runs_2"])
                        * 6
                        / (sum(ours["balls_2"]) if sum(ours["balls_2"]) != 0 else 1)
                    )
                    match_bowler_details.loc[count, "fboDa_economy_3"] = (
                        sum(ours["runs_3"])
                        * 6
                        / (sum(ours["balls_3"]) if sum(ours["balls_3"]) != 0 else 1)
                    )
                    match_bowler_details.loc[count, "fboDa_economy_agg"] = (
                        sum(ours["runs"])
                        * 6
                        / (sum(ours["balls"]) if sum(ours["balls"]) != 0 else 1)
                    )
                    match_bowler_details.loc[count, "fboDa_dismissals_1"] = ours[
                        "wickets_1"
                    ].mean()
                    match_bowler_details.loc[count, "fboDa_dismissals_2"] = ours[
                        "wickets_2"
                    ].mean()
                    match_bowler_details.loc[count, "fboDa_dismissals_3"] = ours[
                        "wickets_3"
                    ].mean()
                    match_bowler_details.loc[count, "fboDa_dismissals_agg"] = ours[
                        "wickets"
                    ].mean()
                    match_bowler_details.loc[count, "fboDa_bowledlbw_1"] = ours[
                        "bowledlbw_1"
                    ].mean()
                    match_bowler_details.loc[count, "fboDa_bowledlbw_2"] = ours[
                        "bowledlbw_2"
                    ].mean()
                    match_bowler_details.loc[count, "fboDa_bowledlbw_3"] = ours[
                        "bowledlbw_3"
                    ].mean()
                    match_bowler_details.loc[count, "fboDa_bowledlbw_agg"] = ours[
                        "bowledlbw"
                    ].mean()
                    match_bowler_details.loc[count, "fboDa_maidens_1"] = ours[
                        "maidens_1"
                    ].mean()
                    match_bowler_details.loc[count, "fboDa_maidens_2"] = ours[
                        "maidens_2"
                    ].mean()
                    match_bowler_details.loc[count, "fboDa_maidens_3"] = ours[
                        "maidens_3"
                    ].mean()
                    match_bowler_details.loc[count, "fboDa_maidens_agg"] = ours[
                        "maidens"
                    ].mean()

                match_bowler_details.loc[count, "match_id"] = i
                match_bowler_details.loc[count, "date"] = player_details.loc[
                    player, "date"
                ]
                match_bowler_details.loc[count, "player_name"] = player
                # put player_id here
                match_bowler_details.loc[count, "team_name"] = player_details.loc[
                    player, "team"
                ]
                match_bowler_details.loc[count, "opposition_name"] = player_details.loc[
                    player, "opposition"
                ]
                match_bowler_details.loc[count, "venue_name"] = player_details.loc[
                    player, "venue"
                ]
                match_bowler_details.loc[
                    count, "innings_played"
                ] = overall_bowler_details.loc[player, "innings"]
                match_bowler_details.loc[count, "format"] = match_details["format"]

                match_bowler_details.loc[
                    count, "previous_balls_involved"
                ] = overall_bowler_details.loc[player, "dots"]
                match_bowler_details.loc[
                    count, "previous_average"
                ] = overall_bowler_details.loc[player, "average"]
                match_bowler_details.loc[
                    count, "previous_strike_rate"
                ] = overall_bowler_details.loc[player, "strike_rate"]
                match_bowler_details.loc[
                    count, "previous_economy"
                ] = overall_bowler_details.loc[player, "economy"]
                match_bowler_details.loc[
                    count, "previous_1haul"
                ] = overall_bowler_details.loc[player, "1haul"]
                match_bowler_details.loc[
                    count, "previous_3haul"
                ] = overall_bowler_details.loc[player, "3haul"]
                match_bowler_details.loc[
                    count, "previous_5haul"
                ] = overall_bowler_details.loc[player, "5haul"]

                match_bowler_details.loc[
                    count, "previous_wickets"
                ] = overall_bowler_details.loc[player, "wickets"]
                match_bowler_details.loc[
                    count, "previous_wickets_1"
                ] = overall_bowler_details.loc[player, "wickets_1"]
                match_bowler_details.loc[
                    count, "previous_wickets_2"
                ] = overall_bowler_details.loc[player, "wickets_2"]
                match_bowler_details.loc[
                    count, "previous_wickets_3"
                ] = overall_bowler_details.loc[player, "wickets_3"]
                match_bowler_details.loc[
                    count, "previous_maidens"
                ] = overall_bowler_details.loc[player, "maidens"]
                match_bowler_details.loc[
                    count, "previous_maidens_1"
                ] = overall_bowler_details.loc[player, "maidens_1"]
                match_bowler_details.loc[
                    count, "previous_maidens_2"
                ] = overall_bowler_details.loc[player, "maidens_2"]
                match_bowler_details.loc[
                    count, "previous_maidens_3"
                ] = overall_bowler_details.loc[player, "maidens_3"]
                match_bowler_details.loc[
                    count, "previous_bowledlbw"
                ] = overall_bowler_details.loc[player, "bowledlbw"]
                match_bowler_details.loc[
                    count, "previous_bowledlbw_1"
                ] = overall_bowler_details.loc[player, "bowledlbw_1"]
                match_bowler_details.loc[
                    count, "previous_bowledlbw_2"
                ] = overall_bowler_details.loc[player, "bowledlbw_2"]
                match_bowler_details.loc[
                    count, "previous_bowledlbw_3"
                ] = overall_bowler_details.loc[player, "bowledlbw_3"]

                match_bowler_details.loc[count, "runs_1"] = player_details.loc[
                    player, "runs_1"
                ]
                match_bowler_details.loc[count, "runs_2"] = player_details.loc[
                    player, "runs_2"
                ]
                match_bowler_details.loc[count, "runs_3"] = player_details.loc[
                    player, "runs_3"
                ]
                match_bowler_details.loc[count, "wickets_1"] = player_details.loc[
                    player, "wickets_1"
                ]
                match_bowler_details.loc[count, "wickets_2"] = player_details.loc[
                    player, "wickets_2"
                ]
                match_bowler_details.loc[count, "wickets_3"] = player_details.loc[
                    player, "wickets_3"
                ]
                match_bowler_details.loc[count, "balls_1"] = player_details.loc[
                    player, "balls_1"
                ]
                match_bowler_details.loc[count, "balls_2"] = player_details.loc[
                    player, "balls_2"
                ]
                match_bowler_details.loc[count, "balls_3"] = player_details.loc[
                    player, "balls_3"
                ]
                match_bowler_details.loc[count, "bowledlbw_1"] = player_details.loc[
                    player, "bowledlbw_1"
                ]
                match_bowler_details.loc[count, "bowledlbw_2"] = player_details.loc[
                    player, "bowledlbw_2"
                ]
                match_bowler_details.loc[count, "bowledlbw_3"] = player_details.loc[
                    player, "bowledlbw_3"
                ]
                match_bowler_details.loc[count, "maidens_1"] = player_details.loc[
                    player, "maidens_1"
                ]
                match_bowler_details.loc[count, "maidens_2"] = player_details.loc[
                    player, "maidens_2"
                ]
                match_bowler_details.loc[count, "maidens_3"] = player_details.loc[
                    player, "maidens_3"
                ]

                match_bowler_details.loc[count, "runs"] = player_details.loc[
                    player, "runs"
                ]
                match_bowler_details.loc[count, "extras"] = player_details.loc[
                    player, "extras"
                ]
                match_bowler_details.loc[count, "balls"] = player_details.loc[
                    player, "balls"
                ]
                match_bowler_details.loc[count, "1s"] = player_details.loc[player, "1s"]
                match_bowler_details.loc[count, "2s"] = player_details.loc[player, "2s"]
                match_bowler_details.loc[count, "4s"] = player_details.loc[player, "4s"]
                match_bowler_details.loc[count, "6s"] = player_details.loc[player, "6s"]
                match_bowler_details.loc[count, "balls_involved"] = player_details.loc[
                    player, "dots"
                ]
                match_bowler_details.loc[count, "maidens"] = player_details.loc[
                    player, "maidens"
                ]
                match_bowler_details.loc[count, "wickets"] = player_details.loc[
                    player, "wickets"
                ]
                match_bowler_details.loc[count, "bowledlbw"] = player_details.loc[
                    player, "bowledlbw"
                ]

                if match_bowler_details.loc[count, "wickets"] == 0:
                    match_bowler_details.loc[count, "strike_rate"] = 0
                else:
                    match_bowler_details.loc[count, "strike_rate"] = (
                        match_bowler_details.loc[count, "balls"]
                        / match_bowler_details.loc[count, "wickets"]
                    )
                if (
                    overall_bowler_details.loc[player, "wickets"]
                    + match_bowler_details.loc[count, "wickets"]
                    == 0
                ):
                    match_bowler_details.loc[count, "average"] = 0
                else:
                    match_bowler_details.loc[count, "average"] = (
                        overall_bowler_details.loc[player, "runs"]
                        + match_bowler_details.loc[count, "runs"]
                    ) / (
                        overall_bowler_details.loc[player, "wickets"]
                        + match_bowler_details.loc[count, "wickets"]
                    )
                if player_details.loc[player, "overs"] == 0:
                    match_bowler_details.loc[
                        count, "economy"
                    ] = match_bowler_details.loc[count, "runs"]
                else:
                    match_bowler_details.loc[count, "economy"] = (
                        match_bowler_details.loc[count, "runs"]
                        / player_details.loc[player, "overs"]
                    )

                match_bowler_details.loc[count, "strike_rate_1"] = (
                    (
                        overall_bowler_details.loc[player, "balls_1"]
                        / overall_bowler_details.loc[player, "wickets_1"]
                    )
                    if overall_bowler_details.loc[player, "wickets_1"] != 0
                    else 0
                )
                match_bowler_details.loc[count, "strike_rate_2"] = (
                    (
                        overall_bowler_details.loc[player, "balls_2"]
                        / overall_bowler_details.loc[player, "wickets_2"]
                    )
                    if overall_bowler_details.loc[player, "wickets_2"] != 0
                    else 0
                )
                match_bowler_details.loc[count, "strike_rate_3"] = (
                    (
                        overall_bowler_details.loc[player, "balls_3"]
                        / overall_bowler_details.loc[player, "wickets_3"]
                    )
                    if overall_bowler_details.loc[player, "wickets_3"] != 0
                    else 0
                )

                # PREVIOUS DATA
                if venue not in venue_dict:
                    venue_dict[venue] = {}
                    venue_dict[venue]["caught"] = 0
                    venue_dict[venue]["run_out"] = 0
                    venue_dict[venue]["stumped"] = 0
                    venue_dict[venue]["innings"] = 0
                    venue_dict[venue]["wickets"] = 0
                    venue_dict[venue]["bowledlbw"] = 0
                    venue_dict[venue]["maidens"] = 0
                    venue_dict[venue]["runs"] = 0
                    venue_dict[venue]["balls"] = 0

                # NEW ONES
                match_bowler_details.loc[count, "venue_innings"] = venue_dict[venue][
                    "innings"
                ]
                match_bowler_details.loc[count, "venue_dismissals"] = venue_dict[venue][
                    "wickets"
                ] / (
                    venue_dict[venue]["innings"]
                    if venue_dict[venue]["innings"] != 0
                    else 1
                )
                if venue_dict[venue]["balls"] != 0:
                    match_bowler_details.loc[count, "venue_economy"] = (
                        venue_dict[venue]["runs"] * 6 / venue_dict[venue]["balls"]
                    )
                else:
                    match_bowler_details.loc[count, "venue_economy"] = 0
                if venue_dict[venue]["wickets"] != 0:
                    match_bowler_details.loc[count, "venue_average"] = (
                        venue_dict[venue]["runs"] / venue_dict[venue]["wickets"]
                    )
                else:
                    match_bowler_details.loc[count, "venue_average"] = venue_dict[
                        venue
                    ]["runs"]
                match_bowler_details.loc[count, "venue_maidens"] = venue_dict[venue][
                    "maidens"
                ] / (
                    venue_dict[venue]["innings"]
                    if venue_dict[venue]["innings"] != 0
                    else 1
                )
                match_bowler_details.loc[count, "venue_bowledlbw"] = venue_dict[venue][
                    "bowledlbw"
                ] / (
                    venue_dict[venue]["innings"]
                    if venue_dict[venue]["innings"] != 0
                    else 1
                )

                # 'match_wickets','match_bowledlbw','match_economy','match_maidens'
                match_bowler_details.loc[
                    count, "match_wickets"
                ] = match_bowler_details.loc[count, "wickets"]
                match_bowler_details.loc[
                    count, "match_bowledlbw"
                ] = match_bowler_details.loc[count, "bowledlbw"]
                match_bowler_details.loc[
                    count, "match_economy"
                ] = match_bowler_details.loc[count, "economy"]
                match_bowler_details.loc[
                    count, "match_maidens"
                ] = match_bowler_details.loc[count, "maidens"]
                bonus = 0
                if match_bowler_details.loc[count, "match_wickets"] == 3:
                    bonus = 4
                if match_bowler_details.loc[count, "match_wickets"] == 4:
                    bonus = 8
                if match_bowler_details.loc[count, "match_wickets"] >= 5:
                    bonus = 16
                match_bowler_details.loc[count, "match_fantasy_points"] = (
                    25 * match_bowler_details.loc[count, "match_wickets"]
                    + 8 * match_bowler_details.loc[count, "match_bowledlbw"]
                    + bonus
                    + 12 * match_bowler_details.loc[count, "match_maidens"]
                )

                if match_bowler_details.loc[count, "balls"] > 12:
                    if match_bowler_details.loc[count, "match_economy"] < 5:
                        match_bowler_details.loc[count, "match_fantasy_points"] += 6
                    elif match_bowler_details.loc[count, "match_economy"] < 6:
                        match_bowler_details.loc[count, "match_fantasy_points"] += 4
                    elif match_bowler_details.loc[count, "match_economy"] < 7:
                        match_bowler_details.loc[count, "match_fantasy_points"] += 2

                    if match_bowler_details.loc[count, "match_economy"] > 12:
                        match_bowler_details.loc[count, "match_fantasy_points"] -= 6
                    elif match_bowler_details.loc[count, "match_economy"] > 11:
                        match_bowler_details.loc[count, "match_fantasy_points"] -= 4
                    elif match_bowler_details.loc[count, "match_economy"] > 10:
                        match_bowler_details.loc[count, "match_fantasy_points"] -= 2

                overall_bowler_details.loc[player, "innings"] += 1
                overall_bowler_details.loc[player, "runs"] += player_details.loc[
                    player, "runs"
                ]
                overall_bowler_details.loc[player, "extras"] += player_details.loc[
                    player, "extras"
                ]
                overall_bowler_details.loc[player, "1s"] += player_details.loc[
                    player, "1s"
                ]
                overall_bowler_details.loc[player, "2s"] += player_details.loc[
                    player, "2s"
                ]
                overall_bowler_details.loc[player, "4s"] += player_details.loc[
                    player, "4s"
                ]
                overall_bowler_details.loc[player, "6s"] += player_details.loc[
                    player, "6s"
                ]
                overall_bowler_details.loc[player, "dots"] += player_details.loc[
                    player, "dots"
                ]
                overall_bowler_details.loc[player, "balls"] += player_details.loc[
                    player, "balls"
                ]
                overall_bowler_details.loc[player, "balls_1"] += player_details.loc[
                    player, "balls_1"
                ]
                overall_bowler_details.loc[player, "balls_2"] += player_details.loc[
                    player, "balls_2"
                ]
                overall_bowler_details.loc[player, "balls_3"] += player_details.loc[
                    player, "balls_3"
                ]

                overall_bowler_details.loc[player, "maidens"] += player_details.loc[
                    player, "maidens"
                ]
                overall_bowler_details.loc[player, "maidens_1"] += player_details.loc[
                    player, "maidens_1"
                ]
                overall_bowler_details.loc[player, "maidens_2"] += player_details.loc[
                    player, "maidens_2"
                ]
                overall_bowler_details.loc[player, "maidens_3"] += player_details.loc[
                    player, "maidens_3"
                ]
                overall_bowler_details.loc[player, "wickets"] += player_details.loc[
                    player, "wickets"
                ]
                overall_bowler_details.loc[player, "wickets_1"] += player_details.loc[
                    player, "wickets_1"
                ]
                overall_bowler_details.loc[player, "wickets_2"] += player_details.loc[
                    player, "wickets_2"
                ]
                overall_bowler_details.loc[player, "wickets_3"] += player_details.loc[
                    player, "wickets_3"
                ]
                overall_bowler_details.loc[player, "bowledlbw"] += player_details.loc[
                    player, "bowledlbw"
                ]
                overall_bowler_details.loc[player, "bowledlbw_1"] += player_details.loc[
                    player, "bowledlbw_1"
                ]
                overall_bowler_details.loc[player, "bowledlbw_2"] += player_details.loc[
                    player, "bowledlbw_2"
                ]
                overall_bowler_details.loc[player, "bowledlbw_3"] += player_details.loc[
                    player, "bowledlbw_3"
                ]
                if player_details.loc[player, "wickets"] != 0:
                    overall_bowler_details.loc[player, "average"] = (
                        (
                            player_details.loc[player, "runs"]
                            / player_details.loc[player, "wickets"]
                        )
                        + (
                            overall_bowler_details.loc[player, "average"]
                            * (overall_bowler_details.loc[player, "innings"] - 1)
                        )
                    ) / overall_bowler_details.loc[player, "innings"]
                    overall_bowler_details.loc[player, "strike_rate"] = (
                        (
                            player_details.loc[player, "balls"]
                            / player_details.loc[player, "wickets"]
                        )
                        + (
                            overall_bowler_details.loc[player, "strike_rate"]
                            * (overall_bowler_details.loc[player, "innings"] - 1)
                        )
                    ) / overall_bowler_details.loc[player, "innings"]
                overall_bowler_details.loc[player, "economy"] = (
                    (
                        player_details.loc[player, "runs"]
                        * 6
                        / player_details.loc[player, "balls"]
                    )
                    + (
                        overall_bowler_details.loc[player, "economy"]
                        * (overall_bowler_details.loc[player, "innings"] - 1)
                    )
                ) / overall_bowler_details.loc[player, "innings"]
                if (
                    player_details.loc[player, "wickets"] >= 1
                    and player_details.loc[player, "wickets"] < 4
                ):
                    overall_bowler_details.loc[player, "1haul"] += 1
                if (
                    player_details.loc[player, "wickets"] >= 3
                    and player_details.loc[player, "wickets"] < 5
                ):
                    overall_bowler_details.loc[player, "3haul"] += 1
                if player_details.loc[player, "wickets"] >= 5:
                    overall_bowler_details.loc[player, "5haul"] += 1

                temp["caught"] += wickets["caught"]
                temp["run_out"] += wickets["run_out"]
                temp["stumped"] += wickets["stumped"]
                temp["wickets"] += wickets["wickets"]
                temp["bowledlbw"] += sum(player_details["bowledlbw"])
                temp["maidens"] += sum(player_details["maidens"])
                temp["runs"] += sum(player_details["runs"])
                temp["balls"] += sum(player_details["balls"])

            venue_dict[venue]["caught"] += temp["caught"]
            venue_dict[venue]["run_out"] += temp["run_out"]
            venue_dict[venue]["stumped"] += temp["stumped"]
            venue_dict[venue]["wickets"] += temp["wickets"]
            venue_dict[venue]["bowledlbw"] += temp["bowledlbw"]
            venue_dict[venue]["maidens"] += temp["maidens"]
            venue_dict[venue]["runs"] += temp["runs"]
            venue_dict[venue]["balls"] += temp["balls"]
            venue_dict[venue]["innings"] += 1

        # UNCOMMENT TO ADD IDS
        location = os.path.join(
            "data", "raw", "additional_data", "people_with_images_and_countries.csv"
        )
        mapping = pd.read_csv(location)

        for i in range(len(match_bowler_details)):
            name = match_bowler_details.iloc[i]["player_name"]

            matched = mapping[mapping["unique_name"] == name]

            if not matched.empty:
                match_bowler_details.iloc[
                    i, match_bowler_details.columns.get_loc("player_id")
                ] = matched["identifier"].values[0]
            else:
                # print(f"No matching entry for {name}: {len(mapping[mapping['unique_name'] == name])} matches")
                match_bowler_details.iloc[
                    i, match_bowler_details.columns.get_loc("player_id")
                ] = "xxxxxxxx"

        target_columns = [
            "match_wickets",
            "match_bowledlbw",
            "match_economy",
            "match_maidens",
            "match_fantasy_points",
        ]
        for target_column in target_columns:
            if target_column in match_bowler_details.columns:
                new_column_name = f"{format}_{target_column}"
                match_bowler_details.rename(
                    columns={target_column: new_column_name}, inplace=True
                )
            else:
                print(f"Column '{target_column}' not found in bowler. Skipping...")

        overs = {}
        venue_dict = {}
        opposition_dict = {}

        for index, row in match_bowler_details.iterrows():
            player = row["player_name"]
            if player not in overs:
                overs[player] = 0
            match_bowler_details.loc[index, "consistency"] = (
                0.4174 * overs[player]
                + 0.2634 * row["innings_played"]
                + 0.1602 * row["previous_strike_rate"]
                + 0.0975 * row["previous_average"]
                + 0.0615 * row["previous_5haul"]
            )
            overs[player] += row["balls"] // 6

            indices = match_bowler_details[
                (match_bowler_details["player_name"] == player)
                & (match_bowler_details.index < index)
            ].index
            if len(indices) == 0:
                match_bowler_details.loc[index, "form"] = 0
            else:
                cur = match_bowler_details.loc[index]
                old = match_bowler_details.loc[index - min(10, len(indices))]
                avg = (
                    ((cur["runs"] - old["runs"]) / (cur["wickets"] - old["wickets"]))
                    if (cur["wickets"] - old["wickets"]) != 0
                    else 0
                )
                sr = (
                    ((cur["balls"] - old["balls"]) / (cur["wickets"] - old["wickets"]))
                    if (cur["wickets"] - old["wickets"]) != 0
                    else 0
                )
                match_bowler_details.loc[index, "form"] = (
                    0.3269 * ((cur["balls"] - old["balls"]) // 6)
                    + 0.2486 * min(10, len(indices))
                    + 0.1877 * sr
                    + 0.1210 * avg
                    + 0.0798 * (cur["previous_5haul"] - old["previous_5haul"])
                )

            opposition = row["opposition_name"]
            if player not in opposition_dict:
                opposition_dict[player] = {}
            if opposition not in opposition_dict[player]:
                opposition_dict[player][opposition] = {}
                opposition_dict[player][opposition]["innings"] = 0
                opposition_dict[player][opposition]["runs"] = 0
                opposition_dict[player][opposition]["balls"] = 0
                opposition_dict[player][opposition]["overs"] = 0
                opposition_dict[player][opposition]["wickets"] = 0
                opposition_dict[player][opposition]["5hauls"] = 0
            try:
                sr = (
                    opposition_dict[player][opposition]["balls"]
                    / opposition_dict[player][opposition]["wickets"]
                )
            except:
                sr = 0
            try:
                avg = (
                    opposition_dict[player][opposition]["runs"]
                    / opposition_dict[player][opposition]["wickets"]
                )
            except:
                avg = 0
            match_bowler_details.loc[index, "opposition"] = (
                0.3177 * opposition_dict[player][opposition]["overs"]
                + 0.3177 * opposition_dict[player][opposition]["innings"]
                + 0.1933 * sr
                + 0.1465 * avg
                + 0.0943 * opposition_dict[player][opposition]["5hauls"]
            )
            opposition_dict[player][opposition]["innings"] += 1
            opposition_dict[player][opposition]["runs"] += row["runs"]
            opposition_dict[player][opposition]["balls"] += row["balls"]
            opposition_dict[player][opposition]["overs"] += row["balls"] // 6
            opposition_dict[player][opposition]["wickets"] += row["wickets"]
            opposition_dict[player][opposition]["5hauls"] += row["wickets"] >= 3

            venue = row["venue_name"]
            if player not in venue_dict:
                venue_dict[player] = {}
            if venue not in venue_dict[player]:
                venue_dict[player][venue] = {}
                venue_dict[player][venue]["innings"] = 0
                venue_dict[player][venue]["runs"] = 0
                venue_dict[player][venue]["balls"] = 0
                venue_dict[player][venue]["overs"] = 0
                venue_dict[player][venue]["wickets"] = 0
                venue_dict[player][venue]["5hauls"] = 0
            try:
                sr = (
                    venue_dict[player][venue]["balls"]
                    / venue_dict[player][venue]["wickets"]
                )
            except:
                sr = 0
            try:
                avg = (
                    venue_dict[player][venue]["runs"]
                    / venue_dict[player][venue]["wickets"]
                )
            except:
                avg = 0
            match_bowler_details.loc[index, "venue"] = (
                0.3018 * venue_dict[player][venue]["overs"]
                + 0.2783 * venue_dict[player][venue]["innings"]
                + 0.1836 * sr
                + 0.1391 * avg
                + 0.0972 * venue_dict[player][venue]["5hauls"]
            )
            venue_dict[player][venue]["innings"] += 1
            venue_dict[player][venue]["runs"] += row["runs"]
            venue_dict[player][venue]["balls"] += row["balls"]
            venue_dict[player][venue]["overs"] += row["balls"] // 6
            venue_dict[player][venue]["wickets"] += row["wickets"]
            venue_dict[player][venue]["5hauls"] += row["wickets"] >= 3

        folder = os.path.join("data", "processed", format)
        os.makedirs(folder, exist_ok=True)
        file_name = "bowler.csv"
        match_bowler_details.to_csv(os.path.join(folder, file_name))
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
