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
import argparse
from datetime import datetime

# Suppress warnings
import warnings

warnings.filterwarnings("ignore")
global mapping
mapping = {}


class PerformancePredictor:
    def __init__(self, data_paths, target_columns_dict, feature_columns_dict):
        buffer = ""
        self.buffer = buffer
        self.data_paths = data_paths  # Dictionary of CSV file paths
        self.target_columns_dict = (
            target_columns_dict  # Dictionary of target columns for each player type
        )
        self.feature_columns_dict = (
            feature_columns_dict  # Dictionary of feature columns for each target column
        )
        self.results = []  # To store results for HTML and CSV reports
        self.predictions_data = {}  # To store predictions and models for each target
        self.models = {}  # To store the weights of all models
        self.scalers = {}
        os.makedirs("plots", exist_ok=True)  # Create directory for plots

    def preprocess_data(
        self, target_column, data, train_from, train_to, test_from, test_to
    ):
        """Preprocess data by selecting features for the target column"""
        feature_columns = self.feature_columns_dict.get(target_column)
        if not feature_columns:
            raise ValueError(
                f"No feature columns defined for target column: {target_column}"
            )

        # Select features and target column
        data_train = data[
            (pd.to_datetime(data["date"]) < datetime.fromisoformat(train_to))
            & (pd.to_datetime(data["date"]) > datetime.fromisoformat(train_from))
        ]  # $$$

        data_test = data[
            (pd.to_datetime(data["date"]) < datetime.fromisoformat(test_to))
            & (pd.to_datetime(data["date"]) > datetime.fromisoformat(test_from))
        ]  # $$$

        if data_train.empty or data_test.empty:
            print(
                f"Skipping target '{target_column}' as no matches found in the specified date range."
            )
            return False, None, None, None, None

        X_train = data_train[feature_columns]

        y_train = data_train[target_column]
        X_test = data_test[feature_columns]

        y_test = data_test[target_column]

        return True, X_train, X_test, y_train, y_test

    def create_model(self, model_type, params):
        """Create a model based on the selected type"""
        if model_type == "xgboost":
            return XGBRegressor(tree_method="gpu_hist", **params)
        elif model_type == "random_forest":
            return RandomForestRegressor(**params)
        elif model_type == "gradient_boosting":
            return GradientBoostingRegressor(**params)
        elif model_type == "lightgbm":
            return LGBMRegressor(device="gpu", **params)
        elif model_type == "catboost":
            return CatBoostRegressor(task_type="GPU", verbose=0, **params)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    def train_and_evaluate_model(
        self, model_type, data, target_column, train_from, train_to, test_from, test_to
    ):

        """Train and evaluate a model without optimization"""
        # Preprocess data for the target column
        # X, y = self.preprocess_data(target_column, data)
        # Split data into train and test sets (20% test data)
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        passed, X_train, X_test, y_train, y_test = self.preprocess_data(
            target_column, data, train_from, train_to, test_from, test_to
        )
        if not passed:
            return passed, None, None, None, None, None
        # Standardize the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        self.scaler_model = scaler

        # Define default hyperparameters
        if model_type == "xgboost":
            params = {
                "n_estimators": 100,
                "max_depth": 6,
                "learning_rate": 0.1,
                "subsample": 0.8,
                "colsample_bytree": 0.8,
                "reg_alpha": 0.1,
                "reg_lambda": 0.1,
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
            "MSE": mean_squared_error(y_test, y_pred),
            "MAE": mean_absolute_error(y_test, y_pred),
            "R2": r2_score(y_test, y_pred),
        }

        # Store the model for respective target
        self.models[target_column] = model
        self.scalers[target_column] = scaler

        # Store the results
        self.predictions_data[target_column] = {
            "metrics": metrics,
            "model": model,
            "y_test": y_test,
            "y_pred": y_pred,
        }

        return True, metrics, model, X_test, y_test, y_pred

    def save_all_models(self):
        """Save all models into a single .pkl file"""
        with open("pickles/models.pkl", "wb") as f:
            pickle.dump(self.models, f)
        with open("pickles/scalers.pkl", "wb") as f:
            pickle.dump(self.scalers, f)

    def run_training(
        self, train_from, train_to, test_from, test_to, model_type="xgboost"
    ):
        all_predictions = []  # List to hold all predictions for CSV output

        for player_type, data_path in self.data_paths.items():
            data = pd.read_csv(self.buffer + data_path)
            target_columns = self.target_columns_dict[
                player_type
            ]  # Get target columns for current player type

            for target_column in target_columns:
                print(f"Training model for target: {target_column} in {player_type}")
                (
                    passed,
                    metrics,
                    model,
                    X_test,
                    y_test,
                    y_pred,
                ) = self.train_and_evaluate_model(
                    model_type,
                    data,
                    target_column,
                    train_from,
                    train_to,
                    test_from,
                    test_to,
                )

                data_test = data[
                    (pd.to_datetime(data["date"]) < datetime.fromisoformat(test_to))
                    & (pd.to_datetime(data["date"]) > datetime.fromisoformat(test_from))
                ]  # $$$
                t_ID = data_test["player_id"]
                match_id = data_test["match_id"]
                if "bowl" in target_column:
                    balls = data_test["balls"]
                else:
                    balls = [0 for _ in range(len(data_test))]
                name = data_test["player_name"]
                # Store the actual and predicted values in a list for CSV export
                global mapping

                if passed:
                    for (
                        true_value,
                        predicted_value,
                        player_id,
                        m_id,
                        ball,
                        name_1,
                        date,
                    ) in zip(
                        y_test, y_pred, t_ID, match_id, balls, name, data_test["date"]
                    ):

                        all_predictions.append(
                            {
                                "player_id": player_id,
                                "target_column": target_column,
                                "true_value": true_value,
                                "predicted_value": predicted_value,
                                "match_id": str(m_id),
                                "balls": ball,
                                "name": name_1,
                            }
                        )
                        if m_id not in mapping:
                            if "team" in data_test.columns:
                                team_1 = data_test.loc[data["match_id"] == m_id]["team"]
                            elif "team_name" in data_test.columns:
                                team_1 = data_test.loc[data["match_id"] == m_id][
                                    "team_name"
                                ]
                            try:
                                team_2 = data_test.loc[data["match_id"] == m_id][
                                    "opposition_name"
                                ]
                                mapping[m_id] = [team_1, team_2, date]
                            except:
                                print(f"ERROR TEAMS NOT FOUND{m_id}")
        print(self.scalers)
        print(self.models)

        # Save all models after training
        os.makedirs("pickles", exist_ok=True)
        self.save_all_models()

        # Convert the list of predictions to a DataFrame
        predictions_df = pd.DataFrame(all_predictions)

        # Save predictions to CSV
        predictions_df.to_csv("predictions_output.csv", index=False)
        print(f"Predictions saved to 'predictions_output.csv'")
        return predictions_df


