import random
from datetime import datetime, timedelta
import pandas as pd
import os

# Base variables
player_id = 1
data_fielding = []

# Start date for random dates
start_date = datetime(2023, 1, 1)

# Generate dummy entries
for i in range(40):
    date = start_date + timedelta(days=random.randint(0, 365))
    fielding = random.randint(0, 80)  # Random numbers for fielding events (e.g., catches or saves)
    matchup = random.randint(1, 100)  # Random numbers for matchup (e.g., matchup IDs)
    data_fielding.append([date.strftime('%Y-%m-%d'), player_id, fielding, matchup])

# Create a DataFrame
df_fielding = pd.DataFrame(data_fielding, columns=["date", "player_id", "fielding", "matchup"])

# Save the data to a CSV file
output_file_fielding_path = 'data/dummy_player_fielding_data.csv'
os.makedirs(os.path.dirname(output_file_fielding_path), exist_ok=True)
df_fielding.to_csv(output_file_fielding_path, index=False)

print(f"File saved to: {output_file_fielding_path}")
