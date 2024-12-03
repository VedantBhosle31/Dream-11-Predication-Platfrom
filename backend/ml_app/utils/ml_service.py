from players.utils.fantacy_points import points_calculator
from players.utils.player_service import fetch_all_player_features, player_features
import pickle
import pandas as pd
from ml_app.utils.predictor import feature_columns_dict
import numpy as np

try:
    with open("ml_app/pickles/models.pkl", "rb") as file:
        models = pickle.load(file)
except FileNotFoundError:
    print("Pickle file not found.")
except pickle.UnpicklingError:
    print("Error while loading the pickle file.")

try:
    with open("ml_app/pickles/scalers.pkl", "rb") as file:
        scalers = pickle.load(file)
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

    # fantasy_points = points_calculator(format=format, runouts_direct=runouts * 0.58
    # ,runouts_indirect=runouts * 0.42, catches=catches, stumpings=stumpings, runs=runs, sixes=sixes, wickets=wickets, bowled_lbw=bowled_lbw, maidens=maidens, economy=economy, strike_rate=strike_rate, boundaries=boundary_runs)
    fantasy_points = 0
    print(fantasy_points)
    return {"predictions":predictions, "fantasy_points":fantasy_points}

def predict(names,date,format):
    fantasy_points={}
    predictions = {}
    all_player_stats = fetch_all_player_features(names.split(','),date,format)
    for name in names:
        fantasy_points[name] = predict_for_one(name,date,format)["fantasy_points"]
        predictions[name] = predict_for_one(all_player_stats[name],format)["predictions"]
    
    # Sort the fantasy points in descending order and send best 11
    fantasy_points = dict(sorted(fantasy_points.items(), key=lambda item: item[1], reverse=True))
    fantasy_points = dict(list(fantasy_points.items())[:11])
    # return fantasy_points
    return {"fantasy_points":fantasy_points, "predictions":predictions}

  