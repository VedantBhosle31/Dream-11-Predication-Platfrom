from players.utils.fantacy_points import points_calculator
from players.utils.player_service import fetch_all_player_features, player_features
import pickle
import pandas as pd
from ml_app.utils.predictor import feature_columns_dict
import numpy as np

COST_CSV = "ml_app/utils/cost.csv"
PLAYER_CSV = "players/utils/player_names.csv"

# Function to recursively convert numpy types to Python native types
def convert_numpy_types(data):
    if isinstance(data, dict):
        return {key: convert_numpy_types(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_types(item) for item in data]
    elif isinstance(data, (np.int64, np.int32, np.float64, np.float32)):
        return data.item()  # Convert numpy types to native Python types
    else:
        return data

try:
    with open("ml_app/pickle.pkl", "rb") as file:
        pickle = pickle.load(file)
        models = pickle['models']
        scalers = pickle['scalers']
except FileNotFoundError:
    print("Pickle file not found.")
except pickle.UnpicklingError:
    print("Error while loading the pickle file.")

targets = ['runs','4s','6s','strike_rate','economy','wickets','bowledlbw','maidens','runouts', 'catches', 'stumpings']

target_position_dict={
    'runs':'batting',
    '4s':'batting',
    '6s':'batting',
    'strike_rate':'batting',
    'economy':'bowling',
    'wickets':'bowling',
    'bowledlbw':'bowling',
    'maidens':'bowling',
    'runouts':'fielding', 
    'catches':'fielding', 
    'stumpings':'fielding'
}
def predict_for_one(player_stats,format):
    features = player_stats
    predictions = {}
    for target in targets:
        s= 'match_'+target if target in ['runouts', 'catches', 'stumpings'] else format.upper()+'_match_'+target
        model = models[s]
        scaler = scalers[s]
        feature_column= feature_columns_dict[s]
        feature = features[target_position_dict[target]]
        if(feature):
            X = [feature[key] for key in feature.keys() if key in feature_column]
            X = np.array(X).reshape(1,-1)
            X_scaled = scaler.transform(X)
            pred = model.predict(X_scaled)
            predictions[target] = str(pred[0])
        else:
            predictions[target] = ""

    # Calculate fantasy points based on the predictions
    runouts = predictions.get('runouts', 0)
    runs = predictions.get('runs', 0)
    strike_rate = predictions.get('strike_rate', 0)

    try:
        runouts = float(runouts)
        runs = float(runs)
        strike_rate = float(strike_rate)
        boundary_runs = float(predictions.get('4s', 0))
        sixes = float(predictions.get('6s', 0))
        wickets = float(predictions.get('wickets', 0))
        bowled_lbw = float(predictions.get('bowledlbw', 0))
        maidens = float(predictions.get('maidens', 0))
        economy = float(predictions.get('economy', 0))
        catches = float(predictions.get('catches', 0))
        stumpings = float(predictions.get('stumpings', 0))
    except ValueError:
        runouts = 0
        runs = 0
        strike_rate = 100
        boundary_runs = 0
        sixes = 0
        wickets = 0
        bowled_lbw = 0
        maidens = 0
        economy = 0
        catches = 0
        stumpings = 0

    fantasy_points = points_calculator(format=format.upper(), runouts_direct=runouts * 0.58
    ,runouts_indirect=runouts * 0.42, catches=catches, stumpings=stumpings, runs=runs, sixes=sixes, wickets=wickets, bowled_lbw=bowled_lbw, maidens=maidens, economy=economy, strike_rate=strike_rate, boundaries=boundary_runs)
    # fantasy_points = 0
    print(fantasy_points)
    return {"predictions":predictions, "fantasy_points":fantasy_points}

def predict(names,date,format):
    fantasy_points = {}
    predictions = {}
    all_player_stats = fetch_all_player_features(names, date, format)
    cost_df = pd.read_csv(COST_CSV)  # Renaming `cost` to `cost_df`
    player_names_df = pd.read_csv(PLAYER_CSV)

    for name in names:
        fantasy_points[name] = predict_for_one(all_player_stats[name], format)["fantasy_points"]
        predictions[name] = predict_for_one(all_player_stats[name], format)["predictions"]
        # Add player_id, cost, position for each player from cost csv
        player = cost_df[cost_df['cricsheet_name'] == name]
        if player.empty:
            raise ValueError(f"Player '{name}' not found in cost CSV.")  # Handle missing players gracefully


        # Add player_id from player_names.csv
        player2 = player_names_df[player_names_df['cricsheet_name'] == name]
        if player2.empty:
            raise ValueError(f"Player '{name}' not found in player_names CSV.")  # Handle missing players gracefully

        player_id2 = player2['espn_id'].values[0]

        
        player_id = player['id'].values[0]
        player_cost = player['cost'].values[0]  # Use `player_cost` to avoid overwriting `cost_df`
        position = player['position'].values[0]

        # average = all_player_stats[name]['average']

        if position == "Unknown":
            position = "Batter"

        predictions[name]["player_id"] = player_id
        predictions[name]["cost"] = player_cost
        predictions[name]["position"] = position

        predictions[name]["player_id2"] = player_id2
        # predictions[name]["average"] = average
        # print(all_player_stats)


    # Sort the fantasy points in descending order and send the best 11
    fantasy_points = dict(sorted(fantasy_points.items(), key=lambda item: item[1], reverse=True))
    fantasy_points = dict(list(fantasy_points.items())[:11])

    result = {
        "fantasy_points": fantasy_points,
        "predictions": predictions,
    }

    # Convert all numpy types before returning
    return convert_numpy_types(result)


  