def calculate_batsman_points_t20(runs, boundaries, sixes, strike_rate, balls_faced):
    batsman_points = 0

    # Runs points
    batsman_points += runs

    # Boundary points
    batsman_points += boundaries * 1  # 1 point per boundary

    # Six points
    batsman_points += sixes * 2  # 2 points per six

    # Milestones points

    batsman_points += np.where(runs > 100, 16, 0)  # 100 runs = 16 points
    batsman_points += np.where(runs > 50, 8, 0)
    batsman_points += np.where(runs > 30, 4, 0)

    # Duck points
    # if runs == 0 and is_out:
    #     batsman_points -= 2  # Duck = -2 points

    # Strike rate bonus points (if player faced at least 10 balls)

    runs_per_100_balls = strike_rate
    # if runs_per_100_balls > 170:
    batsman_points += np.where(
        (balls_faced >= 10) & (runs_per_100_balls > 170), 6, 0
    )  # Above 170 runs per 100 balls
    # elif 150 < runs_per_100_balls <= 170:
    batsman_points += np.where(
        (balls_faced >= 10) & (runs_per_100_balls <= 170) & (runs_per_100_balls > 150),
        4,
        0,
    )  # Between 150.01 and 170 runs per 100 balls
    # elif 130 <= runs_per_100_balls <= 150:
    batsman_points += np.where(
        (balls_faced >= 10) & (runs_per_100_balls <= 150) & (runs_per_100_balls > 130),
        2,
        0,
    )  # Between 130 and 150 runs per 100 balls
    # elif 60 <= runs_per_100_balls <= 70:
    batsman_points += np.where(
        (balls_faced >= 10) & (runs_per_100_balls <= 70) & (runs_per_100_balls > 60),
        -2,
        0,
    )  # Between 60 and 70 runs per 100 balls
    # elif 50 <= runs_per_100_balls < 60:
    batsman_points += np.where(
        (balls_faced >= 10) & (runs_per_100_balls <= 60) & (runs_per_100_balls > 50),
        -4,
        0,
    )  # Between 50 and 59.99 runs per 100 balls
    # elif runs_per_100_balls < 50:
    batsman_points += np.where(
        (balls_faced >= 10) & (runs_per_100_balls < 50), -4, 0
    )  # Below 50 runs per 100 balls

    return batsman_points


