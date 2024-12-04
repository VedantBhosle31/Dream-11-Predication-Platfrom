import pandas as pd
import numpy as np

# Load the master file (combined.csv)
combined = pd.read_csv("combined.csv")

# Load the fantasy file (fantasy_bowl.csv)
fantasy_bowl = pd.read_csv("fantasy_bowl7.csv")

# Merge based on 'player_id' (combined.csv's 'id' column matches fantasy_bowl.csv's 'player_id')
merged = pd.merge(
    combined,
    fantasy_bowl[["player_id", "matchpoints_avg"]],
    left_on="id",
    right_on="player_id",
    how="left",
)

# Calculate the cost for rows with matchpoints_avg
min_matchpoints = np.nanmin(merged["matchpoints_avg"])
max_matchpoints = np.nanmax(merged["matchpoints_avg"])
merged["cost"] = 7 + (
    6
    * (merged["matchpoints_avg"] - min_matchpoints)
    // (max_matchpoints - min_matchpoints)
)

# Assign random integer score between 7 and 9 to missing 'matchpoints_avg'
merged.loc[merged["matchpoints_avg"].isna(), "cost"] = np.random.randint(
    6, 9, size=merged["matchpoints_avg"].isna().sum()
)

# Drop the redundant 'player_id' column
merged = merged.drop(columns=["player_id"])

# Save the merged file
merged.to_csv("costly72.csv", index=False)

# Print the head of the new combined DataFrame for verification
print(merged.head())
