import logging
import nfl_data_py as nfl
import numpy as np
import pandas as pd




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
    logging.info(f"Retrieving weekly PFR data for {stat_type} and years: {years}")
    data = nfl.import_weekly_pfr(stat_type, years)
    data.to_csv(f"data/football/{stat_type}_{years}.csv")
    return data

def main():
    #print(nfl.import_pbp_data([2024]))
    #print(nfl.import_seasonal_pfr('pass', [2024]))
    weeklyPfr('pass',[2024])

if __name__ == "__main__":
    main()