def calculate_batsman_points_odi(runs, boundaries, sixes, strike_rate, balls_faced):
    batsman_points = 0

    # Run points
    batsman_points += runs

    # Boundary points
    batsman_points += boundaries * 1  # 1 point per boundary

    # Six points
    batsman_points += sixes * 2  # 2 points per six

    # Half-century & Century points
    # if runs >= 100:
    batsman_points += np.where(runs > 100, 8, 0)  # 100 runs = 8 points
    # elif runs >= 50:
    batsman_points += np.where(runs > 50, 4, 0)  # 50 runs = 4 points

    # Duck points
    # if runs == 0 and is_out:
    #     batsman_points -= 3  # Duck = -3 points

    # Strike rate bonus points (if player faced at least 20 balls)
    # if balls_faced >= 20:
    runs_per_100_balls = (runs / balls_faced) * 100
    # if runs_per_100_balls > 140:
    batsman_points += np.where(
        (balls_faced >= 20) & (runs_per_100_balls > 140), 6, 0
    )  # Above 140 runs per 100 balls
    # elif 120 < runs_per_100_balls <= 140:
    batsman_points += np.where(
        (balls_faced >= 10) & (runs_per_100_balls <= 140) & (runs_per_100_balls > 120),
        4,
        0,
    )  # Between 120.01 and 140 runs per 100 balls
    # elif 100 <= runs_per_100_balls <= 120:
    batsman_points += np.where(
        (balls_faced >= 10) & (runs_per_100_balls <= 120) & (runs_per_100_balls > 100),
        2,
        0,
    )  # Between 100 and 120 runs per 100 balls
    # elif 40 <= runs_per_100_balls <= 50:
    batsman_points += np.where(
        (balls_faced >= 10) & (runs_per_100_balls <= 50) & (runs_per_100_balls >= 40),
        -2,
        0,
    )  # Between 40 and 50 runs per 100 balls
    # elif 30 <= runs_per_100_balls < 40:
    batsman_points += np.where(
        (balls_faced >= 10) & (runs_per_100_balls < 40) & (runs_per_100_balls >= 30),
        -4,
        0,
    )  # Between 30 and 39.99 runs per 100 balls
    # elif runs_per_100_balls < 30:
    batsman_points += np.where(
        (balls_faced >= 20) & (runs_per_100_balls < 30), -6, 0
    )  # Below 30 runs per 100 ball
    return batsman_points


def calculate_batsman_points_test(runs, boundaries, sixes, strike_rate, balls_faced):
    batsman_points = 0

    # Run points
    batsman_points += runs

    # Boundary points
    batsman_points += boundaries * 1  # 1 point per boundary

    # Six points
    batsman_points += sixes * 2  # 2 points per six

    # Half-century & Century points
    # if runs >= 100:
    batsman_points += np.where((runs >= 100), 8, 0)  # 100 runs = 8 points
    # elif runs >= 50:
    batsman_points += np.where((runs >= 50), 4, 0)  # 50 runs = 4 points

    # Duck points
    # if runs == 0 and is_out:
    #     batsman_points -= 4  # Duck = -4 points

    return batsman_points


# @title bowler 20
def calculate_bowler_points_t20(wickets, bowled_lbw, maidens, economy, balls):
    bowler_points = 0

    # Wicket points
    bowler_points += wickets * 25  # 25 points per wicket

    # Bowled/LBW bonus points (8 points per wicket for Bowled or LBW)
    bowler_points += bowled_lbw * 8  # Each Bowled/LBW wicket adds 8 points

    # Wicket bonus points
    # if wickets >= 5:
    bowler_points += np.where(wickets >= 5, 16, 0)  # 5 wickets = 16 points
    # elif wickets == 4:
    bowler_points += np.where(wickets == 4, 8, 0)  # 4 wickets = 8 points
    # elif wickets == 3:
    bowler_points += np.where(wickets == 3, 4, 0)  # 3 wickets = 4 points

    # Maiden Over points
    bowler_points += maidens * 12  # 12 points per maiden over

    # Economy points
    # if balls >= 12:
    #     if economy < 5:
    bowler_points += np.where(
        (balls >= 12) & (economy < 5), 6, 0
    )  # Below 5 runs per over
    # elif 5 <= economy < 6:
    bowler_points += np.where(
        (balls >= 12) & (economy >= 5) & (economy < 6), 4, 0
    )  # Between 5 and 5.99 runs per over
    # elif 6 <= economy <= 7:
    bowler_points += np.where(
        (balls >= 12) & (economy >= 6) & (economy < 7), 2, 0
    )  # Between 6 and 7 runs per over
    # elif 10 <= economy <= 11:
    bowler_points += np.where(
        (balls >= 12) & (economy >= 10) & (economy <= 11), -2, 0
    )  # Between 10 and 11 runs per over
    # elif 11 < economy <= 12:
    bowler_points += np.where(
        (balls >= 12) & (economy > 11) & (economy <= 12), -4, 0
    )  # Between 11.01 and 12 runs per over
    # elif economy > 12:
    bowler_points += np.where(
        (balls >= 12) & (economy > 12), -6, 0
    )  # Above 12 runs per over

    return bowler_points


