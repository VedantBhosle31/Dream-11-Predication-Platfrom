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
        self.model_weights = {}  # To store the weights of all models
        self.big_pickle = {}
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
        elif model_type == 'random_forest':
            params = {
                'n_estimators': 100,
                'max_depth': 10,
                'min_samples_split': 2,
                'min_samples_leaf': 1,
                'max_features': 'sqrt'
            }
        elif model_type == 'gradient_boosting':
            params = {
                'n_estimators': 100,
                'max_depth': 3,
                'learning_rate': 0.1,
                'subsample': 0.8,
                'min_samples_split': 2,
                'min_samples_leaf': 1
            }
        elif model_type == 'lightgbm':
            params = {
                'n_estimators': 100,
                'num_leaves': 31,
                'max_depth': -1,
                'learning_rate': 0.1,
                'subsample': 0.8,
                'colsample_bytree': 0.8
            }
        elif model_type == 'catboost':
            params = {
                'iterations': 100,
                'depth': 6,
                'learning_rate': 0.1,
                'l2_leaf_reg': 3,
                'bootstrap_type': 'Bayesian'
            }

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

        # Store the model weights
        self.model_weights[target_column] = model

        # Store the results
        self.predictions_data[target_column] = {
            'metrics': metrics,
            'model': model,
            'y_test': y_test,
            'y_pred': y_pred
        }
        
        return metrics, model, X_test, y_test, y_pred

    def save_all_models(self, filename="combined_models.pkl"):
        """Save all models into a single .pkl file"""
        with open(filename, 'wb') as f:
            pickle.dump(self.big_pickle, f)

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

            self.big_pickle[player_type] = self.model_weights 
            self.model_weights = {}

        # Save all models after training
        self.save_all_models()

        # Convert the list of predictions to a DataFrame
        predictions_df = pd.DataFrame(all_predictions)

        # Save predictions to CSV
        predictions_df.to_csv('predictions_output.csv', index=False)
        print(f"Predictions saved to 'predictions_output.csv'")
        return predictions_df

# Define file paths and feature/target columns
# Define file paths
data_paths = {
    'odi_batting':"C:/InterIIT Tech 13.0/simple_match_batsman_details_1.csv",
    'odi_bowling': "C:/InterIIT Tech 13.0/bowler_all_data/IT20/match_bowler_details_1_withids.csv",
    'odi_fielding': "C:/InterIIT Tech 13.0/match_fielder_details_1_withids.csv" ,
        'odm_batting': "C:/InterIIT Tech 13.0/simple_match_batsman_details_1.csv",
    'odm_bowling': "C:/InterIIT Tech 13.0/bowler_all_data/IT20/match_bowler_details_1_withids.csv",
    'odm_fielding': "C:/InterIIT Tech 13.0/match_fielder_details_1_withids.csv" ,
        't20_batting': "C:/InterIIT Tech 13.0/simple_match_batsman_details_1.csv",
    't20_bowling': "C:/InterIIT Tech 13.0/bowler_all_data/IT20/match_bowler_details_1_withids.csv",
    't20_fielding':  "C:/InterIIT Tech 13.0/match_fielder_details_1_withids.csv" ,
        'it20_batting': "C:/InterIIT Tech 13.0/simple_match_batsman_details_1.csv",
    'it20_bowling': "C:/InterIIT Tech 13.0/bowler_all_data/IT20/match_bowler_details_1_withids.csv",
    'it20_fielding':  "C:/InterIIT Tech 13.0/match_fielder_details_1_withids.csv" ,
        'test_batting': "C:/InterIIT Tech 13.0/simple_match_batsman_details_1.csv",
    'test_bowling': "C:/InterIIT Tech 13.0/bowler_all_data/IT20/match_bowler_details_1_withids.csv",
    'test_fielding':  "C:/InterIIT Tech 13.0/match_fielder_details_1_withids.csv" ,
        'mdm_batting': "C:/InterIIT Tech 13.0/simple_match_batsman_details_1.csv",
    'mdm_bowling': "C:/InterIIT Tech 13.0/bowler_all_data/IT20/match_bowler_details_1_withids.csv",
    'mdm_fielding': "C:/InterIIT Tech 13.0/match_fielder_details_1_withids.csv" ,
        'wodi_batting': "C:/InterIIT Tech 13.0/simple_match_batsman_details_1.csv",
    'wodi_bowling': "C:/InterIIT Tech 13.0/bowler_all_data/IT20/match_bowler_details_1_withids.csv",
    'wodi_fielding':  "C:/InterIIT Tech 13.0/match_fielder_details_1_withids.csv" ,
        'wt20_batting': "C:/InterIIT Tech 13.0/simple_match_batsman_details_1.csv",
    'wt20_bowling': "C:/InterIIT Tech 13.0/bowler_all_data/IT20/match_bowler_details_1_withids.csv",
    'wt20_fielding': "C:/InterIIT Tech 13.0/match_fielder_details_1_withids.csv",
        'wtest_batting': "C:/InterIIT Tech 13.0/simple_match_batsman_details_1.csv",
    'wtest_bowling': "C:/InterIIT Tech 13.0/bowler_all_data/IT20/match_bowler_details_1_withids.csv",
    'wtest_fielding':  "C:/InterIIT Tech 13.0/match_fielder_details_1_withids.csv" ,
}

