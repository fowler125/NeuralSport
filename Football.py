import logging
import nfl_data_py as nfl
import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler




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
   
    #logging.info(f"Retrieving weekly stats data for years: {years}")
    data = nfl.import_weekly_data(years)
    data.to_csv(f"data/football/stats_{years}.csv")
    return data
def NGSdata(st_tpe:str, years:list):
    data = nfl.import_ngs_data(stat_type = st_tpe,years=years)
    data.to_csv(f"data/football/{st_tpe}_NGS{years}.csv")
    return data
def grabPlayer(first: str, last: str, data: pd.DataFrame) -> pd.DataFrame:
    # Combine first and last name to match the format in player_name column
    full_name = f"{first[0].upper()}.{last}"
    
    # Filter the DataFrame based on the player's name
    player_data = data[data['player_name'] == full_name]
    
    # If no data is found, try matching with player_display_name
    if player_data.empty:
        full_display_name = f"{first} {last}"
        player_data = data[data['player_display_name'] == full_display_name]
    
    return player_data
def grabPosition(group:str, data: pd.DataFrame) -> pd.DataFrame:

    group_data = data[data['position'] == group]

    return group_data
def prepare_data(position_group_data):
    # Select relevant features for predicting passing yards
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
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Create and train the model
    model = create_model(X_train.shape[1])
    
    # Add early stopping
    early_stopping = keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
    
    history = model.fit(
        X_train_scaled, y_train,
        epochs=200,
        batch_size=32,
        validation_split=0.2,
        callbacks=[early_stopping],
        verbose=1
    )
    
    # Evaluate the model
    test_loss, test_mae = model.evaluate(X_test_scaled, y_test)
    print(f"Test Loss: {test_loss}")
    print(f"Test Mean Absolute Error: {test_mae}")
    
    return model, scaler, history
def predict_passing_yards(model, scaler, new_data):
    new_data_scaled = scaler.transform(new_data)
    predictions = model.predict(new_data_scaled)
    return predictions.flatten()
    
def main():
    #print(nfl.import_pbp_data([2024]))
    #print(nfl.import_seasonal_pfr('pass', [2024]))
    print(nfl.see_weekly_cols())
    week_df = weeklyStats([2019,2020,2021,2022,2023,2024])
    #result = grabPlayer("Aaron", "Rodgers", week_df)
    #print(result)
    print(grabPosition('QB',week_df))
    #NGSdata('passing',[2024])
    
    
    #------------------------------------------------------------------
    # Get all QB data
    qb_data = grabPosition('QB', week_df)
    
    # Prepare the data
    X, y = prepare_data(qb_data)
    
    # Train the model
    model, scaler, history = train_model(X, y)
    
    # Example: Make predictions for a specific player
    player_data = grabPlayer("Aaron", "Rodgers", qb_data)
    player_features = player_data[X.columns]  # Ensure we use the same features as in training
    predicted_yards = predict_passing_yards(model, scaler, player_features)
    print(f"Predicted passing yards for Aaron Rodgers: {predicted_yards}")
    
    # Example: Make predictions for a new game
    new_game_stats = pd.DataFrame({
        'completions': [25], 'attempts': [40], 'passing_tds': [2], 'interceptions': [1],
        'sacks': [2], 'sack_yards': [15], 'passing_air_yards': [200],
        'passing_yards_after_catch': [100], 'passing_first_downs': [15],
        'passing_epa': [10.5], 'pacr': [0.8]
    })
    predicted_yards = predict_passing_yards(model, scaler, new_game_stats)
    print(f"Predicted passing yards for new game: {predicted_yards[0]:.2f}")

    return model, scaler

if __name__ == "__main__":
    main()
