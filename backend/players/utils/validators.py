import pandas as pd
from difflib import get_close_matches

def validate_uploaded_csv(file, players_csv_path, teams_csv_path):
    errors = []
    team_logos = {}
    final_players_unique_names = []

    try:
        # Load the uploaded CSV file
        try:
            uploaded_df = pd.read_csv(file)
            if uploaded_df.empty:
                errors.append("Uploaded file is empty.")
                return {"errors": errors, "team_logos": team_logos, "final_players_unique_names": final_players_unique_names}
        except pd.errors.EmptyDataError:
            errors.append("Uploaded file is empty or invalid.")
            return {"errors": errors, "team_logos": team_logos, "final_players_unique_names": final_players_unique_names}

        # Ensure required columns exist in the uploaded file
        required_columns = {"Player Name", "Squad", "Match Date"}
        missing_columns = required_columns - set(uploaded_df.columns)
        if missing_columns:
            errors.append(f"Uploaded file is missing required columns: {', '.join(missing_columns)}.")
            return {"errors": errors, "team_logos": team_logos, "final_players_unique_names": final_players_unique_names}

        # Load reference data
        try:
            players_df = pd.read_csv(players_csv_path)
            teams_df = pd.read_csv(teams_csv_path)
        except FileNotFoundError as e:
            errors.append(f"Reference file not found: {str(e)}")
            return {"errors": errors, "team_logos": team_logos, "final_players_unique_names": final_players_unique_names}

        # Combine all player name variations into a dictionary with cricsheet_unique_name as the value
        player_name_columns = [
            "name", "full_name", "display_name", "cricsheet_name", "cricsheet_unique_name"
        ]
        valid_players = {}
        for col in player_name_columns:
            if col in players_df.columns:
                for _, row in players_df.iterrows():
                    name = str(row[col]).strip().lower() if pd.notna(row[col]) else None
                    if name:
                        valid_players[name] = row.get("cricsheet_unique_name", name)

        # Function to find the closest match for a player name
        def get_player_unique_name(player_name, valid_players, threshold=0.8):
            player_name = player_name.lower().strip()
            if player_name in valid_players:
                return valid_players[player_name]
            close_matches = get_close_matches(player_name, valid_players.keys(), n=1, cutoff=threshold)
            return valid_players[close_matches[0]] if close_matches else None

        # Prepare valid teams with their logos
        team_name_columns = [
            "name", "nickname", "abbreviation", "display_name", "short_display_name"
        ]
        valid_teams = {}
        for _, row in teams_df.iterrows():
            for col in team_name_columns:
                if col in row and pd.notna(row[col]):
                    valid_teams[row[col].strip().lower()] = row.get("logo", "")

        # Validate each row in the uploaded CSV
        for index, row in uploaded_df.iterrows():
            player_name = str(row.get("Player Name", "")).strip()
            team_name = str(row.get("Squad", "")).strip()
            match_date = str(row.get("Match Date", "")).strip()

            if not player_name or not team_name or not match_date:
                errors.append(f"Row {index + 1}: Missing player name, team, or match date.")
                continue

            if team_name.lower() not in valid_teams:
                errors.append(f"Row {index + 1}: Team '{team_name}' does not exist.")

            unique_name = get_player_unique_name(player_name, valid_players)
            if unique_name:
                final_players_unique_names.append(unique_name)
            else:
                errors.append(f"Row {index + 1}: Player '{player_name}' does not exist.")

        # Additional checks if no row-level errors were found
        if not errors:
            # Ensure exactly 22 players
            if len(uploaded_df) != 22:
                errors.append(f"Expected 22 players, but got {len(uploaded_df)}.")

            # Ensure only 2 teams are represented
            unique_teams = uploaded_df["Squad"].str.strip().str.lower().unique()
            if len(unique_teams) != 2:
                errors.append(f"Expected players from exactly 2 teams, but got {len(unique_teams)} teams: {', '.join(unique_teams)}.")
            else:
                # Get the logos for the two valid teams
                team_logos = [valid_teams[team] for team in unique_teams]

            # Ensure all match dates are the same
            unique_dates = uploaded_df["Match Date"].str.strip().unique()
            if len(unique_dates) != 1:
                errors.append(f"All players must have the same match date, but got multiple dates: {', '.join(unique_dates)}.")

    except Exception as e:
        errors.append(f"Error processing file: {str(e)}")

    return {"errors": errors, "team_logos": team_logos, "final_players_unique_names": final_players_unique_names}
