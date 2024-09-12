import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import keras
from tensorflow.keras import models, datasets, layers, optimizers, ops

def setup_pitcher_df(id):
    """
    :param id (int) players id value, important for identifying player and csv location
    """
    
