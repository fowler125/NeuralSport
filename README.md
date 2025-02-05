# Neural Sport

This repository provides tools to analyze baseball player statistics using the `pybaseball` library. The functions included allow you to fetch Statcast data, look up player IDs, and retrieve specific pitching statistics.

## Requirements

- Python 3.x
- pandas
- pybaseball

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/baseball-stats-analyzer.git
cd baseball-stats-analyzer
```

2. Install the required libraries:

```bash
pip install pandas pybaseball
```

## Usage

### Functions

#### `grabStatCast(start_date, end_date=None, playerID=None)`

Fetches Statcast data for a given date range and player ID.

- **Parameters:**
  - `start_date` (str): The start date for fetching data.
  - `end_date` (str, optional): The end date for fetching data. Defaults to `None`.
  - `playerID` (int, optional): The player's ID. Defaults to `None`.
- **Returns:** 
  - A DataFrame with Statcast pitches.

#### `playerIDLookup(lastname, firstname=None, fuzz=False)`

Looks up player IDs based on the player's last name and optionally the first name.

- **Parameters:**
  - `lastname` (str): The player's last name.
  - `firstname` (str, optional): The player's first name. Defaults to `None`.
  - `fuzz` (bool, optional): Whether to use fuzzy matching. Defaults to `False`.
- **Returns:** 
  - A DataFrame with player information, including the player's ID.

#### `grabPitches()`

Fetches pitching data for a specific date and player, and prints a modified DataFrame with selected columns.

### Example

```python
from pybaseball import statcast, playerid_lookup, statcast_pitcher
import pandas as pd

def grabStatCast(start_date, end_date=None, playerID=None):
    data = statcast_pitcher(start_dt=start_date, end_dt=end_date, player_id=playerID)
    return data

def playerIDLookup(lastname, firstname=None, fuzz=False):
    data = playerid_lookup(lastname, firstname, fuzz)
    if data.empty:
        return playerid_lookup(lastname, firstname, fuzzy=True)
    else:
        return data

def grabPitches():
    pitcher_df = statcast_pitcher('2024-06-10', '2024-06-10', player_id=621244)
    modified_df = pitcher_df[['pitch_type', 'game_date', 'release_speed', 'player_name', 'inning', 'balls', 'strikes', 'on_3b', 'on_2b', 'on_1b']]
    print(modified_df)

def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(playerIDLookup('berríos', 'josé'))

if __name__ == '__main__':
    main()
```

### Running the Code

To run the code, simply execute the main script:

```bash
python main.py
```

This will look up the player ID for "José Berríos" and print the relevant information.

## Contributing and Helpful Resources

https://github.com/toddrob99/MLB-StatsAPI/blob/master/statsapi/endpoints.py
API endpoints for MLB API

https://github.com/zero-sum-seattle/python-mlb-statsapi


https://baseballsavant.mlb.com/statcast_search

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
