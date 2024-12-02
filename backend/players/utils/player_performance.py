import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import optuna
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from optuna.pruners import MedianPruner
from optuna.samplers import TPESampler
import os
import base64
import pickle
from io import BytesIO

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')
from fantacy_points import points_calculator

from db import db


db = db()

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

    def get_base64_plot(self):
        """Convert the current matplotlib plot to base64 string"""
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode()

    def preprocess_data(self, target_column, data):
        """Preprocess data by selecting features for the target column"""
        feature_columns = self.feature_columns_dict.get(target_column)
        if not feature_columns:
            raise ValueError(f"No feature columns defined for target column: {target_column}")
        
        # Select features and target column
        X = data[feature_columns][0:20]
        y = data[target_column][0:20]
        
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

    def objective(self, trial, X_train, y_train, model_type, target_column):
        """Define the optimization objective for each model"""
        if model_type == 'xgboost':
            params = {
                'n_estimators': trial.suggest_int('n_estimators', 50, 500),
                'max_depth': trial.suggest_int('max_depth', 3, 12),
                'learning_rate': trial.suggest_loguniform('learning_rate', 1e-4, 1e-1),
                'subsample': trial.suggest_uniform('subsample', 0.5, 1.0),
                'colsample_bytree': trial.suggest_uniform('colsample_bytree', 0.5, 1.0),
                'reg_alpha': trial.suggest_loguniform('reg_alpha', 1e-3, 10.0),
                'reg_lambda': trial.suggest_loguniform('reg_lambda', 1e-3, 10.0)
            }
        elif model_type == 'random_forest':
            params = {
                'n_estimators': trial.suggest_int('n_estimators', 50, 500),
                'max_depth': trial.suggest_int('max_depth', 5, 20),
                'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
                'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
                'max_features': trial.suggest_categorical('max_features', ['auto', 'sqrt', 'log2'])
            }
        elif model_type == 'gradient_boosting':
            params = {
                'n_estimators': trial.suggest_int('n_estimators', 50, 500),
                'max_depth': trial.suggest_int('max_depth', 3, 10),
                'learning_rate': trial.suggest_loguniform('learning_rate', 1e-4, 1e-1),
                'subsample': trial.suggest_uniform('subsample', 0.5, 1.0),
                'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
                'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10)
            }
        elif model_type == 'lightgbm':
            params = {
                'n_estimators': trial.suggest_int('n_estimators', 50, 500),
                'num_leaves': trial.suggest_int('num_leaves', 20, 300),
                'max_depth': trial.suggest_int('max_depth', -1, 15),
                'learning_rate': trial.suggest_loguniform('learning_rate', 1e-4, 1e-1),
                'subsample': trial.suggest_uniform('subsample', 0.5, 1.0),
                'colsample_bytree': trial.suggest_uniform('colsample_bytree', 0.5, 1.0)
            }
        elif model_type == 'catboost':
            params = {
                'iterations': trial.suggest_int('iterations', 100, 500),
                'depth': trial.suggest_int('depth', 4, 10),
                'learning_rate': trial.suggest_loguniform('learning_rate', 1e-4, 1e-1),
                'l2_leaf_reg': trial.suggest_loguniform('l2_leaf_reg', 1e-3, 10.0),
                'bootstrap_type': trial.suggest_categorical('bootstrap_type', ['Bayesian', 'Bernoulli', 'MVS'])
            }
            if params['bootstrap_type'] == 'Bayesian':
                params['bagging_temperature'] = trial.suggest_uniform('bagging_temperature', 0, 10)
            else:
                params['subsample'] = trial.suggest_uniform('subsample', 0.5, 1.0)

        model = self.create_model(model_type, params)
        
        # KFold Cross-Validation
        kf = KFold(n_splits=2, shuffle=True, random_state=42)
        scores = []
        
        for train_idx, val_idx in kf.split(X_train):
            X_kf_train, X_kf_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
            y_kf_train = y_train.iloc[train_idx]
            y_kf_val = y_train.iloc[val_idx]

            scaler = StandardScaler()
            X_kf_train_scaled = scaler.fit_transform(X_kf_train)
            X_kf_val_scaled = scaler.transform(X_kf_val)

            model.fit(X_kf_train_scaled, y_kf_train)
            y_pred = model.predict(X_kf_val_scaled)
            scores.append(mean_squared_error(y_kf_val, y_pred))

        return np.mean(scores)

    def optimize_and_train(self, model_type, data, target_column, n_trials=50):
        """Optimize the model and train on the provided target column"""
    
        # Preprocess data for the target column
        X, y = self.preprocess_data(target_column, data)
        
        # Create an Optuna study
        study = optuna.create_study(
            direction='minimize',
            pruner=MedianPruner(),
            sampler=TPESampler()
        )
        
        # Optimize hyperparameters
        study.optimize(
            lambda trial: self.objective(trial, X, y, model_type, target_column),
            n_trials=n_trials
        )
        
        # Train final model using the best parameters
        best_params = study.best_params
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Standardize the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Create the model using the optimized parameters
        model = self.create_model(model_type, best_params)
        model.fit(X_train_scaled, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test_scaled)
        metrics = {
            'MSE': mean_squared_error(y_test, y_pred),
            'MAE': mean_absolute_error(y_test, y_pred),
            'R2': r2_score(y_test, y_pred)
        }

        # Store the model weights
        self.model_weights[target_column] = model.get_booster().get_dump() if hasattr(model, 'get_booster') else model

        # Store the results
        self.predictions_data[target_column] = {
            'metrics': metrics,
            'model': model
        }
        
        return metrics, model

    def save_all_models(self, filename="combined_models.pkl"):
        """Save all models into a single .pkl file"""
        with open(filename, 'wb') as f:
            pickle.dump(self.big_pickle, f)

    def run_optimization(self, model_type='xgboost'):
        for player_type, data_path in self.data_paths.items():
            data = pd.read_csv(data_path)
            target_columns = self.target_columns_dict[player_type]  # Get target columns for current player type
            for target_column in target_columns:
                print(f"Optimizing model for target: {target_column} in {player_type}")
                metrics, model = self.optimize_and_train(model_type, data, target_column)
                self.predictions_data[target_column] = {
                    'metrics': metrics,
                    'model': model
                }
            self.big_pickle[player_type] = self.model_weights 
            self.model_weights = {}
        self.save_all_models()

    def predict(self, target_column, match_type data):
        """Predict the performance for a given player type and target column"""
        runs_model = self.predictions_data[target_column]['model'].predict(data)
        runs = runs_model.predict()
        boundaries_model = predictor.create_model('xgboost', different_models[f'{match_type}_batting']['4s'])
        boundaries = boundaries_model.predict()
        sixes_model = predictor.create_model('xgboost', different_models[f'{match_type}_batting']['6s'])
        sixes = sixes_model.predict()
        strike_rate_model = predictor.create_model('xgboost', different_models[f'{match_type}_batting']['strike_rate'])
        strike_rate = strike_rate_model.predict()
        wickets_model = predictor.create_model('xgboost', different_models[f'{match_type}_bowling']['IT20_match_wickets'])
        wickets = wickets_model.predict()
        bowled_lbw_model = predictor.create_model('xgboost', different_models[f'{match_type}_bowling']['IT20_match_bowledlbw'])
        bowled_lbw = bowled_lbw_model.predict()
        maidens_model = predictor.create_model('xgboost', different_models[f'{match_type}_bowling']['IT20_match_maidens'])
        maidens = maidens_model.predict()
        economy_model = predictor.create_model('xgboost', different_models[f'{match_type}_bowling']['IT20_match_economy'])
        economy = economy_model.predict()
        catches_model = predictor.create_model('xgboost', different_models[f'{match_type}_fielding']['match_catches'])
        catches = catches_model.predict()
        stumpings_model = predictor.create_model('xgboost', different_models[f'{match_type}_fielding']['match_stumpings'])
        stumpings = stumpings_model.predict()
        runouts_direct_model = predictor.create_model('xgboost', different_models[f'{match_type}_fielding']['match_runouts'])
        runouts_direct = runouts_direct_model.predict()



    
    def inference(self):
    # Unpickle
    # Define i/o to choose model and inputs
    # do model.predict() with that data
        pass

