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
    dict = yaml.load(open(filename), yaml.Loader)

    match_details = {}
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

    wickets = {}  # player by player

    try:
        for x in dict["info"]["players"]:
            for y in dict["info"]["players"][x]:
                wickets[y] = {}
                wickets[y]["caught"] = 0
                wickets[y]["run_out"] = 0
                wickets[y]["stumped"] = 0
    except:
        pass

    innings1 = dict["innings"][0]["1st innings"]["deliveries"]
    runs_this_over = 0
    for ball in innings1:
        for delivery in ball:

            if "wicket" in ball[delivery]:
                if "kind" in ball[delivery]["wicket"]:
                    try:
                        fielder = ball[delivery]["wicket"]["fielders"][0]
                        if fielder not in wickets:
                            wickets[fielder] = {}
                            wickets[fielder]["caught"] = 0
                            wickets[fielder]["run_out"] = 0
                            wickets[fielder]["stumped"] = 0
                        if "caught" in ball[delivery]["wicket"]["kind"]:
                            wickets[fielder]["caught"] += 1
                        if ball[delivery]["wicket"]["kind"] == "run out":
                            wickets[fielder]["run_out"] += 1
                        if ball[delivery]["wicket"]["kind"] == "stumped":
                            wickets[fielder]["stumped"] += 1
                    except:
                        pass
                else:
                    for x in ball[delivery]["wicket"]:
                        try:
                            fielder = x["fielders"][0]
                            if fielder not in wickets:
                                wickets[fielder] = {}
                                wickets[fielder]["caught"] = 0
                                wickets[fielder]["run_out"] = 0
                                wickets[fielder]["stumped"] = 0
                            if "caught" in x["kind"]:
                                wickets[fielder]["caught"] += 1
                            if x["kind"] == "run out":
                                wickets[fielder]["run_out"] += 1
                            if x["kind"] == "stumped":
                                wickets[fielder]["stumped"] += 1
                        except:
                            pass

    try:
        innings2 = dict["innings"][1]["2nd innings"]["deliveries"]
    except:
        flag = True
    else:
        for ball in innings2:
            for delivery in ball:

                if "wicket" in ball[delivery]:
                    if "kind" in ball[delivery]["wicket"]:
                        try:
                            fielder = ball[delivery]["wicket"]["fielders"][0]
                            if fielder not in wickets:
                                wickets[fielder] = {}
                                wickets[fielder]["caught"] = 0
                                wickets[fielder]["run_out"] = 0
                                wickets[fielder]["stumped"] = 0
                            if "caught" in ball[delivery]["wicket"]["kind"]:
                                wickets[fielder]["caught"] += 1
                            if ball[delivery]["wicket"]["kind"] == "run out":
                                wickets[fielder]["run_out"] += 1
                            if ball[delivery]["wicket"]["kind"] == "stumped":
                                wickets[fielder]["stumped"] += 1
                        except:
                            pass
                    else:
                        for x in ball[delivery]["wicket"]:
                            try:
                                fielder = x["fielders"][0]
                                if fielder not in wickets:
                                    wickets[fielder] = {}
                                    wickets[fielder]["caught"] = 0
                                    wickets[fielder]["run_out"] = 0
                                    wickets[fielder]["stumped"] = 0
                                if "caught" in x["kind"]:
                                    wickets[fielder]["caught"] += 1
                                if x["kind"] == "run out":
                                    wickets[fielder]["run_out"] += 1
                                if x["kind"] == "stumped":
                                    wickets[fielder]["stumped"] += 1
                            except:
                                pass

    try:
        innings3 = dict["innings"][2]["3rd innings"]["deliveries"]
    except:
        flag = True
    else:
        for ball in innings3:
            for delivery in ball:

                if "wicket" in ball[delivery]:
                    if "kind" in ball[delivery]["wicket"]:
                        try:
                            fielder = ball[delivery]["wicket"]["fielders"][0]
                            if fielder not in wickets:
                                wickets[fielder] = {}
                                wickets[fielder]["caught"] = 0
                                wickets[fielder]["run_out"] = 0
                                wickets[fielder]["stumped"] = 0
                            if "caught" in ball[delivery]["wicket"]["kind"]:
                                wickets[fielder]["caught"] += 1
                            if ball[delivery]["wicket"]["kind"] == "run out":
                                wickets[fielder]["run_out"] += 1
                            if ball[delivery]["wicket"]["kind"] == "stumped":
                                wickets[fielder]["stumped"] += 1
                        except:
                            pass
                    else:
                        for x in ball[delivery]["wicket"]:
                            try:
                                fielder = x["fielders"][0]
                                if fielder not in wickets:
                                    wickets[fielder] = {}
                                    wickets[fielder]["caught"] = 0
                                    wickets[fielder]["run_out"] = 0
                                    wickets[fielder]["stumped"] = 0
                                if "caught" in x["kind"]:
                                    wickets[fielder]["caught"] += 1
                                if x["kind"] == "run out":
                                    wickets[fielder]["run_out"] += 1
                                if x["kind"] == "stumped":
                                    wickets[fielder]["stumped"] += 1
                            except:
                                pass
    try:
        innings4 = dict["innings"][3]["4th innings"]["deliveries"]
    except:
        flag = True
    else:
        for ball in innings4:
            for delivery in ball:

                if "wicket" in ball[delivery]:
                    if "kind" in ball[delivery]["wicket"]:
                        try:
                            fielder = ball[delivery]["wicket"]["fielders"][0]
                            if fielder not in wickets:
                                wickets[fielder] = {}
                                wickets[fielder]["caught"] = 0
                                wickets[fielder]["run_out"] = 0
                                wickets[fielder]["stumped"] = 0
                            if "caught" in ball[delivery]["wicket"]["kind"]:
                                wickets[fielder]["caught"] += 1
                            if ball[delivery]["wicket"]["kind"] == "run out":
                                wickets[fielder]["run_out"] += 1
                            if ball[delivery]["wicket"]["kind"] == "stumped":
                                wickets[fielder]["stumped"] += 1
                        except:
                            pass
                    else:
                        for x in ball[delivery]["wicket"]:
                            try:
                                fielder = x["fielders"][0]
                                if fielder not in wickets:
                                    wickets[fielder] = {}
                                    wickets[fielder]["caught"] = 0
                                    wickets[fielder]["run_out"] = 0
                                    wickets[fielder]["stumped"] = 0
                                if "caught" in x["kind"]:
                                    wickets[fielder]["caught"] += 1
                                if x["kind"] == "run out":
                                    wickets[fielder]["run_out"] += 1
                                if x["kind"] == "stumped":
                                    wickets[fielder]["stumped"] += 1
                            except:
                                pass

    return match_details, wickets


