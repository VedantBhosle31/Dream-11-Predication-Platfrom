import pandas as pd
import numpy as np
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

class PerformancePredictor:
    def __init__(self, data_paths, target_columns_dict, feature_columns_dict):
        self.data_paths = data_paths  # Dictionary of CSV file paths
        self.target_columns_dict = target_columns_dict  # Dictionary of target columns for each player type
        self.feature_columns_dict = feature_columns_dict  # Dictionary of feature columns for each target column
        self.results = []  # To store results for HTML and CSV reports
        self.predictions_data = {}  # To store predictions and models for each target
        self.models = {}  # To store the weights of all models
        self.scalers = {}
        os.makedirs('plots', exist_ok=True)  # Create directory for plots

    def preprocess_data(self, target_column, data):
        """Preprocess data by selecting features for the target column"""
        feature_columns = self.feature_columns_dict.get(target_column)
        if not feature_columns:
            raise ValueError(f"No feature columns defined for target column: {target_column}")
        
        # Select features and target column
        X = data[feature_columns]
        y = data[target_column]
        
        return X, y

    def create_model(self, model_type, params):
        """Create a model based on the selected type"""
        if model_type == 'xgboost':
            return XGBRegressor(tree_method='gpu_hist', **params)
        elif model_type == 'random_forest':
            return RandomForestRegressor(**params)
        elif model_type == 'gradient_boosting':
            return GradientBoostingRegressor(**params)
        elif model_type == 'lightgbm':
            return LGBMRegressor(device='gpu', **params)
        elif model_type == 'catboost':
            return CatBoostRegressor(task_type="GPU", verbose=0, **params)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    def train_and_evaluate_model(self, model_type, data, target_column):
        """Train and evaluate a model without optimization"""
        # Preprocess data for the target column
        X, y = self.preprocess_data(target_column, data)
        # Split data into train and test sets (20% test data)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Standardize the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scaler_model = scaler

        # Define default hyperparameters
        if model_type == 'xgboost':
            params = {
                'n_estimators': 100,
                'max_depth': 6,
                'learning_rate': 0.1,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'reg_alpha': 0.1,
                'reg_lambda': 0.1
            }
        # elif model_type == 'random_forest':
        #     params = {
        #         'n_estimators': 100,
        #         'max_depth': 10,
        #         'min_samples_split': 2,
        #         'min_samples_leaf': 1,
        #         'max_features': 'sqrt'
        #     }
        # elif model_type == 'gradient_boosting':
        #     params = {
        #         'n_estimators': 100,
        #         'max_depth': 3,
        #         'learning_rate': 0.1,
        #         'subsample': 0.8,
        #         'min_samples_split': 2,
        #         'min_samples_leaf': 1
        #     }
        # elif model_type == 'lightgbm':
        #     params = {
        #         'n_estimators': 100,
        #         'num_leaves': 31,
        #         'max_depth': -1,
        #         'learning_rate': 0.1,
        #         'subsample': 0.8,
        #         'colsample_bytree': 0.8
        #     }
        # elif model_type == 'catboost':
        #     params = {
        #         'iterations': 100,
        #         'depth': 6,
        #         'learning_rate': 0.1,
        #         'l2_leaf_reg': 3,
        #         'bootstrap_type': 'Bayesian'
        #     }

        # Create the model using the predefined hyperparameters
        model = self.create_model(model_type, params)
        
        # Train the model
        model.fit(X_train_scaled, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test_scaled)
        metrics = {
            'MSE': mean_squared_error(y_test, y_pred),
            'MAE': mean_absolute_error(y_test, y_pred),
            'R2': r2_score(y_test, y_pred)
        }

        # Store the model for respective target
        self.models[target_column] = model
        self.scalers[target_column] = scaler

        # Store the results
        self.predictions_data[target_column] = {
            'metrics': metrics,
            'model': model,
            'y_test': y_test,
            'y_pred': y_pred
        }
        
        return metrics, model, X_test, y_test, y_pred

    def save_all_models(self):
        """Save all models into a single .pkl file"""
        with open('pickles/models.pkl', 'wb') as f:
            pickle.dump(self.models, f)
        with open('pickles/scalers.pkl','wb') as f:
            pickle.dump(self.scalers,f)

    def run_training(self, model_type='xgboost'):
        all_predictions = []  # List to hold all predictions for CSV output

        for player_type, data_path in self.data_paths.items():
            data = pd.read_csv(data_path)
            target_columns = self.target_columns_dict[player_type]  # Get target columns for current player type
            
            for target_column in target_columns:
                print(f"Training model for target: {target_column} in {player_type}")
                metrics, model, X_test, y_test, y_pred = self.train_and_evaluate_model(model_type, data, target_column)
                
                # Store the actual and predicted values in a list for CSV export
                for true_value, predicted_value in zip(y_test, y_pred):
                    all_predictions.append({
                        'target_column': target_column,
                        'true_value': true_value,
                        'predicted_value': predicted_value
                    })
        print(self.scalers)
        print(self.models)

        # Save all models after training
        self.save_all_models()

        # Convert the list of predictions to a DataFrame
        predictions_df = pd.DataFrame(all_predictions)

        # Save predictions to CSV
        predictions_df.to_csv('predictions_output.csv', index=False)
        print(f"Predictions saved to 'predictions_output.csv'")
        return predictions_df
    
    # def predict(self,X,format):
    #     targets = ['runs','4s','6s','strike_rate','economy','wickets','bowledlbw','maidens','runouts', 'catches', 'stumpings']
    #     prediction_dict = {}
    #     for target in targets:
    #         model = self.models[format+'_match_'+target]
    #         scaler = self.scalers[format+'_match_'+target]
    #         pred = model.predict(scaler.transform(X[self.feature_columns_dict[format+'_match_'+target]]))
    #         prediction_dict[target] = pred
    #     return prediction_dict
        