formats = ['odi', 'od','t20i','t20','test','fc','wodi','wt20','wtest']

# Define file paths
data_paths = {
    # ODI Data
    'odi_batting': pd.DataFrame.from_records(db['batter']['ODI'].objects.all().values()),
    'odi_bowling': pd.DataFrame.from_records(db['bowler']['ODI'].objects.all().values()),
    'odi_fielding': pd.DataFrame.from_records(db['fielder']['ODI'].objects.all().values()),
    
    # T20I Data
    't20i_batting': pd.DataFrame.from_records(db['batter']['T20I'].objects.all().values()),
    't20i_bowling': pd.DataFrame.from_records(db['bowler']['T20I'].objects.all().values()),
    't20i_fielding': pd.DataFrame.from_records(db['fielder']['T20I'].objects.all().values()),
    
    # T20 Data
    't20_batting': pd.DataFrame.from_records(db['batter']['T20'].objects.all().values()),
    't20_bowling': pd.DataFrame.from_records(db['bowler']['T20'].objects.all().values()),
    't20_fielding': pd.DataFrame.from_records(db['fielder']['T20'].objects.all().values()),
    
    # Test Data
    'test_batting': pd.DataFrame.from_records(db['batter']['TEST'].objects.all().values()),
    'test_bowling': pd.DataFrame.from_records(db['bowler']['TEST'].objects.all().values()),
    'test_fielding': pd.DataFrame.from_records(db['fielder']['TEST'].objects.all().values()),
    
    # First Class Data
    'fc_batting': pd.DataFrame.from_records(db['batter']['FC'].objects.all().values()),
    'fc_bowling': pd.DataFrame.from_records(db['bowler']['FC'].objects.all().values()),
    'fc_fielding': pd.DataFrame.from_records(db['fielder']['FC'].objects.all().values()),
    
    # Women's ODI Data
    'wodi_batting': pd.DataFrame.from_records(db['batter']['WODI'].objects.all().values()),
    'wodi_bowling': pd.DataFrame.from_records(db['bowler']['WODI'].objects.all().values()),
    'wodi_fielding': pd.DataFrame.from_records(db['fielder']['WODI'].objects.all().values()),
    
    # Women's T20 Data
    'wt20_batting': pd.DataFrame.from_records(db['batter']['WT20'].objects.all().values()),
    'wt20_bowling': pd.DataFrame.from_records(db['bowler']['WT20'].objects.all().values()),
    'wt20_fielding': pd.DataFrame.from_records(db['fielder']['WT20'].objects.all().values()),
    
    # Women's Test Data
    'wtest_batting': pd.DataFrame.from_records(db['batter']['WTEST'].objects.all().values()),
    'wtest_bowling': pd.DataFrame.from_records(db['bowler']['WTEST'].objects.all().values()),
    'wtest_fielding': pd.DataFrame.from_records(db['fielder']['WTEST'].objects.all().values()),
}


