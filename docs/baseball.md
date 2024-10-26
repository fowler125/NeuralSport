# Baseball.py

This module contains functions for working with baseball data.

## Functions

### `grabStatCast(start_date, end_date=None, playerID=None)`

Fetches Statcast data for a given date range and player ID.

- **Parameters:**
  - `start_date` (str): The start date for fetching data.
  - `end_date` (str, optional): The end date for fetching data. Defaults to `None`.
  - `playerID` (int, optional): The player's ID. Defaults to `None`.
- **Returns:**
  - A DataFrame with Statcast pitches.

### `playerIDLookup(lastname, firstname=None, fuzz=False)`

Looks up player IDs based on the player's last name and optionally the first name.

- **Parameters:**
  - `lastname` (str): The player's last name.
  - `firstname` (str, optional): The player's first name. Defaults to `None`.
  - `fuzz` (bool, optional): Whether to use fuzzy matching. Defaults to `False`.
- **Returns:**
  - A DataFrame with relevant information.

### `grabPitches()`

Fetches pitching data for a specific date and player, and prints a modified DataFrame with selected columns.

- **Parameters:**
  - None.
- **Returns:**
  - None.

### `main()`

The entry point of the script.

- **Parameters:**
  - None.
- **Returns:**
  - None.

## Usage

To use the functions in this module, you can import them and call them as needed. For example:

```python
from Baseball import grabStatCast, playerIDLookup, grabPitches

# Fetch Statcast data for a specific date and player
data = grabStatCast('2024-06-10', '2024-06-10', playerID=621244)

# Look up player IDs based on the player's last name and first name
data = playerIDLookup('berríos', 'josé')

# Fetch pitching data for a specific date and player, and print a modified DataFrame
grabPitches()