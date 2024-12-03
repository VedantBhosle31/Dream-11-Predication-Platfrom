from players.utils.player_service import player_features
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
def predict_for_one(name,date,format):
    features = player_features(name,date,format.capitalize())
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
    print(predictions)
    return predictions

def predict(names,date,format):
    predictions={}
    for name in names.split(','):
        predictions[name] = predict_for_one(name,date,format)
    return predictions

        


    
    