# Define file paths and feature/target columns
# Define file paths
data_paths = {
    'ODI_batting':"all_data_final/all_data_final/ODI/batter.csv",
    'ODI_bowling':"all_data_final/all_data_final/ODI/bowler.csv",
    'ODI_fielding': "all_data_final/all_data_final/ODI/fielder.csv" ,
        'ODM_batting': "all_data_final/all_data_final/ODM/batter.csv",
    'ODM_bowling':"all_data_final/all_data_final/ODM/bowler.csv",
    'ODM_fielding': "all_data_final/all_data_final/ODM/fielder.csv" ,
        'T20_batting': "all_data_final/all_data_final/T20/batter.csv",
    'T20_bowling':"all_data_final/all_data_final/T20/bowler.csv",
    'T20_fielding':  "all_data_final/all_data_final/T20/fielder.csv" ,
        'IT20_batting': "all_data_final/all_data_final/IT20/batter.csv",
    'IT20_bowling':"all_data_final/all_data_final/IT20/bowler.csv",
    'IT20_fielding':  "all_data_final/all_data_final/IT20/fielder.csv",
        'Test_batting': "all_data_final/all_data_final/Test/batter.csv",
    'Test_bowling':"all_data_final/all_data_final/Test/bowler.csv",
    'Test_fielding':  "all_data_final/all_data_final/Test/fielder.csv",
        'MDM_batting': "all_data_final/all_data_final/MDM/batter.csv",
    'MDM_bowling':"all_data_final/all_data_final/MDM/bowler.csv",
    'MDM_fielding':"all_data_final/all_data_final/MDM/fielder.csv" ,
        'WODI_batting':"all_data_final/all_data_final/WODI/batter.csv",
    'WODI_bowling':"all_data_final/all_data_final/WODI/bowler.csv",
    'WODI_fielding':  "all_data_final/all_data_final/WODI/fielder.csv" ,
        'WT20_batting': "all_data_final/all_data_final/WT20/batter.csv",
    'WT20_bowling':"all_data_final/all_data_final/WT20/bowler.csv",
    'WT20_fielding': "all_data_final/all_data_final/WT20/fielder.csv",
        'WTest_batting': "all_data_final/all_data_final/WTest/batter.csv",
    'WTest_bowling':"all_data_final/all_data_final/WTest/bowler.csv",
    'WTest_fielding': "all_data_final/all_data_final/WTest/fielder.csv",
            'WODM_batting': "all_data_final/all_data_final/WODM/batter.csv",
    'WODM_bowling':"all_data_final/all_data_final/WODM/bowler.csv",
    'WODM_fielding': "all_data_final/all_data_final/WODM/fielder.csv",
            'WIT20_batting': "all_data_final/all_data_final/WIT20/batter.csv",
    'WIT20_bowling':"all_data_final/all_data_final/WIT20/bowler.csv",
    'WIT20_fielding':"all_data_final/all_data_final/WIT20/fielder.csv"
}