def func(gender, location, formats, matchid_mapping):
    location_runouts = os.path.join(
        "data", "raw", "additional_data", "runouts_with_cricsheet_id.csv"
    )

    df = pd.read_csv(location_runouts)
    indirect_runouts = df["player_2_cricsheet_name"].notna().sum()
    total_runouts = df["player_1_cricsheet_name"].notna().sum()
    direct_runouts = total_runouts - indirect_runouts

    files = pd.read_csv(location)
    grouped = files.groupby("format")

    j = -1
    for format in formats:
        if format[0] == "W":
            form = format[1:]
        else:
            form = format
        date_file_pair = (grouped.get_group(form))["filename"]

        overall_fielding_details = pd.DataFrame(
            columns=["caught", "runouts", "stumped", "innings"]
        )

        player_fielding = pd.DataFrame(
            columns=[
                "date",
                "player_name",
                "player_id",
                "venue_name",
                "previous_innings_fielded",
                "match_id",
                "match_catches",
                "match_runouts",
                "match_stumpings",
                "match_fantasy_points",
                "previous_catches",
                "previous_runouts",
                "previous_stumpings",
                "pFa_catches",
                "pFa_stumpings",
                "pFa_runouts",
                "venue_catches",
                "venue_runouts",
                "venue_stumpings",
                "venue_innings",
            ]
        )

        player_highest_score = {}
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

            match_details, wickets = extract_details(location)

            temp = {}
            temp["caught"] = 0
            temp["run_out"] = 0
            temp["stumped"] = 0
            venue = match_details["venue"]
            for player, outs in wickets.items():
                player = player.replace(" (sub)", "")
                count += 1
                try:
                    overall_fielding_details.index.get_loc(player)
                except:

                    overall_fielding_details.loc[player, "caught"] = 0
                    overall_fielding_details.loc[player, "runouts"] = 0
                    overall_fielding_details.loc[player, "stumped"] = 0
                    overall_fielding_details.loc[player, "innings"] = 0

                player_fielding.loc[count, "date"] = match_details["date"]
                player_fielding.loc[count, "player_name"] = player
                player_fielding.loc[count, "venue_name"] = match_details["venue"]
                player_fielding.loc[count, "match_id"] = i

                player_fielding.loc[
                    count, "previous_catches"
                ] = overall_fielding_details.loc[player, "caught"]
                player_fielding.loc[
                    count, "previous_runouts"
                ] = overall_fielding_details.loc[player, "runouts"]
                player_fielding.loc[
                    count, "previous_stumpings"
                ] = overall_fielding_details.loc[player, "stumped"]
                player_fielding.loc[
                    count, "previous_innings_fielded"
                ] = overall_fielding_details.loc[player, "innings"]

                player_fielding.loc[count, "match_catches"] = outs["caught"]
                player_fielding.loc[count, "match_runouts"] = outs["run_out"]
                player_fielding.loc[count, "match_stumpings"] = outs["stumped"]
                player_fielding.loc[count, "match_fantasy_points"] = (
                    8 * player_fielding.loc[count, "match_catches"]
                    + 12 * player_fielding.loc[count, "match_stumpings"]
                    + (4 if player_fielding.loc[count, "match_catches"] >= 3 else 0)
                    + round(
                        (
                            12 * direct_runouts / total_runouts
                            + 6 * indirect_runouts / total_runouts
                        )
                        * player_fielding.loc[count, "match_runouts"]
                    )
                )

                player_fielding.loc[count, "pFa_catches"] = (
                    (
                        overall_fielding_details.loc[player, "caught"]
                        / overall_fielding_details.loc[player, "innings"]
                    )
                    if overall_fielding_details.loc[player, "innings"] != 0
                    else 0
                )
                player_fielding.loc[count, "pFa_stumpings"] = (
                    (
                        overall_fielding_details.loc[player, "stumped"]
                        / overall_fielding_details.loc[player, "innings"]
                    )
                    if overall_fielding_details.loc[player, "innings"] != 0
                    else 0
                )
                player_fielding.loc[count, "pFa_runouts"] = (
                    (
                        overall_fielding_details.loc[player, "runouts"]
                        / overall_fielding_details.loc[player, "innings"]
                    )
                    if overall_fielding_details.loc[player, "innings"] != 0
                    else 0
                )

                # PREVIOUS DATA
                if venue not in venue_dict:
                    venue_dict[venue] = {}
                    venue_dict[venue]["caught"] = 0
                    venue_dict[venue]["run_out"] = 0
                    venue_dict[venue]["stumped"] = 0
                    venue_dict[venue]["innings"] = 0

                player_fielding.loc[count, "venue_innings"] = venue_dict[venue][
                    "innings"
                ]
                player_fielding.loc[count, "venue_catches"] = venue_dict[venue][
                    "caught"
                ]
                player_fielding.loc[count, "venue_runouts"] = venue_dict[venue][
                    "run_out"
                ]
                player_fielding.loc[count, "venue_stumpings"] = venue_dict[venue][
                    "stumped"
                ]

                overall_fielding_details.loc[player, "caught"] += outs["caught"]
                overall_fielding_details.loc[player, "runouts"] += outs["run_out"]
                overall_fielding_details.loc[player, "stumped"] += outs["stumped"]
                overall_fielding_details.loc[player, "innings"] += 1

                temp["caught"] += outs["caught"]
                temp["run_out"] += outs["run_out"]
                temp["stumped"] += outs["stumped"]

            venue_dict[venue]["caught"] += temp["caught"]
            venue_dict[venue]["run_out"] += temp["run_out"]
            venue_dict[venue]["stumped"] += temp["stumped"]
            venue_dict[venue]["innings"] += 1

        # UNCOMMENT TO ADD IDS
        location = os.path.join(
            "data", "raw", "additional_data", "people_with_images_and_countries.csv"
        )
        mapping = pd.read_csv(location)

        for i in range(len(player_fielding)):
            name = player_fielding.iloc[i]["player_name"]

            matched = mapping[mapping["unique_name"] == name]

            if not matched.empty:
                player_fielding.iloc[
                    i, player_fielding.columns.get_loc("player_id")
                ] = matched["identifier"].values[0]
            else:
                # print(f"No matching entry for {name}: {len(mapping[mapping['unique_name'] == name])} matches")
                player_fielding.iloc[
                    i, player_fielding.columns.get_loc("player_id")
                ] = "xxxxxxxx"

        folder = os.path.join("data", "processed", format)
        os.makedirs(folder, exist_ok=True)
        file_name = "fielder.csv"
        player_fielding.to_csv(os.path.join(folder, file_name))

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