def calculate_bowler_points_odi(wickets, bowled_lbw, maidens, economy, balls):
    bowler_points = 0

    # Wicket points (excluding run outs)
    bowler_points += wickets * 25  # 25 points per wicket

    # Bowled/LBW bonus points (8 points per wicket for Bowled or LBW)
    bowler_points += bowled_lbw * 8  # Each Bowled/LBW wicket adds 8 points

    # Wicket bonus points
    # if wickets >= 5:
    bowler_points += np.where((wickets >= 5), 8, 0)  # 5 wickets = 8 points
    # elif wickets == 4:
    bowler_points += np.where((wickets == 4), 4, 0)  # 4 wickets = 4 points

    # Maiden Over points
    bowler_points += maidens * 4  # 4 points per maiden over

    # Economy points
    # if balls >= 30:
    #     if economy < 2.5:
    bowler_points += np.where(
        (balls >= 30) & (economy < 2.5), 6, 0
    )  # Below 2.5 runs per over
    # elif 2.5 <= economy < 3.5:
    bowler_points += np.where(
        (balls >= 12) & (economy >= 2.5) & (economy < 3.5), 4, 0
    )  # Between 2.5 and 3.49 runs per over
    # elif 3.5 <= economy <= 4.5:
    bowler_points += np.where(
        (balls >= 12) & (economy >= 3.5) & (economy <= 4.5), 2, 0
    )  # Between 3.5 and 4.5 runs per over
    # elif 7 <= economy <= 8:
    bowler_points += np.where(
        (balls >= 12) & (economy >= 7) & (economy <= 8), -2, 0
    )  # Between 7 and 8 runs per over
    # elif 8 < economy <= 9:
    bowler_points += np.where(
        (balls >= 12) & (economy > 8) & (economy <= 9), -4, 0
    )  # Between 8.01 and 9 runs per over
    # elif economy > 9:
    bowler_points += np.where(
        (balls >= 30) & (economy > 9), -6, 0
    )  # Above 9 runs per over

    return bowler_points


# @title test
def calculate_bowler_points_test(wickets, bowled_lbw, maidens, economy, balls):
    bowler_points = 0

    # Wicket points (excluding run outs)
    bowler_points += wickets * 16  # 16 points per wicket

    # Bowled/LBW bonus points (8 points per wicket for Bowled or LBW)
    bowler_points += bowled_lbw * 8  # Each Bowled/LBW wicket adds 8 points

    # Wicket bonus points
    # if wickets >= 5:
    bowler_points += np.where((wickets >= 5), 8, 0)  # 5 wickets = 8 points
    # elif wickets == 4:
    bowler_points += np.where((wickets == 4), 4, 0)  # 4 wickets = 4 points

    return bowler_points


def calculate_fielder_points_t20(catches, stumpings):
    fielder_points = 0

    # Catches: +8 points for each catch
    fielder_points += catches * 8

    # 3 Catch Bonus: +4 points if 3 or more catches are taken
    # if catches >= 3:
    fielder_points += np.where(catches >= 3, 4, 0)

    # Stumpings: +12 points for each stumping
    fielder_points += stumpings * 12

    # fielder_points += runouts* 9

    return fielder_points


def calculate_fielder_points_odi(catches, stumpings):
    fielder_points = 0

    # Catches: +8 points for each catch
    fielder_points += catches * 8

    # 3 Catch Bonus: +4 points if 3 or more catches are taken
    # if catches >= 3:
    fielder_points += np.where(catches >= 3, 4, 0)

    # Stumpings: +12 points for each stumping
    fielder_points += stumpings * 12

    # fielder_points += runouts * 9

    return fielder_points


def calculate_fielder_points_test(catches, stumpings):
    fielder_points = 0

    # Catches: +8 points for each catch
    fielder_points += catches * 8

    # Stumpings: +12 points for each stumping
    fielder_points += stumpings * 12

    # fielder_points += runouts * 9

    return fielder_points


def points_calculator(
    format,
    runs,
    boundaries,
    sixes,
    strike_rate,
    wickets,
    bowled_lbw,
    maidens,
    economy,
    catches,
    stumpings,
    balls_bowled=30,
):  # assume each bowler bowls 2 overs
    # strike rate is runs per 100 balls. strike rate/100 is runs per ball. hence runs*100/strike_rate is number of balls

    balls_faced_while_batting = runs * 100 / strike_rate
    balls_faced_while_batting.replace([np.inf], 0)
    format = format.lower()
    if format[-2:] == "20":
        total_points = (
            calculate_batsman_points_t20(
                runs, boundaries, sixes, strike_rate, balls_faced_while_batting
            )
            + calculate_bowler_points_t20(
                wickets, bowled_lbw, maidens, economy, balls_bowled
            )
            + calculate_fielder_points_t20(catches, stumpings)
        )

    elif "od" in format:
        total_points = (
            calculate_batsman_points_odi(
                runs, boundaries, sixes, strike_rate, balls_faced_while_batting
            )
            + calculate_bowler_points_odi(
                wickets, bowled_lbw, maidens, economy, balls_bowled
            )
            + calculate_fielder_points_odi(catches, stumpings)
        )

    else:
        total_points = (
            calculate_batsman_points_test(
                runs, boundaries, sixes, strike_rate, balls_faced_while_batting
            )
            + calculate_bowler_points_test(
                wickets, bowled_lbw, maidens, economy, balls_bowled
            )
            + calculate_fielder_points_test(catches, stumpings)
        )

    return total_points