# Define target columns for each player type
target_columns_dict = {
    # ODI statistics
    'odi_batting': ['runs', '4s', '6s', 'strike_rate'],
    'odi_bowling': ['IT20_match_wickets', 'IT20_match_bowledlbw', 'IT20_match_economy', 'IT20_match_maidens'],
    'odi_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # ODM statistics (domestic or other format)
    'odm_batting': ['runs', '4s', '6s', 'strike_rate'],
    'odm_bowling': ['IT20_match_wickets', 'IT20_match_bowledlbw', 'IT20_match_economy', 'IT20_match_maidens'],
    'odm_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # T20 statistics
    't20_batting':['runs', '4s', '6s', 'strike_rate'],
    't20_bowling': ['IT20_match_wickets', 'IT20_match_bowledlbw', 'IT20_match_economy', 'IT20_match_maidens'],
    't20_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # IT20 statistics (could refer to domestic T20 leagues or other T20 formats)
    'it20_batting': ['runs', '4s', '6s', 'strike_rate'],
    'it20_bowling': ['IT20_match_wickets', 'IT20_match_bowledlbw', 'IT20_match_economy', 'IT20_match_maidens'],
    'it20_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # Test match statistics
    'test_batting': ['runs', '4s', '6s', 'strike_rate'],
    'test_bowling': ['IT20_match_wickets', 'IT20_match_bowledlbw', 'IT20_match_economy', 'IT20_match_maidens'],
    'test_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # MDM statistics
    'mdm_batting': ['runs', '4s', '6s', 'strike_rate'],
    'mdm_bowling': ['IT20_match_wickets', 'IT20_match_bowledlbw', 'IT20_match_economy', 'IT20_match_maidens'],
    'mdm_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # Women's ODI statistics
    'wodi_batting':['runs', '4s', '6s', 'strike_rate'] ,
    'wodi_bowling': ['IT20_match_wickets', 'IT20_match_bowledlbw', 'IT20_match_economy', 'IT20_match_maidens'],
    'wodi_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # Women's T20I statistics
    'wt20_batting': ['runs', '4s', '6s', 'strike_rate'],
    'wt20_bowling': ['IT20_match_wickets', 'IT20_match_bowledlbw', 'IT20_match_economy', 'IT20_match_maidens'],
    'wt20_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
    
    # Women's Test statistics
    'wtest_batting': ['runs', '4s', '6s', 'strike_rate'],
    'wtest_bowling': ['IT20_match_wickets', 'IT20_match_bowledlbw', 'IT20_match_economy', 'IT20_match_maidens'],
    'wtest_fielding': ['match_runouts', 'match_catches', 'match_stumpings'],
}


# Define feature columns for each target
feature_columns_dict = {
    'runs':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '4s':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'IT20_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'IT20_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'IT20_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'IT20_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'match_catches': ['previous_catches', 'pFa_catches','venue_catches'],
    'match_runouts': ['previous_runouts', 'pFa_runouts','venue_runouts'],
    'match_stumpings' : ['previous_stumpings','pFa_stumpings','venue_stumpings'],

    'runs':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '4s':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'IT20_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'IT20_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'IT20_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'IT20_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'match_catches': ['previous_catches', 'pFa_catches','venue_catches'],
    'match_runouts': ['previous_runouts', 'pFa_runouts','venue_runouts'],
    'match_stumpings' : ['previous_stumpings','pFa_stumpings','venue_stumpings'],

    'runs':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '4s':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'IT20_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'IT20_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'IT20_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'IT20_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'match_catches': ['previous_catches', 'pFa_catches','venue_catches'],
    'match_runouts': ['previous_runouts', 'pFa_runouts','venue_runouts'],
    'match_stumpings' : ['previous_stumpings','pFa_stumpings','venue_stumpings'],

    'runs':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '4s':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'IT20_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'IT20_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'IT20_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'IT20_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'match_catches': ['previous_catches', 'pFa_catches','venue_catches'],
    'match_runouts': ['previous_runouts', 'pFa_runouts','venue_runouts'],
    'match_stumpings' : ['previous_stumpings','pFa_stumpings','venue_stumpings'],

    'runs':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '4s':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'IT20_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'IT20_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'IT20_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'IT20_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'match_catches': ['previous_catches', 'pFa_catches','venue_catches'],
    'match_runouts': ['previous_runouts', 'pFa_runouts','venue_runouts'],
    'match_stumpings' : ['previous_stumpings','pFa_stumpings','venue_stumpings'],

    'runs':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '4s':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'IT20_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'IT20_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'IT20_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'IT20_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'match_catches': ['previous_catches', 'pFa_catches','venue_catches'],
    'match_runouts': ['previous_runouts', 'pFa_runouts','venue_runouts'],
    'match_stumpings' : ['previous_stumpings','pFa_stumpings','venue_stumpings'],

    'runs':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '4s':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'IT20_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'IT20_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'IT20_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'IT20_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'match_catches': ['previous_catches', 'pFa_catches','venue_catches'],
    'match_runouts': ['previous_runouts', 'pFa_runouts','venue_runouts'],
    'match_stumpings' : ['previous_stumpings','pFa_stumpings','venue_stumpings'],

    'runs':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '4s':['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    '6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s', 'highest_score','consistency','form','opposition','venue'],
    'IT20_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'IT20_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'IT20_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'IT20_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'match_catches': ['previous_catches', 'pFa_catches','venue_catches'],
    'match_runouts': ['previous_runouts', 'pFa_runouts','venue_runouts'],
    'match_stumpings' : ['previous_stumpings','pFa_stumpings','venue_stumpings'],
}

# Example Usage
predictor = PerformancePredictor(data_paths, target_columns_dict, feature_columns_dict)

# Train and evaluate the models and save predictions to CSV
predictions_df = predictor.run_training(model_type='xgboost')
