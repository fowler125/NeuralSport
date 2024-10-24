import logging
import nfl_data_py as nfl
import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy import stats



def weeklyPfr(stat_type:str,years:list):
    '''
    Retrieve weekly PFR data for a specific statistic type and years.

    Parameters:
    - stat_type (str): The type of statistic to retrieve.
    - years (list): A list of years to retrieve the data for.

    Returns:
    None

    Saves the retrieved data to a CSV file in the 'data/football' directory with a filename based on the statistic type and years.
    '''
    #logging.info(f"Retrieving weekly PFR data for {stat_type} and years: {years}")
    data = nfl.import_weekly_pfr(stat_type, years)
    data.to_csv(f"data/football/{stat_type}_{years}.csv")
    return data

def weeklyStats(years:list):

    '''
    Retrieve weekly stats data for a list of years.

    Parameters:
    - years (list): A list of years to retrieve the data for.

    Returns:
    None

    Saves the retrieved data to a CSV file in the 'data/football' directory with a filename based on the years.
    '''
    data = nfl.import_weekly_data(years)
    data.to_csv(f"data/football/stats_{years}.csv")
    return data
def NGSdata(st_tpe:str, years:list):
    data = nfl.import_ngs_data(stat_type = st_tpe,years=years)
    data.to_csv(f"data/football/{st_tpe}_NGS{years}.csv")
    return data
def grabPlayer(first: str, last: str, data: pd.DataFrame) -> pd.DataFrame:
    full_name = f"{first[0].upper()}.{last}"
    player_data = data[data['player_name'] == full_name]
    if player_data.empty:
        full_display_name = f"{first} {last}"
        player_data = data[data['player_display_name'] == full_display_name]
    return player_data
def grabPosition(group: str, data: pd.DataFrame) -> pd.DataFrame:
    return data[data['position'] == group]

def prepare_data(position_group_data):
    features = [
        'completions', 'attempts', 'passing_tds', 'interceptions',
        'sacks', 'sack_yards', 'passing_air_yards', 'passing_yards_after_catch',
        'passing_first_downs', 'passing_epa', 'pacr'
    ]
    X = position_group_data[features]
    y = position_group_data['passing_yards']
    return X, y
    
    
def create_model(input_shape):
    model = keras.Sequential([
        keras.layers.Dense(128, activation='relu', input_shape=(input_shape,)),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1)  # Output layer (predicting a single value: passing yards)
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    return model
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    model = create_model(X_train.shape[1])
    early_stopping = keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
    history = model.fit(
        X_train_scaled, y_train,
        epochs=200,
        batch_size=32,
        validation_split=0.2,
        callbacks=[early_stopping],
        verbose=1
    )
    
    
    # Calculate MAPE for accuracy score
    y_pred = model.predict(X_test_scaled).flatten()
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test,y_pred))
    r2 = r2_score(y_test,y_pred)

    accuracy = 1 - (mae / np.mean(y_test))
    
    print(f"Mean Absolute Error: {mae:.2f} yards")
    print(f"Root Mean Squared Error: {rmse:.2f} yards")
    print(f"R-squared Score: {r2:.4f}")
    print(f"Custom Accuracy: {accuracy:.2%}")
    
    return model, scaler, history, (mae, rmse, r2, accuracy)

def predict_passing_yards(model, scaler, new_data):
    new_data_scaled = scaler.transform(new_data)
    predictions = model.predict(new_data_scaled)
    return predictions.flatten()

def predict_next_game(player_data, model, scaler):

    
    features = [
        'completions', 'attempts', 'passing_tds', 'interceptions',
        'sacks', 'sack_yards', 'passing_air_yards', 'passing_yards_after_catch',
        'passing_first_downs', 'passing_epa', 'pacr'
    ]
    avg_stats = player_data[features].mean().to_frame().T
    
    # Make prediction
    next_game_prediction = predict_passing_yards(model, scaler, avg_stats)
    
    # Calculate confidence interval
    all_yards = player_data['passing_yards']
    pred_std = np.std(all_yards)
    degrees_of_freedom = len(all_yards)-1
    confidence_level = 0.95
    t_value = stats.t.ppf((1+confidence_level)/2,degrees_of_freedom)
    margin_of_error = t_value * (pred_std/np.sqrt(len(all_yards)))
    confidence_interval = (
        next_game_prediction[0]-margin_of_error,
        next_game_prediction[0]+margin_of_error
    )
    
    """
    confidence_interval = stats.t.interval(alpha=0.95, df=len(last_games)-1,
                                           loc=next_game_prediction[0],
                                           scale=pred_std)
    """
    return next_game_prediction[0], confidence_interval
def main():
    #print(nfl.import_pbp_data([2024]))
    #print(nfl.import_seasonal_pfr('pass', [2024]))
    #print(nfl.see_weekly_cols())
    week_df = weeklyStats([2019,2020,2021,2022,2023,2024])
    #result = grabPlayer("Aaron", "Rodgers", week_df)
    #print(result)
    #print(grabPosition('QB',week_df))
    #NGSdata('passing',[2024])
    
    
    #------------------------------------------------------------------
    # Get all QB data
    qb_data = grabPosition('QB', week_df)
    
    # Prepare the data
    X, y = prepare_data(qb_data)
    
    # Train the model
    model, scaler, history,metrics= train_model(X, y)

    mae,rmse,r2,accuracy = metrics

    first_name = "Kirk"
    last_name = "Cousins"
    
    # Example: Make predictions for a specific player
    player_data = grabPlayer(first_name, last_name, qb_data)

    player_data.to_csv(f"data/football/{first_name}{last_name}.csv")

    predicted_yards, confidence_interval = predict_next_game(player_data, model, scaler)
    print(f"\nModel Performance Metrics:")

    #avg absolute difference between predicted and actual yards
    print(f"Mean Absolute Error: {mae:.2f} yards")

    #gives the square root of the average squared difference between predicted and actual yards
    print(f"Root Mean Squared Error: {rmse:.2f} yards")
    
    #how much variance in the data in our model. ranges from 0-1
    print(f"R-squared Score: {r2:.4f}")
    print(f"Custom Accuracy: {accuracy:.2%}")
    print(f"\nPredicted passing yards for {first_name} {last_name} in his next game: {predicted_yards:.2f}")
    print(f"95% Confidence Interval: {confidence_interval[0]:.2f} to {confidence_interval[1]:.2f}")
    return model, scaler
    

if __name__ == "__main__":
    main()