# Define file paths
data_paths = {
    "ODI_batting": "all_data/ODI/batter.csv",
    "ODI_bowling": "all_data/ODI/bowler.csv",
    "ODI_fielding": "all_data/ODI/fielder.csv",
    "ODM_batting": "all_data/ODM/batter.csv",
    "ODM_bowling": "all_data/ODM/bowler.csv",
    "ODM_fielding": "all_data/ODM/fielder.csv",
    "T20_batting": "all_data/T20/batter.csv",
    "T20_bowling": "all_data/T20/bowler.csv",
    "T20_fielding": "all_data/T20/fielder.csv",
    "IT20_batting": "all_data/IT20/batter.csv",
    "IT20_bowling": "all_data/IT20/bowler.csv",
    "IT20_fielding": "all_data/IT20/fielder.csv",
    "Test_batting": "all_data/Test/batter.csv",
    "Test_bowling": "all_data/Test/bowler.csv",
    "Test_fielding": "all_data/Test/fielder.csv",
    "MDM_batting": "all_data/MDM/batter.csv",
    "MDM_bowling": "all_data/MDM/bowler.csv",
    "MDM_fielding": "all_data/MDM/fielder.csv",
    "WODI_batting": "all_data/WODI/batter.csv",
    "WODI_bowling": "all_data/WODI/bowler.csv",
    "WODI_fielding": "all_data/WODI/fielder.csv",
    "WT20_batting": "all_data/WT20/batter.csv",
    "WT20_bowling": "all_data/WT20/bowler.csv",
    "WT20_fielding": "all_data/WT20/fielder.csv",
    "WTest_batting": "all_data/WTest/batter.csv",
    "WTest_bowling": "all_data/WTest/bowler.csv",
    "WTest_fielding": "all_data/WTest/fielder.csv",
    "WODM_batting": "all_data/WODM/batter.csv",
    "WODM_bowling": "all_data/WODM/bowler.csv",
    "WODM_fielding": "all_data/WODM/fielder.csv",
    "WIT20_batting": "all_data/WIT20/batter.csv",
    "WIT20_bowling": "all_data/WIT20/bowler.csv",
    "WIT20_fielding": "all_data/WIT20/fielder.csv",
}

# Define target columns for each player type
target_columns_dict = {
    # ODI statistics
    "ODI_batting": [
        "ODI_match_runs",
        "ODI_match_4s",
        "ODI_match_6s",
        "ODI_match_strike_rate",
    ],
    "ODI_bowling": [
        "ODI_match_wickets",
        "ODI_match_bowledlbw",
        "ODI_match_economy",
        "ODI_match_maidens",
    ],
    "ODI_fielding": ["match_runouts", "match_catches", "match_stumpings"],
    # ODM statistics (domestic or other format)
    "ODM_batting": [
        "ODM_match_runs",
        "ODM_match_4s",
        "ODM_match_6s",
        "ODM_match_strike_rate",
    ],
    "ODM_bowling": [
        "ODM_match_wickets",
        "ODM_match_bowledlbw",
        "ODM_match_economy",
        "ODM_match_maidens",
    ],
    "ODM_fielding": ["match_runouts", "match_catches", "match_stumpings"],
    # T20 statistics
    "T20_batting": [
        "T20_match_runs",
        "T20_match_4s",
        "T20_match_6s",
        "T20_match_strike_rate",
    ],
    "T20_bowling": [
        "T20_match_wickets",
        "T20_match_bowledlbw",
        "T20_match_economy",
        "T20_match_maidens",
    ],
    "T20_fielding": ["match_runouts", "match_catches", "match_stumpings"],
    # IT20 statistics (could refer to domestic T20 leagues or other T20 formats)
    "IT20_batting": [
        "IT20_match_runs",
        "IT20_match_4s",
        "IT20_match_6s",
        "IT20_match_strike_rate",
    ],
    "IT20_bowling": [
        "IT20_match_wickets",
        "IT20_match_bowledlbw",
        "IT20_match_economy",
        "IT20_match_maidens",
    ],
    "IT20_fielding": ["match_runouts", "match_catches", "match_stumpings"],
    # Test match statistics
    "Test_batting": [
        "Test_match_runs",
        "Test_match_4s",
        "Test_match_6s",
        "Test_match_strike_rate",
    ],
    "Test_bowling": [
        "Test_match_wickets",
        "Test_match_bowledlbw",
        "Test_match_economy",
        "Test_match_maidens",
    ],
    "Test_fielding": ["match_runouts", "match_catches", "match_stumpings"],
    # MDM statistics
    "MDM_batting": [
        "MDM_match_runs",
        "MDM_match_4s",
        "MDM_match_6s",
        "MDM_match_strike_rate",
    ],
    "MDM_bowling": [
        "MDM_match_wickets",
        "MDM_match_bowledlbw",
        "MDM_match_economy",
        "MDM_match_maidens",
    ],
    "MDM_fielding": ["match_runouts", "match_catches", "match_stumpings"],
    # Women's ODI statistics
    "WODI_batting": [
        "WODI_match_runs",
        "WODI_match_4s",
        "WODI_match_6s",
        "WODI_match_strike_rate",
    ],
    "WODI_bowling": [
        "WODI_match_wickets",
        "WODI_match_bowledlbw",
        "WODI_match_economy",
        "WODI_match_maidens",
    ],
    "WODI_fielding": ["match_runouts", "match_catches", "match_stumpings"],
    # Women's T20I statistics
    "WT20_batting": [
        "WT20_match_runs",
        "WT20_match_4s",
        "WT20_match_6s",
        "WT20_match_strike_rate",
    ],
    "WT20_bowling": [
        "WT20_match_wickets",
        "WT20_match_bowledlbw",
        "WT20_match_economy",
        "WT20_match_maidens",
    ],
    "WT20_fielding": ["match_runouts", "match_catches", "match_stumpings"],
    # Women's Test statistics
    "WTest_batting": [
        "WTest_match_runs",
        "WTest_match_4s",
        "WTest_match_6s",
        "WTest_match_strike_rate",
    ],
    "WTest_bowling": [
        "WTest_match_wickets",
        "WTest_match_bowledlbw",
        "WTest_match_economy",
        "WTest_match_maidens",
    ],
    "WTest_fielding": ["match_runouts", "match_catches", "match_stumpings"],
    # Women's ODM
    "WODM_batting": [
        "WODM_match_runs",
        "WODM_match_4s",
        "WODM_match_6s",
        "WODM_match_strike_rate",
    ],
    "WODM_bowling": [
        "WODM_match_wickets",
        "WODM_match_bowledlbw",
        "WODM_match_economy",
        "WODM_match_maidens",
    ],
    "WODM_fielding": ["match_runouts", "match_catches", "match_stumpings"],
    # Women's ODM
    "WIT20_batting": [
        "WIT20_match_runs",
        "WIT20_match_4s",
        "WIT20_match_6s",
        "WIT20_match_strike_rate",
    ],
    "WIT20_bowling": [
        "WIT20_match_wickets",
        "WIT20_match_bowledlbw",
        "WIT20_match_economy",
        "WIT20_match_maidens",
    ],
    "WIT20_fielding": ["match_runouts", "match_catches", "match_stumpings"],
}


