import pandas as pd
from pybaseball import statcast_pitcher, playerid_lookup, pitching_stats_range, statcast_pitcher_pitch_arsenal
from dict import name_id, seasons

def grabStatCast(start_date, end_date, playerID):
    """
    This function grabs Statcast data for a given player within a date range.
    The data includes metrics such as Spin Rate (SR), Exit Velocity (EV), pitch X, Y, and Z coordinates, and more.
    The function statcast(start_dt, end_dt) pulls this data from baseballsavant.com.

    :param start_date: Enter a start date
    :param end_date: Enter an end date
    :param playerID: Enter a player's ID, this can be obtained from playerIDLookup function
    :return: A dataframe with statcast pitches
    """
    data = statcast_pitcher(start_dt=start_date, end_dt=end_date, player_id=playerID)
    data.to_csv(f"data/unclean/{playerID}.csv")
    print("Data Collection is Finished")
    return data

def playerIDLookup(lastname, firstname=None, fuzz=False) -> pd.DataFrame:
    """
    This function looks up a player's ID using their last name and optionally their first name.
    If the player's name contains special characters, it will attempt a fuzzy search.

    :param lastname: Enter the last name of a player (Be careful of players with special characters)
    :param firstname: Enter the first name of the player, Firstname is optional
    :return: returns a players dataframe, all that is important is a value named {key_mlbam}, this is the players ID
    """
    data = playerid_lookup(lastname, firstname, fuzz)
    if data.empty:
        print("The desired player may have special characters contained inside their name, please check list of players below:\n")
        return playerid_lookup(lastname, firstname, fuzzy=True)
    else:
        player_id = data["key_mlbam"].values[0]
        player_name = f"{firstname} {lastname}" if firstname else lastname
        name_id[player_id] = player_name
        return data

def grabPitchStats():
    data = pitching_stats_range("2024-03-20", "2024-09-30")
    data.to_csv(f"data/unclean/pitch_stats_2024.csv")
def statCastArsenal():
    data = statcast_pitcher_pitch_arsenal(2024,minP=100,arsenal_type="n_")
    data.to_csv(f"data/unclean/pitch_arsenal_2024.csv")

def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    opening_day = '2021-03-28'
    today = '2024-09-19'
    
    # Use player ID lookup to grab the ID of the player which is needed for looking up the stats via statcast
    # Lastname required, firstname optional, fuzz for possible discrepancies in name
    player_lookup_df = playerIDLookup('skubal', 'tarik')
    id = player_lookup_df["key_mlbam"].values[0]
    print(id)
    grabStatCast(opening_day, today, playerID=id)
    
    grabPitchStats()
    statCastArsenal()
    
    # pitcher = KerasModelMLB(id)
    # pitcher.setup_pitcher_df()

if __name__ == '__main__':
    main()