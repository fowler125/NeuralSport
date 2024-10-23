import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import keras
from tensorflow.keras import models, datasets, layers, optimizers, ops
from sklearn.model_selection import train_test_split

class KerasPitcherModel:
    def __init__(self,id) -> None:
        self.id = id
    def plotting(self):
        """ for loop to go thru all the features, and plot them in a graph, x axis = features, y axis= zone"""
        pitcher_df = pd.read_csv(f"data/clean/{self.id}.csv")
        pitcher_df_X = pitcher_df[["pitch_type","release_speed","release_pos_x","release_pos_z","spin_dir","spin_rate_deprecated","break_angle_deprecated","break_length_deprecated","stand","p_throws","type","balls","strikes","pfx_x","pfx_z","plate_x","plate_z","on_3b","on_2b","on_1b","outs_when_up","inning","vx0","vy0","vz0","ax","ay","az","sz_top","sz_bot","release_spin_rate","release_extension","release_pos_y","at_bat_number","pitch_number","pitch_name","spin_axis"]]
        pitcher_df_Y = pitcher_df[["zone"]]

        for i in pitcher_df.columns:
            plt.scatter(pitcher_df[i],pitcher_df_Y)
            plt.show()


    def new_setup(self):
        """
        param :: self
        We no longer need to use reduced data, as we have already cleaned the data, so no need to split it up
        -DO NOT HARDCODE ANY VALUES, previous iteration had hardcoded python splits [:xxx], this is not dynamic, and isnt something we want, so from now 
        on we will use the split method off the keras documentation:
        https://keras.io/api/models/model_training_apis/

        Different, should use early stopping, nth number of epochs

        Hyperparamater Tuning as well needs to be implemented 
        """
        pitcher_df = pd.read_csv(f"data/clean/{self.id}.csv")
        pitcher_df_X = pitcher_df[["pitch_type","release_speed","release_pos_x","release_pos_z","spin_dir","spin_rate_deprecated","break_angle_deprecated","break_length_deprecated","stand","p_throws","type","balls","strikes","pfx_x","pfx_z","plate_x","plate_z","on_3b","on_2b","on_1b","outs_when_up","inning","vx0","vy0","vz0","ax","ay","az","sz_top","sz_bot","release_spin_rate","release_extension","release_pos_y","at_bat_number","pitch_number","pitch_name","spin_axis"]]
        pitcher_df_Y = pitcher_df[["zone"]]

        print(len(pitcher_df_X.columns))

        test = keras.Input(shape = (pitcher_df_X.shape[1],))

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




    def setup_pitcher_df(self):
        """
        :param self (int) players id value, important for identifying player and csv location
        """
        pitcher_df = pd.read_csv(f"data/clean/{self.id}.csv")
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
p1.new_setup()