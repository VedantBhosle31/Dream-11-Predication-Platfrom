import random
from datetime import datetime, timedelta
import pandas as pd
import os

player_id = 1

start_date = datetime(2023, 1, 1)
data_bowler = []

for i in range(40):
    date = start_date + timedelta(days=random.randint(0, 365))
    wickets = random.randint(10, 100)  
    economy = round(random.uniform(3.0, 10.0), 2) 
    data_bowler.append([date.strftime('%Y-%m-%d'), player_id, wickets, economy])

df_bowler = pd.DataFrame(data_bowler, columns=["date", "player_id", "wickets", "economy"])

# Save the new data to a CSV file
output_file_bowler_path = 'data/dummy_player_bowler_data.csv'
os.makedirs(os.path.dirname(output_file_bowler_path), exist_ok=True)
df_bowler.to_csv(output_file_bowler_path, index=False)

output_file_bowler_path

