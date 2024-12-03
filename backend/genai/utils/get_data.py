import players.utils.player_service as player_service
from genai.utils.db import db

db = db()


def batter_data(player_name, date, model, player_opponents, player_type):
    player_data = player_service.get_player_data(player_name, date, model)
    matchups = (
        db["matchup"][model.upper()]
        .objects.filter(
            batsman_name=player_name, bowler_name__in=player_opponents, date__lt=date
        )
        .order_by("-date")
        .values(
            "bowler_name",
            "runs",
            "previous_runs",
            "previous_wickets",
            "previous_avg_strike_rate",
            "previous_innings_head_to_head",
            "previous_4s",
            "previous_6s",
        )
        .first()
    )

    matchups_data = list(matchups)
    data = {
        "player_name": player_name,
        "player_type": player_type,
        "bowlerwise_matchups": matchups_data,
        "fielding_stats": {
            "catches_per_game": player_data["fielding"]["pfa_catches"],
            "runouts_per_game": player_data["fielding"]["pfa_runouts"],
            "stumpings_per_game": player_data["fielding"]["pfa_stumpings"],
        },
        "batter_indices": {
            "consistency": player_data["batting"]["consistency"],
            "venue": player_data["batting"]["venue"],
            "form": player_data["batting"]["form"],
            "opposition": player_data["batting"]["opposition"],
        },
        "historical_data": {
            "total_runs": player_data["batting"]["previous_runs"],
            "total_matches": player_data["batting"]["innings_played"],
            "total_fifties": player_data["batting"]["previous_fifties"],
            "total_hundreds": player_data["batting"]["previous_centuries"],
            "highest_score": player_data["batting"]["highest_score"],
            "average": player_data["batting"]["previous_average"],
            "average_against_spin": player_data["batting"]["tbahs_economy_agg"] * 100,
            "strike_rate_against_spin": player_data["batting"]["previous_strike_rate"]
            * player_data["batting"]["tbahr_economy_agg"],
            "strike_rate_against_pace": player_data["batting"]["previous_strike_rate"]
            / player_data["batting"]["tbahp_economy_agg"],
            "average_against_pace": player_data["batting"]["tbahp_economy_agg"] * 100,
            "career_strike_rate": player_data["batting"]["previous_strike_rate"],
            "boundary_percentage": (
                (
                    player_data["batting"]["previous_4s"]
                    + player_data["batting"]["previous_6s"]
                )
                / player_data["batting"]["previous_balls"]
            )
            * 100,
        },
    }

    return data


def bowler_data(player_name, date, model, player_opponents, player_type):
    player_data = player_service.get_player_data(player_name, date, model)
    matchups = (
        db["matchup"][model.upper()]
        .objects.filter(
            bowler_name=player_name, batsman_name__in=player_opponents, date__lt=date
        )
        .order_by("-date")
        .values(
            "batsman_name",
            "runs",
            "previous_runs",
            "previous_wickets",
            "previous_avg_strike_rate",
            "previous_innings_head_to_head",
            "previous_4s",
            "previous_6s",
        )
        .first()
    )

    matchups_data = list(matchups)

    data = {
        "player_name": player_name,
        "player_type": player_type,
        "bowlerwise_matchups": matchups_data,
        "fielding_stats": {
            "catches_per_game": player_data["fielding"]["pfa_catches"],
            "runouts_per_game": player_data["fielding"]["pfa_runouts"],
            "stumpings_per_game": player_data["fielding"]["pfa_stumpings"],
        },
        "bowler_indices": {
            "consistency": player_data["bowling"]["consistency"],
            "venue": player_data["bowling"]["venue"],
            "form": player_data["bowling"]["form"],
            "opposition": player_data["bowling"]["opposition"],
        },
        "historical_data": {
            "total_wickets": player_data["bowling"]["previous_wickets"],
            "total_matches": player_data["bowling"]["innings_played"],
            "average": player_data["bowling"]["previous_average"],
            "economy_rate": player_data["bowling"]["previous_economy"],
            "strike_rate": player_data["bowling"]["previous_strike_rate"],
        },
    }

    return data


def allrounder_data(player_name, date, model, player_opponents, player_type):
    data = []
    data.append(batter_data(player_name, date, model, player_opponents, player_type))
    data.append(bowler_data(player_name, date, model, player_opponents, player_type))
    return data


def wicketkeeper_data(player_name, date, model, player_opponents, player_type):
    player_data = player_service.get_player_data(player_name, date, model)
    matchups = (
        db["matchup"][model.upper()]
        .objects.filter(
            batsman_name=player_name, bowler_name__in=player_opponents, date__lt=date
        )
        .order_by("-date")
        .values(
            "bowler_name",
            "runs",
            "previous_runs",
            "previous_wickets",
            "previous_avg_strike_rate",
            "previous_innings_head_to_head",
            "previous_4s",
            "previous_6s",
        )
        .first()
    )

    matchups_data = list(matchups)

    data = {
        "player_name": player_name,
        "player_type": "Wicketkeeper",
        "bowlerwise_matchups": matchups_data,
        "fielding_stats": {
            "catches_per_game": player_data["fielding"]["pfa_catches"],
            "runouts_per_game": player_data["fielding"]["pfa_runouts"],
            "stumpings_per_game": player_data["fielding"]["pfa_stumpings"],
            "total_stumpings": player_data["fielding"]["total_stumpings"],
            "total_catches": player_data["fielding"]["total_catches"],
        },
        "bowler_indices": {
            "consistency": player_data["bowling"]["consistency"],
            "venue": player_data["bowling"]["venue"],
            "form": player_data["bowling"]["form"],
            "opposition": player_data["bowling"]["opposition"],
        },
        "historical_data": {
            "total_runs": player_data["batting"]["previous_runs"],
            "total_matches": player_data["batting"]["innings_played"],
            "total_fifties": player_data["batting"]["previous_fifties"],
            "total_hundreds": player_data["batting"]["previous_centuries"],
            "highest_score": player_data["batting"]["highest_score"],
            "average": player_data["batting"]["previous_average"],
            "average_against_spin": player_data["batting"]["tbahs_economy_agg"] * 100,
            "strike_rate_against_spin": player_data["batting"]["previous_strike_rate"]
            * player_data["batting"]["tbahr_economy_agg"],
            "strike_rate_against_pace": player_data["batting"]["previous_strike_rate"]
            / player_data["batting"]["tbahp_economy_agg"],
            "average_against_pace": player_data["batting"]["tbahp_economy_agg"] * 100,
            "career_strike_rate": player_data["batting"]["previous_strike_rate"],
            "total_balls_faced": player_data["batting"]["previous_balls"],
            "total_catches_taken": player_data["fielding"]["total_catches"],
            "total_run_outs": player_data["fielding"]["total_runouts"],
            "total_stumpings": player_data["fielding"]["total_stumpings"],
        },
    }


def get_data(player_type, player_name, date, model, player_opponents):
    if player_type == "batter":
        return batter_data(player_name, date, model, player_opponents, player_type)
    elif player_type == "bowler":
        return bowler_data(player_name, date, model, player_opponents, player_type)
    elif player_type == "allrounder":
        return allrounder_data(player_name, date, model, player_opponents, player_type)
    elif player_type == "wicketkeeper":
        return wicketkeeper_data(player_name, date, model, player_opponents, player_type)