# Define feature columns for each target
feature_columns_dict = {
    "ODI_match_runs": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "ODI_match_4s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "ODI_match_6s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "ODI_match_strike_rate": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "ODI_match_wickets": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "ODI_match_economy": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "ODI_match_bowledlbw": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "ODI_match_maidens": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "ODM_match_runs": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "ODM_match_4s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "ODM_match_6s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "ODM_match_strike_rate": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "ODM_match_wickets": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "ODM_match_economy": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "ODM_match_bowledlbw": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "ODM_match_maidens": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "T20_match_runs": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "T20_match_4s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "T20_match_6s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "T20_match_strike_rate": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "T20_match_wickets": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "T20_match_economy": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "T20_match_bowledlbw": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "T20_match_maidens": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "IT20_match_runs": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "IT20_match_4s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "IT20_match_6s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "IT20_match_strike_rate": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "IT20_match_wickets": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "IT20_match_economy": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "IT20_match_bowledlbw": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "IT20_match_maidens": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "Test_match_runs": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "Test_match_4s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "Test_match_6s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "Test_match_strike_rate": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "Test_match_wickets": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "Test_match_economy": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "Test_match_bowledlbw": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "Test_match_maidens": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "MDM_match_runs": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "MDM_match_4s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "MDM_match_6s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "MDM_match_strike_rate": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "MDM_match_wickets": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "MDM_match_economy": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "MDM_match_bowledlbw": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "MDM_match_maidens": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WODI_match_runs": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WODI_match_4s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WODI_match_6s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WODI_match_strike_rate": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WODI_match_wickets": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WODI_match_economy": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WODI_match_bowledlbw": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WODI_match_maidens": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WTest_match_runs": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WTest_match_4s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WTest_match_6s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WTest_match_strike_rate": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WTest_match_wickets": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WTest_match_economy": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WTest_match_bowledlbw": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WTest_match_maidens": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WT20_match_runs": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WT20_match_4s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WT20_match_6s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WT20_match_strike_rate": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WT20_match_wickets": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WT20_match_economy": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WT20_match_bowledlbw": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WT20_match_maidens": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WIT20_match_runs": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WIT20_match_4s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WIT20_match_6s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WIT20_match_strike_rate": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WIT20_match_wickets": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WIT20_match_economy": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WIT20_match_bowledlbw": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WIT20_match_maidens": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WODM_match_runs": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WODM_match_4s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WODM_match_6s": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WODM_match_strike_rate": [
        "venue",
        "innings_played",
        "previous_balls_involved",
        "previous_outs",
        "previous_average",
        "previous_strike_rate",
        "previous_centuries",
        "previous_thirties",
        "previous_fifties",
        "previous_zeros",
        "previous_runs",
        "previous_4s",
        "previous_6s",
        "highest_score",
        "opposition",
        "consistency",
        "form",
        "career_score",
        "recent_score",
        "combined_score",
        "WvbaH_dismissals",
        "WvbaH_4s",
        "WvbaH_6s",
        "WvbaH_economy",
        "WfbaH_dismissals",
        "WfbaH_4s",
        "WfbaH_6s",
        "WfbaH_economy",
        "WtbaH_dismissals",
        "WtbaH_4s",
        "WtbaH_6s",
        "WtbaH_economy",
    ],
    "WODM_match_wickets": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WODM_match_economy": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WODM_match_bowledlbw": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "WODM_match_maidens": [
        "WvboDa_economy",
        "WvboDa_dismissals",
        "WvboDa_bowledlbw",
        "WvboDa_maidens",
        "WtboDa_economy",
        "WtboDa_dismissals",
        "WtboDa_bowledlbw",
        "WtboDa_maidens",
        "WfboDa_economy",
        "WfboDa_dismissals",
        "WfboDa_bowledlbw",
        "WfboDa_maidens",
        "innings_played",
        "previous_balls_involved",
        "previous_wickets",
        "previous_average",
        "previous_strike_rate",
        "previous_economy",
        "venue_maidens",
        "venue_bowledlbw",
        "venue_average",
        "venue_economy",
        "venue_innings",
        "previous_3haul",
        "previous_5haul",
        "previous_maidens",
        "consistency",
        "form",
        "venue",
        "opposition",
    ],
    "match_catches": ["previous_catches", "pFa_catches", "venue_catches"],
    "match_runouts": ["previous_runouts", "pFa_runouts", "venue_runouts"],
    "match_stumpings": ["previous_stumpings", "pFa_stumpings", "venue_stumpings"],
}

