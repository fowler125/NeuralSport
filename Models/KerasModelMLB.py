import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import keras
from tensorflow.keras import models, datasets, layers, optimizers, ops

class KerasPitcherModel:
    def __init__(self,id) -> None:
        self.id = id
    
    def setup_pitcher_df(self):
        """
        :param id (int) players id value, important for identifying player and csv location
        """
        pitcher_df = pd.read_csv(f"data/unclean/{self.id}.csv")
        reduced_df_X = pitcher_df[["vx0","vy0","vz0"]]
        reduced_df_Y = pitcher_df[["zone"]]

        X_train, X_valid, X_test = reduced_df_X[:31668], reduced_df_X[31668:38454], reduced_df_X[38454:]
        y_train, y_valid, y_test = reduced_df_Y[:31668], reduced_df_Y[31668:38454], reduced_df_Y[38454:]

        test = keras.Input(shape = (3,))

        dense = layers.Dense(64, activation="relu")
        x = dense(test)

        StrikeZone = layers.Dense(13)(x)

        model = keras.Model(inputs=test, outputs=StrikeZone, name="mnist_model")

        model.compile(
            loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            optimizer=keras.optimizers.RMSprop(),
            metrics=["accuracy"],
        )

        history = model.fit(X_train, y_train, epochs=100)

        test_scores = model.evaluate(X_test, y_test, verbose=2)
        print("Test loss:", test_scores[0])
        print("Test accuracy:", test_scores[1])





p1 = KerasPitcherModel(554430)
p1.setup_pitcher_df()