# Define target columns for each player type
target_columns_dict = {
    # ODI statistics
    'odi_batting': ['odi_runs', 'odi_4s', 'odi_6s', 'odi_strike_rate'],
    'odi_bowling': ['odi_match_wickets', 'odi_match_bowledlbw', 'odi_match_economy', 'odi_match_maidens'],
    'odi_fielding': ['odi_match_catches', 'odi_match_runouts', 'odi_match_stumpings'],
    
    # OD statistics (domestic or other format)
    'od_batting': ['od_runs', 'od_4s', 'od_6s', 'od_strike_rate'],
    'od_bowling': ['od_match_wickets', 'od_match_bowledlbw', 'od_match_economy', 'od_match_maidens'],
    'od_fielding': ['od_match_catches', 'od_match_runouts', 'od_match_stumpings'],
    
    # T20I statistics
    't20i_batting': ['t20i_runs', 't20i_4s', 't20i_6s', 't20i_strike_rate'],
    't20i_bowling': ['t20i_match_wickets', 't20i_match_bowledlbw', 't20i_match_economy', 't20i_match_maidens'],
    't20i_fielding': ['t20i_match_catches', 't20i_match_runouts', 't20i_match_stumpings'],
    
    # T20 statistics (could refer to domestic T20 leagues or other T20 formats)
    't20_batting': ['t20_runs', 't20_4s', 't20_6s', 't20_strike_rate'],
    't20_bowling': ['t20_match_wickets', 't20_match_bowledlbw', 't20_match_economy', 't20_match_maidens'],
    't20_fielding': ['t20_match_catches', 't20_match_runouts', 't20_match_stumpings'],
    
    # Test match statistics
    'test_batting': ['test_runs', 'test_4s', 'test_6s', 'test_strike_rate'],
    'test_bowling': ['test_match_wickets', 'test_match_bowledlbw', 'test_match_economy', 'test_match_maidens'],
    'test_fielding': ['test_match_catches', 'test_match_runouts', 'test_match_stumpings'],
    
    # First-class statistics
    'fc_batting': ['fc_runs', 'fc_4s', 'fc_6s', 'fc_strike_rate'],
    'fc_bowling': ['fc_match_wickets', 'fc_match_bowledlbw', 'fc_match_economy', 'fc_match_maidens'],
    'fc_fielding': ['fc_match_catches', 'fc_match_runouts', 'fc_match_stumpings'],
    
    # Women's ODI statistics
    'wodi_batting': ['wodi_runs', 'wodi_4s', 'wodi_6s', 'wodi_strike_rate'],
    'wodi_bowling': ['wodi_match_wickets', 'wodi_match_bowledlbw', 'wodi_match_economy', 'wodi_match_maidens'],
    'wodi_fielding': ['wodi_match_catches', 'wodi_match_runouts', 'wodi_match_stumpings'],
    
    # Women's T20I statistics
    'wt20_batting': ['wt20_runs', 'wt20_4s', 'wt20_6s', 'wt20_strike_rate'],
    'wt20_bowling': ['wt20_match_wickets', 'wt20_match_bowledlbw', 'wt20_match_economy', 'wt20_match_maidens'],
    'wt20_fielding': ['wt20_match_catches', 'wt20_match_runouts', 'wt20_match_stumpings'],
    
    # Women's Test statistics
    'wtest_batting': ['wtest_runs', 'wtest_4s', 'wtest_6s', 'wtest_strike_rate'],
    'wtest_bowling': ['wtest_match_wickets', 'wtest_match_bowledlbw', 'wtest_match_economy', 'wtest_match_maidens'],
    'wtest_fielding': ['wtest_match_catches', 'wtest_match_runouts', 'wtest_match_stumpings'],
}


