import pandas as pd

def validate_uploaded_csv(file, players_csv_path, teams_csv_path):
    errors = []
    uploaded_df = pd.read_csv(file)


    try:
        # Load reference data
        players_df = pd.read_csv(players_csv_path)
        teams_df = pd.read_csv(teams_csv_path)

        # Combine all player name variations into a single set
        name_columns_players = ["name","full_name","display_name","cricsheet_name","cricsheet_unique_name"]
        valid_players = set()
        for col in name_columns_players:
            if col in players_df.columns:
                valid_players.update(players_df[col].dropna().str.strip())
        
        name_columns_teams = []
        valid_teams = set()
        for col in name_columns_teams:
            if col in teams_df.columns:
                valid_teams.update(players_df[col].dropna().str.strip())



        # Validate each row in the uploaded CSV
        for index, row in uploaded_df.iterrows():
            player_name = row.get("Player Name", "").strip()
            team_name = row.get("Squad", "").strip()
            match_date = row.get("Match Date", "").strip()

            if not player_name or not team_name or not match_date:
                errors.append(f"Row {index + 1}: Missing player name, team, or match date.")
                continue

            if team_name not in valid_teams:
                errors.append(f"Row {index + 1}: Team '{team_name}' does not exist.")

            if player_name not in valid_players:
                errors.append(f"Row {index + 1}: Player '{player_name}' does not exist.")

        # Additional checks
        if not errors:
            # Ensure exactly 22 players
            if len(uploaded_df) != 22:
                errors.append(f"Expected 22 players, but got {len(uploaded_df)}.")

            # Ensure only 2 teams are represented
            unique_teams = uploaded_df['Squad'].str.strip().unique()
            if len(unique_teams) != 2:
                errors.append(f"Expected players from exactly 2 teams, but got {len(unique_teams)} teams: {', '.join(unique_teams)}.")

            # Ensure all match dates are the same
            unique_dates = uploaded_df['Match Date'].str.strip().unique()
            if len(unique_dates) != 1:
                errors.append(f"All players must have the same match date, but got multiple dates: {', '.join(unique_dates)}.")

    except Exception as e:
        errors.append(f"Error processing file: {str(e)}")

    return errors