import os
import pandas as pd

# Define the current working directory
cwd = os.getcwd()

# Initialize a dictionary to store player data for bowlers
bowler_data = {}

# Function to process bowler and fielder files
def process_file(file_path, player_data, file_type):
    try:
        # Read the CSV
        df = pd.read_csv(file_path)

        # Find the column with fantasy match points
        fantasy_column = [col for col in df.columns if "match_fantasy_points" in col]
        if not fantasy_column:
            print(f"No fantasy points column in {file_path}")
            return
        fantasy_column = fantasy_column[0]  # Get the first matching column

        # Iterate over each player and calculate average points
        for _, row in df.iterrows():
            player_name = row.get("player_name", None)
            player_id = row.get("player_id", None).strip()
            fantasy_points = row.get(fantasy_column, None)

            if (
                True
            ):  # if (player_name and player_id and fantasy_points is not None )or True:
                if player_id not in player_data.keys():
                    player_data[player_id] = {
                        "player_name": player_name,
                        "total_points": 0,
                        "matches": 0,
                    }
                player_data[player_id]["total_points"] += fantasy_points
                player_data[player_id]["matches"] += 1

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    # print(len(player_data))


# Traverse the directory for bowler and fielder files
for subdir, dirs, files in os.walk(cwd):
    print(len(bowler_data))
    for file in files:
        print(file)
        if file in ["batter.csv", "bowler.csv", "fielder.csv"]:
            file_path = os.path.join(subdir, file)
            if "bowler" in file:

                process_file(file_path, bowler_data, "bowler")
            elif "fielder" in file:
                process_file(file_path, bowler_data, "fielder")
            elif "batter" in file:
                process_file(file_path, bowler_data, "batter")

# Calculate the average match points for each player (bowler and fielder)
result_bowler_data = []
for player_id, data in bowler_data.items():
    avg_points = data["total_points"] / data["matches"]
    result_bowler_data.append(
        {
            "player_name": data["player_name"],
            "player_id": player_id,
            "matchpoints_avg": avg_points,
        }
    )

# Convert the results into a DataFrame
result_bowler_df = pd.DataFrame(result_bowler_data)

# Sort the results by average points (optional)
# result_bowler_df = result_bowler_df.sort_values(by="matchpoints_avg", ascending=False)

# Save the result to a CSV file
result_bowler_df.to_csv("fantasy_bowl7.csv", index=False)
print(len(result_bowler_data))
# Print the results for verification
print("\nBowler/Fielder Fantasy Points Summary")
print(result_bowler_df.head())
