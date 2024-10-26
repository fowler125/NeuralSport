
# KerasModelMLB.py

This module contains a class for building and training a Keras model for predicting baseball pitch outcomes.

## Class: KerasPitcherModel

### Description

This class represents a Keras model for predicting baseball pitch outcomes. It provides methods for loading data, preprocessing, building and training the model, and making predictions.

### Attributes

* `id`: The ID of the pitcher.

### Methods

#### `__init__(self, id)`

Initializes the KerasPitcherModel instance with the given pitcher ID.

* **Parameters:**
  - `id` (int): The ID of the pitcher.
* **Returns:**
  - None.

#### `new_setup(self)`

Loads the data for the given pitcher, preprocesses it, and sets up the model.

* **Parameters:**
  - None.
* **Returns:**
  - None.

#### `correlation_matrix(self, data)`

Creates a correlation matrix for the given data.

* **Parameters:**
  - `data` (pd.DataFrame): The data for which to create the correlation matrix.
* **Returns:**
  - None.

#### `plotting(self)`

Plots the data for the given pitcher.

* **Parameters:**
  - None.
* **Returns:**
  - None.

#### `pitch_plotting(self, data)`

Plots the pitch data for the given pitcher.

* **Parameters:**
  - `data` (pd.DataFrame): The pitch data for the given pitcher.
* **Returns:**
  - None.

#### `setup_pitcher_df(self)`

Sets up the pitcher data frame.

* **Parameters:**
  - None.
* **Returns:**
  - None.

### Usage

To use the KerasPitcherModel class, you can create an instance of it and call its methods as needed. For example:

```python
from KerasModelMLB import KerasPitcherModel

# Create an instance of the KerasPitcherModel class
model = KerasPitcherModel(656302)

# Load the data and set up the model
model.new_setup()

# Create a correlation matrix for the data
model.correlation_matrix(model.pitcher_df_X)

# Plot the data
model.plotting()
## Dependencies

This module depends on the following libraries:

- `keras`
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `sklearn`

## License

This module is licensed under the MIT License.
```

Please note that the above documentation is based on the code provided in the `KerasModelMLB.py` file. If there are any additional methods or details that are not included in the code, you may need to add them to the documentation.