from pybaseball import statcast
from pybaseball import playerid_lookup
from pybaseball import statcast_pitcher
from pybaseball import pitching_stats
from pybaseball import batting_stats_range
from data import dataCleaner
import Models
import pandas as pd




def grabStatCast(start_date,end_date=None,playerID=None):
    """
    Statcast data include pitch-level features such as Perceived Velocity (PV),
    Spin Rate (SR), Exit Velocity (EV), pitch X, Y, and Z coordinates, and more.
    The function statcast(start_dt, end_dt) pulls this data from baseballsavant.com.

    :param start_date: Enter a start date
    :param end_date: Enter a end date
    :param playerID: Enter a player's ID, this can be obtained from playerIDLookup function
    :return: A dataframe with statcast pitches
    """
    data = statcast_pitcher(start_dt=start_date, end_dt=end_date,player_id=playerID)
    data.to_csv(f"data/unclean/{playerID}.csv")
    print("Data Collection is Finished")
    return data

def playerIDLookup(lastname,firstname=None,fuzz=False) -> pd.DataFrame:
    """
    :param lastname:Enter the lastname of a player (Be careful of players with special characters)
    :param firstname:Enter the first name of the player, Firstname is optional
    :return: returns a players dataframe, all that is important is a value named {key_mlbam}, this is the players ID
    """
    
    data = playerid_lookup(lastname,firstname,fuzz)
    if data.empty:
        print("The desired player may have special characters contained inside their name, please check list of players below:","\n")
        return playerid_lookup(lastname,firstname,fuzzy=True)
    else:
        return data
    


def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    opening_day = '2020-03-28'
    today = '2023-09-19'
    
    #use player id lookup to grab the id of the player which is needed for looking up the stats via statcast
    #lastname require, firstname optional, fuzz for possible discrepencies in name
    player_lookup_df = playerIDLookup('scherzer','max')
    id = player_lookup_df["key_mlbam"].values[0]
    print(id)
    grabStatCast(opening_day,today,playerID=id)
    
    #pitcher = KerasModelMLB(id)
    #pitcher.setup_pitcher_df()


if __name__ == '__main__':
    main()