# Define target columns for each player type
target_columns_dict = {
    # ODI statistics
    'ODI_batting': ['ODI_match_runs', 'ODI_match_4s', 'ODI_match_6s', 'ODI_match_strike_rate'],
    'ODI_bowling': ['ODI_match_wickets', 'ODI_match_bowledlbw', 'ODI_match_economy', 'ODI_match_maidens'],
    'ODI_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # ODM statistics (domestic or other format)
    'ODM_batting': ['ODM_match_runs', 'ODM_match_4s', 'ODM_match_6s', 'ODM_match_strike_rate'],
    'ODM_bowling': ['ODM_match_wickets', 'ODM_match_bowledlbw', 'ODM_match_economy', 'ODM_match_maidens'],
    'ODM_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # T20 statistics
    'T20_batting':['T20_match_runs', 'T20_match_4s', 'T20_match_6s', 'T20_match_strike_rate'],
    'T20_bowling': ['T20_match_wickets', 'T20_match_bowledlbw', 'T20_match_economy', 'T20_match_maidens'],
    'T20_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # IT20 statistics (could refer to domestic T20 leagues or other T20 formats)
    'IT20_batting': ['IT20_match_runs', 'IT20_match_4s', 'IT20_match_6s', 'IT20_match_strike_rate'],
    'IT20_bowling': ['IT20_match_wickets', 'IT20_match_bowledlbw', 'IT20_match_economy', 'IT20_match_maidens'],
    'IT20_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # Test match statistics
    'Test_batting': ['Test_match_runs', 'Test_match_4s', 'Test_match_6s', 'Test_match_strike_rate'],
    'Test_bowling': ['Test_match_wickets', 'Test_match_bowledlbw', 'Test_match_economy', 'Test_match_maidens'],
    'Test_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # MDM statistics
    'MDM_batting': ['MDM_match_runs', 'MDM_match_4s', 'MDM_match_6s', 'MDM_match_strike_rate'],
    'MDM_bowling': ['MDM_match_wickets', 'MDM_match_bowledlbw', 'MDM_match_economy', 'MDM_match_maidens'],
    'MDM_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # Women's ODI statistics
    'WODI_batting':['WODI_match_runs', 'WODI_match_4s', 'WODI_match_6s', 'WODI_match_strike_rate'] ,
    'WODI_bowling': ['WODI_match_wickets', 'WODI_match_bowledlbw', 'WODI_match_economy', 'WODI_match_maidens'],
    'WODI_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # Women's T20I statistics
    'WT20_batting': ['WT20_match_runs', 'WT20_match_4s', 'WT20_match_6s', 'WT20_match_strike_rate'],
    'WT20_bowling': ['WT20_match_wickets', 'WT20_match_bowledlbw', 'WT20_match_economy', 'WT20_match_maidens'],
    'WT20_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # Women's Test statistics
    'WTest_batting': ['WTest_match_runs', 'WTest_match_4s', 'WTest_match_6s', 'WTest_match_strike_rate'],
    'WTest_bowling': ['WTest_match_wickets', 'WTest_match_bowledlbw', 'WTest_match_economy', 'WTest_match_maidens'],
    'WTest_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],

    # Women's ODM
    'WODM_batting': ['WODM_match_runs', 'WODM_match_4s', 'WODM_match_6s', 'WODM_match_strike_rate'],
    'WODM_bowling': ['WODM_match_wickets', 'WODM_match_bowledlbw', 'WODM_match_economy', 'WODM_match_maidens'],
    'WODM_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],

        # Women's ODM
    'WIT20_batting': ['WIT20_match_runs', 'WIT20_match_4s', 'WIT20_match_6s', 'WIT20_match_strike_rate'],
    'WIT20_bowling': ['WIT20_match_wickets', 'WIT20_match_bowledlbw', 'WIT20_match_economy', 'WIT20_match_maidens'],
    'WIT20_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
}