# Define feature columns for each target
feature_columns_dict = {
    'odi_runs': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'odi_4s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'odi_6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'odi_strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'odi_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'odi_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'odi_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'odi_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'odi_catches': ['previous_overs', 'previous_balls'],
    'odi_run_outs': ['previous_overs', 'previous_runs'],
    'odi_stumpings' : [],

    'wodi_runs': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'wodi_4s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'wodi_6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'wodi_strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'wodi_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'wodi_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'wodi_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'wodi_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'wodi_catches': ['previous_overs', 'previous_balls'],
    'wodi_run_outs': ['previous_overs', 'previous_runs'],
    'wodi_stumpings' : [],

    'od_runs': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'od_4s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'od_6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'od_strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'od_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'od_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'od_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'od_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'od_catches': ['previous_overs', 'previous_balls'],
    'od_run_outs': ['previous_overs', 'previous_runs'],
    'od_stumpings' : [],

    't20i_runs': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    't20i_4s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    't20i_6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    't20i_strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    't20i_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    't20i_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    't20i_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    't20i_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    't20i_catches': ['previous_overs', 'previous_balls'],
    't20i_run_outs': ['previous_overs', 'previous_runs'],
    't20i_stumpings' : [],

    'wt20i_runs': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'wt20i_4s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'wt20i_6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'wt20i_strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'wt20i_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'wt20i_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'wt20i_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'wt20i_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'wt20i_catches': ['previous_overs', 'previous_balls'],
    'wt20i_run_outs': ['previous_overs', 'previous_runs'],
    'wt20i_stumpings' : [],

    't20_runs': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    't20_4s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    't20_6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    't20_strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    't20_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    't20_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    't20_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    't20_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    't20_catches': ['previous_overs', 'previous_balls'],
    't20_run_outs': ['previous_overs', 'previous_runs'],
    't20_stumpings' : [],
 
    'odi_runs': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'odi_4s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'odi_6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'odi_strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'odi_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'odi_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'odi_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'odi_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'odi_catches': ['previous_overs', 'previous_balls'],
    'odi_run_outs': ['previous_overs', 'previous_runs'],
    'odi_stumpings' : [],

    'test_runs': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'test_4s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'test_6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'test_strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'test_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'test_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'test_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'test_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'test_catches': ['previous_overs', 'previous_balls'],
    'test_run_outs': ['previous_overs', 'previous_runs'],
    'test_stumpings' : [],

    'wtest_runs': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'wtest_4s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'wtest_6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'wtest_strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'wtest_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'wtest_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'wtest_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'wtest_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'wtest_catches': ['previous_overs', 'previous_balls'],
    'wtest_run_outs': ['previous_overs', 'previous_runs'],
    'wtest_stumpings' : [],

    'fc_runs': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'fc_4s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'fc_6s': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'fc_strike_rate': ['innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition', 'previous_4s', 'previous_6s'],
    'fc_match_wickets': ['tboDa_dismissals_agg', 'fboDa_dismissals_agg', 'tboDa_maidens_agg', 'fboDa_maidens_agg'],
    'fc_match_economy': ['tboDa_bowledlbw_agg', 'fboDa_economy_agg', 'tboDa_maidens_agg', 'vboDa_maidens_agg'],
    'fc_match_bowledlbw': ['tboDa_bowledlbw_agg', 'fboDa_bowledlbw_agg', 'tboDa_dismissals_agg', 'vboDa_bowledlbw_agg'],
    'fc_match_maidens': ['tboDa_maidens_agg', 'fboDa_maidens_agg', 'tboDa_dismissals_agg', 'tboDa_economy_agg'],
    'fc_catches': ['previous_overs', 'previous_balls'],
    'fc_run_outs': ['previous_overs', 'previous_runs'],
    'fc_stumpings' : [],
}


