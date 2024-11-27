import random
from datetime import datetime, timedelta
import pandas as pd
import os

player_id = 1
data = []

start_date = datetime(2023, 1, 1)

for i in range(40):
    date = start_date + timedelta(days=random.randint(0, 365))
    previous_runs = random.randint(10, 1000)
    data.append([date.strftime('%Y-%m-%d'), player_id, previous_runs])

df = pd.DataFrame(data, columns=["Date", "Player_ID", "Previous_Runs"])

print(df.head())

output_file_path = 'data/dummy_player_data.csv'

os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

df.to_csv(output_file_path, index=False)

output_file_path