# Define feature columns for each target
feature_columns_dict = {
    'ODI_match_runs':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'ODI_match_4s':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'ODI_match_6s': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'ODI_match_strike_rate': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'ODI_match_wickets': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'ODI_match_economy': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'ODI_match_bowledlbw': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'ODI_match_maidens': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],

    'ODM_match_runs':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'ODM_match_4s':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'ODM_match_6s': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'ODM_match_strike_rate': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'ODM_match_wickets': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'ODM_match_economy': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'ODM_match_bowledlbw': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'ODM_match_maidens': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],

    'T20_match_runs':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'T20_match_4s':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'T20_match_6s': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'T20_match_strike_rate': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'T20_match_wickets': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'T20_match_economy': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'T20_match_bowledlbw': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'T20_match_maidens': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],

    'IT20_match_runs':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'IT20_match_4s':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'IT20_match_6s': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'IT20_match_strike_rate': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'IT20_match_wickets': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'IT20_match_economy': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'IT20_match_bowledlbw': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'IT20_match_maidens': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],

    'Test_match_runs':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'Test_match_4s':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'Test_match_6s': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'Test_match_strike_rate': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'Test_match_wickets': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'Test_match_economy': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'Test_match_bowledlbw': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'Test_match_maidens': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],

    'MDM_match_runs':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'MDM_match_4s':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'MDM_match_6s': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'MDM_match_strike_rate': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'MDM_match_wickets': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'MDM_match_economy': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'MDM_match_bowledlbw': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'MDM_match_maidens': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],

    'WODI_match_runs':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WODI_match_4s':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WODI_match_6s': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WODI_match_strike_rate': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WODI_match_wickets': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WODI_match_economy': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WODI_match_bowledlbw': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WODI_match_maidens': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],

    'WTest_match_runs':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WTest_match_4s':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WTest_match_6s': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WTest_match_strike_rate': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WTest_match_wickets': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WTest_match_economy': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WTest_match_bowledlbw': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WTest_match_maidens': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],

    'WT20_match_runs':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WT20_match_4s':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WT20_match_6s': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WT20_match_strike_rate': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WT20_match_wickets': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WT20_match_economy': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WT20_match_bowledlbw':['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WT20_match_maidens': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],

    'WIT20_match_runs':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WIT20_match_4s':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WIT20_match_6s':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WIT20_match_strike_rate': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WIT20_match_wickets':['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WIT20_match_economy': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WIT20_match_bowledlbw': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WIT20_match_maidens': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],

    'WODM_match_runs':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WODM_match_4s':['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WODM_match_6s': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WODM_match_strike_rate': ['venue','innings_played','previous_balls_involved','previous_outs','previous_average',
                           'previous_strike_rate','previous_centuries','previous_thirties','previous_fifties',
                           'previous_zeros','previous_runs','previous_4s','previous_6s','highest_score','opposition',
                           'consistency','form','career_score','recent_score','combined_score',
                           'wvbah_dismissals','wvbah_4s','wvbah_6s','wvbah_economy',
                           'wfbah_dismissals','wfbah_4s','wfbah_6s','wfbah_economy',
                           'wtbah_dismissals','wtbah_4s','wtbah_6s','wtbah_economy'],
    'WODM_match_wickets': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WODM_match_economy': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WODM_match_bowledlbw': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],
    'WODM_match_maidens': ['wvboda_economy', 'wvboda_dismissals', 'wvboda_bowledlbw', 'wvboda_maidens', 
                           'wtboda_economy', 'wtboda_dismissals', 'wtboda_bowledlbw', 'wtboda_maidens',
                            'wfboda_economy', 'wfboda_dismissals', 'wfboda_bowledlbw', 'wfboda_maidens',
                            'innings_played', 'previous_balls_involved', 'previous_wickets', 
                         'previous_average', 'previous_strike_rate', 'previous_economy',
                         'venue_maidens', 'venue_bowledlbw', 'venue_average' ,'venue_economy', 'venue_innings',
                         'previous_3haul', 'previous_5haul','previous_maidens','consistency','form','venue','opposition'],

    'match_catches': ['previous_catches', 'pfa_catches','venue_catches'],
    'match_runouts': ['previous_runouts', 'pfa_runouts','venue_runouts'],
    'match_stumpings' : ['previous_stumpings','pfa_stumpings','venue_stumpings'],
}