#####date is defined here $$$$


if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Process 4 dates")

    # Define the 4 date arguments (with date format validation)
    parser.add_argument("date1", type=str, help="First date (format: YYYY-MM-DD)")
    parser.add_argument("date2", type=str, help="Second date (format: YYYY-MM-DD)")
    parser.add_argument("date3", type=str, help="Third date (format: YYYY-MM-DD)")
    parser.add_argument("date4", type=str, help="Fourth date (format: YYYY-MM-DD)")

    # Parse the arguments
    args = parser.parse_args()

    # Access the dates
    date1 = args.date1
    date2 = args.date2
    date3 = args.date3
    date4 = args.date4
    model = PerformancePredictor(data_paths, target_columns_dict, feature_columns_dict)
    date = [date1, date2, date3, date4]  # fat
    model.run_training(
        *date
    )  # /content/drive/MyDrive/all_data/IT20/batter.csv

    output = pd.read_csv("predictions_output.csv")

    lst_feature = {
        "runs": "runs",
        "6": "sixes",
        "4": "boundaries",
        "strike": "strike_rate",
        "stump": "stumpings",
        "lbw": "bowled_lbw",
        "catch": "catches",
        "econ": "economy",
        "wicket": "wickets",
        "maiden": "maidens",
    }

    ####peak data handling
    player_df_real = pd.DataFrame()
    points_df_real = pd.DataFrame()
    player_df_predicted = pd.DataFrame()
    points_df_predicted = pd.DataFrame()
    match_groups = output.groupby("match_id")
    for i in list(match_groups.groups.keys()):
        df1 = match_groups.get_group(i)

        # print(df1['target_column'].unique())
        format = [i for i in list(df1["target_column"].unique()) if "run" in i][
            0
        ].split("_")[0]
        player_ids = list(df1["player_id"].unique())
        grouping = df1.groupby("target_column")
        # print(grouping.get_group(list(grouping.groups.keys())[0]))
        # break
        dfx = pd.DataFrame(index=range(len(df1["name"].unique())))

        dfr = pd.DataFrame(index=range(len(df1["name"].unique())))
        dfx.set_index(df1["name"].unique(), inplace=True)
        dfr.set_index(df1["name"].unique(), inplace=True)
        dfr["balls"] = 0
        for j in grouping.groups.keys():
            # print(j)
            df_feat = grouping.get_group(j)

            df_feat.set_index("name", inplace=True)
            # print(df_feat)
            df_feat = df_feat[~df_feat.index.duplicated(keep="first")]
            # print(df_feat)
            try:
                key = [m for m in lst_feature.keys() if m in j][0]
            except:
                continue
            key = lst_feature[key]
            # print(key)

            dfx[key] = df_feat.reindex(dfx.index, fill_value=0)["predicted_value"]
            dfr[key] = df_feat.reindex(dfx.index, fill_value=0)["true_value"]
            dfr["balls"] += df_feat["balls"]

        dfx["pred_points"] = points_calculator(
            format=format,
            runs=dfx["runs"],
            boundaries=dfx["boundaries"],
            sixes=dfx["sixes"],
            strike_rate=dfx["strike_rate"],
            wickets=dfx["wickets"],
            bowled_lbw=dfx["bowled_lbw"],
            maidens=dfx["maidens"],
            economy=dfx["economy"],
            catches=dfx["catches"],
            stumpings=dfx["stumpings"],
            balls_bowled=12,
        )
        dfx["real_points"] = points_calculator(
            format=format,
            runs=dfr["runs"],
            boundaries=dfr["boundaries"],
            sixes=dfr["sixes"],
            strike_rate=dfr["strike_rate"],
            wickets=dfr["wickets"],
            bowled_lbw=dfr["bowled_lbw"],
            maidens=dfr["maidens"],
            economy=dfr["economy"],
            catches=dfr["catches"],
            stumpings=dfr["stumpings"],
            balls_bowled=12,
        )
        dfx = dfx.reset_index().rename(columns={"index": "name"})
        # print(dfx.sort_values('real_points').iloc[1]['real_points'])
        df_real = dfx.sort_values("real_points", ascending=False).iloc[:11]
        df_pred = dfx.sort_values("pred_points", ascending=False).iloc[:11]
        # print(df_real)
        # print({'player'+str(i):df_real.iloc[i].index.values[0] for i in range(11)})
        player_df_real = pd.concat(
            [
                player_df_real,
                pd.DataFrame(
                    {
                        "player" + str(i) + "_real": df_real.iloc[i]["name"]
                        for i in range(11)
                    },
                    index=[i],
                ),
            ]
        )
        player_df_predicted = pd.concat(
            [
                player_df_predicted,
                pd.DataFrame(
                    {"player" + str(i): df_pred.iloc[i]["name"] for i in range(11)},
                    index=[i],
                ),
            ]
        )
        points_df_real = pd.concat(
            [
                points_df_real,
                pd.DataFrame(
                    {
                        "player"
                        + str(i)
                        + "real_points": df_real.iloc[i]["real_points"]
                        for i in range(11)
                    },
                    index=[i],
                ),
            ]
        )
        points_df_predicted = pd.concat(
            [
                points_df_predicted,
                pd.DataFrame(
                    {
                        "player"
                        + str(i)
                        + "predicted_points": df_pred.iloc[i]["pred_points"]
                        for i in range(11)
                    },
                    index=[i],
                ),
            ]
        )

    ####final prediction area
    final_predictions = pd.DataFrame(
        columns=[
            "index",
            "Match Date",
            "Team",
            "Team 2",
            "Predicted Player 1",
            "Predicted Player 1 Points",
            "Predicted Player 2",
            "Predicted Player 2 Points",
            "Predicted Player 3",
            "Predicted Player 3 Points",
            "Predicted Player 4",
            "Predicted Player 4 Points",
            "Predicted Player 5",
            "Predicted Player 5 Points",
            "Predicted Player 6",
            "Predicted Player 6 Points",
            "Predicted Player 7",
            "Predicted Player 7 Points",
            "Predicted Player 8",
            "Predicted Player 8 Points",
            "Predicted Player 9",
            "Predicted Player 9 Points",
            "Predicted Player 10",
            "Predicted Player 10 Points",
            "Predicted Player 11",
            "Predicted Player 11 Points",
            "Dream Team Player 1",
            "Dream Team Player 1 Points",
            "Dream Team Player 2",
            "Dream Team Player 2 Points",
            "Dream Team Player 3",
            "Dream Team Player 3 Points",
            "Dream Team Player 4",
            "Dream Team Player 4 Points",
            "Dream Team Player 5",
            "Dream Team Player 5 Points",
            "Dream Team Player 6",
            "Dream Team Player 6 Points",
            "Dream Team Player 7",
            "Dream Team Player 7 Points",
            "Dream Team Player 8",
            "Dream Team Player 8 Points",
            "Dream Team Player 9",
            "Dream Team Player 9 Points",
            "Dream Team Player 10",
            "Dream Team Player 10 Points",
            "Dream Team Player 11",
            "Dream Team Player 11 Points",
            "Total Points Predicted",
            "Total Dream Team Points",
            "Total points MAE",
        ]
    )

    for i in points_df_real.index:
        for k in range(11):
            pred = "Predicted Player " + str(k + 1)
            real = "Dream Team Player " + str(k + 1)
            pred_col = f"player{k}"
            real_col = f"player{k}_real"
            final_predictions.loc[i, pred] = player_df_predicted[pred_col][i]
            final_predictions.loc[i, pred + " Points"] = points_df_predicted[
                pred_col + "predicted_points"
            ][i]
            final_predictions.loc[i, real] = player_df_real[real_col][i]
            final_predictions.loc[i, real + " Points"] = points_df_real[
                pred_col + "real_points"
            ][i]

    # Initialize the new DataFrame
    new_df = pd.DataFrame()

    # Iterate over the indices of `final_predictions`
    for i in final_predictions.index:
        # Create a new row dictionary
        final = {
            "index": i,
            "Match Date": mapping[i][2],
            "Team": list(mapping[i][0])[0],
            "Team 2": list(mapping[i][1])[0],
        }

        # Append the new row to the DataFrame
        new_df = pd.concat([new_df, pd.DataFrame([final])], ignore_index=True)

    new_df.set_index("index", inplace=True)
    final_predictions["Match Date"] = new_df["Match Date"]
    final_predictions["Team"] = new_df["Team"]
    final_predictions["Team 2"] = new_df["Team 2"]

    predlist = []
    realist = []
    for k in range(11):
        pred = "Predicted Player " + str(k + 1) + " Points"
        real = "Dream Team Player " + str(k + 1) + " Points"
        predlist.append(pred)
        realist.append(real)

    final_predictions["Total Points Predicted"] = final_predictions[predlist].sum(
        axis=1
    )
    final_predictions["Total Dream Team Points"] = final_predictions[realist].sum(
        axis=1
    )
    final_predictions["Total points MAE"] = abs(
        final_predictions["Total Points Predicted"]
        - final_predictions["Total Dream Team Points"]
    )
    final_predictions.to_csv("Final_Result.csv")
