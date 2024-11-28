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
import warnings
from optuna.pruners import MedianPruner
from optuna.samplers import TPESampler
import os
import base64
from io import BytesIO

# Suppress warnings
warnings.filterwarnings('ignore')

class CricketPerformancePredictor:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.target_columns = ['runs', '4s', '6s']
        self.results = []  # To store results for HTML and CSV reports
        self.predictions_data = {}  # To store predictions and features for each model
        
        # Create directory for plots if it doesn't exist
        os.makedirs('plots', exist_ok=True)

    def get_base64_plot(self):
        """Convert the current matplotlib plot to base64 string"""
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode()

    def preprocess_data(self):
        feature_columns = ['innings_played', 'previous_balls', 'previous_balls_involved', 
                         'previous_outs', 'previous_average', 'previous_strike_rate', 
                         'previous_centuries', 'previous_fifties', 'previous_thirties', 
                         'previous_zeros', 'previous_runs', 'previous_4s', 'previous_6s', 'consistency', 'form', 'venue', 'opposition']
        self.feature_columns=feature_columns
        X = self.data[feature_columns]
        y = self.data[self.target_columns]
        return X, y

    def create_model(self, model_type, params):
        if model_type == 'xgboost':
            return XGBRegressor(tree_method='hist', **params)
        elif model_type == 'random_forest':
            return RandomForestRegressor(**params)
        elif model_type == 'gradient_boosting':
            return GradientBoostingRegressor(**params)
        elif model_type == 'lightgbm':
            return LGBMRegressor(device='cuda', **params)
        elif model_type == 'catboost':
            return CatBoostRegressor(task_type="GPU", verbose=0, **params)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    def objective(self, trial, X_train, y_train, model_type, target_column):
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
        
        kf = KFold(n_splits=2, shuffle=True, random_state=42)
        scores = []
        
        for train_idx, val_idx in kf.split(X_train):
            X_kf_train, X_kf_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
            y_kf_train = y_train[target_column].iloc[train_idx]
            y_kf_val = y_train[target_column].iloc[val_idx]

            scaler = StandardScaler()
            X_kf_train_scaled = scaler.fit_transform(X_kf_train)
            X_kf_val_scaled = scaler.transform(X_kf_val)

            model.fit(X_kf_train_scaled, y_kf_train)
            y_pred = model.predict(X_kf_val_scaled)
            scores.append(mean_squared_error(y_kf_val, y_pred))

        return np.mean(scores)

    def optimize_and_train(self, model_type, n_trials=50):
        X, y = self.preprocess_data()
        feature_importance_dict = {}
        best_params_dict = {}
        metrics_dict = {}
        models_dict = {}
        
        # Train separate model for each target
        for target in self.target_columns:
            print(f"Optimizing {model_type} for target: {target}")
            
            study = optuna.create_study(
                direction='minimize',
                pruner=MedianPruner(),
                sampler=TPESampler()
            )
            
            study.optimize(
                lambda trial: self.objective(trial, X, y, model_type, target),
                n_trials=n_trials
            )

            best_params = study.best_params
            best_params_dict[target] = best_params
            
            # Train final model with best parameters
            X_train, X_test, y_train, y_test = train_test_split(
                X, y[target], test_size=0.2, random_state=42
            )

            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            self.scaler = scaler

            model = self.create_model(model_type, best_params)
            model.fit(X_train_scaled, y_train)
            # Store model
            models_dict[target] = model
            
            # Get predictions
            y_pred = model.predict(X_test_scaled)
            
            # Calculate metrics
            metrics_dict[target] = {
                'MSE': mean_squared_error(y_test, y_pred),
                'MAE': mean_absolute_error(y_test, y_pred),
                'R2': r2_score(y_test, y_pred)
            }
            
            # Get feature importance
            if hasattr(model, 'feature_importances_'):
                feature_importance_dict[target] = pd.DataFrame({
                    'feature': X.columns,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)

        self.predictions_data[model_type] = {
            'models': models_dict,
            'feature_importance': feature_importance_dict
        }

        self.results.append({
            'model_type': model_type,
            'metrics': metrics_dict,
            'best_params': best_params_dict,
            'feature_importance': feature_importance_dict
        })

    def generate_html_report(self):
        html_content = """
        <html>
        <head>
            <title>Model Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; margin: 15px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f5f5f5; }
                .model-section { margin-bottom: 30px; }
            </style>
        </head>
        <body>
        """
        
        for result in self.results:
            html_content += f"<div class='model-section'>"
            html_content += f"<h2>Model: {result['model_type']}</h2>"
            
            # Add metrics table
            html_content += "<h3>Performance Metrics</h3>"
            metrics_df = pd.DataFrame(result['metrics']).round(4)
            html_content += metrics_df.to_html()
            
            # Add feature importance for each target
            for target, importance in result['feature_importance'].items():
                if importance is not None:
                    html_content += f"<h3>Feature Importance for {target}</h3>"
                    html_content += importance.to_html()
            
            html_content += "</div>"
        
        html_content += "</body></html>"
        
        with open("report.html", "w") as f:
            f.write(html_content)

    def compare_models(self):
        for model_type in ['xgboost']:#, 'random_forest', 'gradient_boosting', 'lightgbm', 'catboost']:
            print(f"\nTraining {model_type.upper()} models...")
            self.optimize_and_train(model_type)
        self.generate_html_report()
    
    def generate_parameters_csv(self):
        # Create a dataframe for parameters
        parameters_csv = []

        for result in self.results:
            model_type = result['model_type']
            for target, params in result['best_params'].items():
                param_record = {
                    'model_type': model_type,
                    'target': target,
                }
                param_record.update(params)
                parameters_csv.append(param_record)

        parameters_df = pd.DataFrame(parameters_csv)
        parameters_df.to_csv("model_parameters.csv", index=False)
        print("Model parameters CSV saved as 'model_parameters.csv'")

    def generate_predictions_csv(self):
        # Create a dataframe for predictions
        predictions_csv = pd.DataFrame()

        # Add player names
        predictions_csv['name'] = self.data['name']

        # Add real values
        for target in self.target_columns:
            predictions_csv[f'real_{target}'] = self.data[target]

        # Add predicted values for each model
        for model_type, model_data in self.predictions_data.items():
            for target, model in model_data['models'].items():
                X, _ = self.preprocess_data()
                X_scaled = self.scaler.transform(X)

                predictions_csv[f'{model_type}_predicted_{target}'] = model.predict(X_scaled)

        # Save to CSV
        predictions_csv.to_csv("player_predictions.csv", index=False)
        print("Predictions CSV saved as 'player_predictions.csv'")
    
    def predict(self,playerNames,date):
        '''
            given list of player names and date run predict_by_name for each one of them and give final predicitons are results 4s, 6s, runs
            output is matrix (number of players x 3)
        '''
        X=[]
        for player in playerNames:
            X.append(self.get_feature_by_name(player,date))
        X = (pd.DataFrame(X))
        X_scaled = self.scaler.transform(X)
        preds ={}
        for target in self.target_columns:
            model = self.predictions_data['xgboost']['models'][target]
            preds[target]  = model.predict(X_scaled)
        return pd.DataFrame(preds)

    def get_feature_by_name(self,playerName,date):
        '''
        input:
            'Player-name'
        preprocess:
            'consistency','form','innings_played', 'previous_balls', 'previous_balls_involved', 'previous_outs', 'previous_average', 'previous_strike_rate', 'previous_centuries', 'previous_fifties', 'previous_thirties', 'previous_zeros', 'previous_runs', 'venue', 'opposition','previous_4s','previous_6s'
            for last time player played before the date mentioned 
        output:
            4s 6s runs
        '''
        if playerName not in self.data['name'].values:
            raise ValueError(f"Player {playerName} not found in the dataset.")
    
        filtered_data = self.data[self.data['name'] == playerName]
        if filtered_data.empty:
            raise ValueError(f"No data found for player {playerName}.")
        
        try:
            date = pd.to_datetime(date)
        except Exception as e:
            raise ValueError(f"Error in converting 'date' column to datetime: {e}")

        # Filter rows where the date is less than the given date
        filtered_data = filtered_data[pd.to_datetime(filtered_data['date']) <= date]
        # Sort by date in descending order to get the most recent date before the given date
        result = filtered_data.sort_values(by='date', ascending=False).head(1)
        X = result[self.feature_columns] #getting features for prediction
        return X.values.flatten().tolist()