def predict(format, match_type, player_ids):
    predictor = PerformancePredictor(data_paths, target_columns_dict, feature_columns_dict)
    
    with open("combined_models.pkl", 'rb') as f:
        different_models = pickle.load(f)
    
    match_type = match_type.lower()
    for player_id in player_ids:
        runs_model = predictor.create_model('xgboost', different_models[f'{match_type}_batting']['runs'])
        runs = runs_model.predict()
        boundaries_model = predictor.create_model('xgboost', different_models[f'{match_type}_batting']['4s'])
        boundaries = boundaries_model.predict()
        sixes_model = predictor.create_model('xgboost', different_models[f'{match_type}_batting']['6s'])
        sixes = sixes_model.predict()
        strike_rate_model = predictor.create_model('xgboost', different_models[f'{match_type}_batting']['strike_rate'])
        strike_rate = strike_rate_model.predict()
        wickets_model = predictor.create_model('xgboost', different_models[f'{match_type}_bowling']['IT20_match_wickets'])
        wickets = wickets_model.predict()
        bowled_lbw_model = predictor.create_model('xgboost', different_models[f'{match_type}_bowling']['IT20_match_bowledlbw'])
        bowled_lbw = bowled_lbw_model.predict()
        maidens_model = predictor.create_model('xgboost', different_models[f'{match_type}_bowling']['IT20_match_maidens'])
        maidens = maidens_model.predict()
        economy_model = predictor.create_model('xgboost', different_models[f'{match_type}_bowling']['IT20_match_economy'])
        economy = economy_model.predict()
        catches_model = predictor.create_model('xgboost', different_models[f'{match_type}_fielding']['match_catches'])
        catches = catches_model.predict()
        stumpings_model = predictor.create_model('xgboost', different_models[f'{match_type}_fielding']['match_stumpings'])
        stumpings = stumpings_model.predict()
        runouts_direct_model = predictor.create_model('xgboost', different_models[f'{match_type}_fielding']['match_runouts'])
        runouts_direct = runouts_direct_model.predict()
        
        points = points_calculator(format, runs, boundaries, sixes, strike_rate, wickets, bowled_lbw, maidens, economy, catches, stumpings, runouts_direct, runouts_indirect)



