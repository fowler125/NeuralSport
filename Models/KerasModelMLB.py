import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import keras
import seaborn as sns
from tensorflow.keras import models, datasets, layers, optimizers, ops
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.callbacks import EarlyStopping
import matplotlib.image as mpimg

features_dict = {
    "reduced":["vx0","vy0","vz0","ax","ay","az"],
    "full":["pitch_type","release_speed","release_pos_x","release_pos_z","spin_dir",
            "spin_rate_deprecated","break_angle_deprecated","break_length_deprecated",
            "zone","stand","p_throws","type","balls","strikes","pfx_x","pfx_z","plate_x","plate_z",
            "on_3b","on_2b","on_1b","outs_when_up","inning","vx0","vy0","vz0","ax","ay","az","sz_top",
            "sz_bot","release_spin_rate","release_extension","release_pos_y","at_bat_number",
            "pitch_number","pitch_name","spin_axis"],
    "velocity":["vx0","vy0","vz0"],
    "numerical_only":["vx0","vy0","vz0","ax","ay","az","pfx_x","pfx_z","plate_x","plate_z"],
    "plotting_data":["vx0","vy0","vz0","ax","ay","az","pfx_x","pfx_z","plate_x","plate_z","sz_top","sz_bot"]
}
class KerasPitcherModel:
    def __init__(self,id) -> None:
        self.id = id
    def deprecated_plotting(self):
        """ for loop to go thru all the features, and plot them in a graph, x axis = features, y axis= zone"""
        pitcher_df = pd.read_csv(f"data/clean/{self.id}.csv")
        pitcher_df_X = pitcher_df[["pitch_type","release_speed","release_pos_x","release_pos_z","spin_dir","spin_rate_deprecated","break_angle_deprecated","break_length_deprecated","stand","p_throws","type","balls","strikes","pfx_x","pfx_z","plate_x","plate_z","on_3b","on_2b","on_1b","outs_when_up","inning","vx0","vy0","vz0","ax","ay","az","sz_top","sz_bot","release_spin_rate","release_extension","release_pos_y","at_bat_number","pitch_number","pitch_name","spin_axis"]]
        pitcher_df_Y = pitcher_df[["zone"]]

        for i in pitcher_df.columns:
            plt.scatter(pitcher_df[i],pitcher_df_Y)
            plt.show()

    def correlation_matrix(self,data:pd.DataFrame):
        corr_matrix = data.corr()
        plt.figure(figsize=(10,8))
        sns.heatmap(corr_matrix, annot=True,cmap='coolwarm',square=True)
        plt.title("Correlation Matrix")
        plt.show()
    def deprecated_pitch_plotting(self,data:pd.DataFrame): 
        
        
        # Create a new figure
        plt.figure(figsize=(8, 8))
        
        # Get the maximum and minimum x and z values from the data
        x_max = data['plate_x'].max()
        x_min = data['plate_x'].min()
        z_max = data['plate_z'].max()
        z_min = data['plate_z'].min()
        
        # Calculate the range of the x and z values
        x_range = x_max - x_min
        z_range = z_max - z_min
        
        # Calculate the maximum range of the x and z values
        max_range = max(x_range, z_range)
        
        # Calculate the scaling factor for the x and z values
        x_scale = (400 / max_range)
        z_scale = (400 / max_range)
        
        # Define a dictionary to map zone numbers to colors
        zone_colors = {
            1: 'red',
            2: 'orange',
            3: 'yellow',
            4: 'green',
            5: 'blue',
            6: 'purple',
            7: 'pink',
            8: 'brown',
            9: 'gray',
            10: 'black',
            11: 'white'
        }
        
        # Plot each pitch using scaled plate_x and plate_z coordinates and zone-based colors
        for index, row in data.iterrows():
            zone = row['zone']
            color = zone_colors.get(zone, 'black')
            plt.scatter((row['plate_x'] - (x_max + x_min) / 2) * x_scale, (row['plate_z'] - (z_max + z_min) / 2) * z_scale, c=color, s=50, alpha=0.5)
        
        # Add a line at the origin (middle of the plot)
        plt.axvline(0, color='k', linestyle='--', alpha=0.5)
        plt.axhline(0, color='k', linestyle='--', alpha=0.5)
        
        # Set the limits of the plot to be symmetric around the origin
        plt.xlim(-400, 400)
        plt.ylim(-400, 400)
        
        # Show the plot
        plt.show()
        
    def pitcher_plotting(self,data:pd.DataFrame):
        # Filter the data to only include rows with 'ball' or 'called_strike' in the 'description' column
        data_filter = data[(data['description'].isin(['ball', 'called_strike'])) & (~data['sz_top'].isna()) & (~data['sz_bot'].isna())]

        fig,ax = plt.subplots(figsize=(8,8))

        x_max = data['plate_x'].max()
        x_min = data['plate_x'].min()
        z_max = data['plate_z'].max()
        z_min = data['plate_z'].min()

        # Plot the points
        sns.scatterplot(x='plate_x', y='plate_z', hue='type', data=data, alpha=0.5, ax=ax)

        # Plot the strike zone rectangle
        strike_zone_rect = plt.Rectangle((-0.7083, data_filter['sz_bot'].median()), 1.4166, data['sz_top'].median() - data['sz_bot'].median(), alpha=0.5, edgecolor='black', facecolor='none', linewidth=2)
        ax.add_patch(strike_zone_rect)
        """ax.add_patch(plt.Rectangle((-0.7083, data['sz_bot'].median()), 
                                   1.4166, data['sz_top'].median() - data['sz_bot'].median(), 
                                   alpha=0, edgecolor='black', facecolor='none', linewidth=2))"""
        # Set the title and labels
        ax.set_title('Called Balls and Strikes')
        ax.set_xlabel('Horizontal Position')
        ax.set_ylabel('Vertical Position')

        # Set the color palette
        sns.set_palette(['lightskyblue', 'cornflowerblue'])

        # Set the aspect ratio
        ax.set_aspect('equal')

        # Remove the legend
        #ax.get_legend().remove()

        # Set the font family
        plt.rcParams['font.family'] = 'serif'
        plt.show()

        # Facet by type
        for type in data_filter['type'].unique():
            fig, ax = plt.subplots(figsize=(8, 8))
            sns.scatterplot(x='plate_x', y='plate_z', hue='type', data=data_filter[data_filter['type'] == type], alpha=0.5, ax=ax,legend="full")
            ax.add_patch(plt.Rectangle((-0.7083, data_filter['sz_bot'].median()), 1.4166, data_filter['sz_top'].median() - data_filter['sz_bot'].median(), alpha=0.5, edgecolor='gray', facecolor='none', linewidth=2))
            ax.set_title(type)
            ax.set_xlabel('Horizontal Position')
            ax.set_ylabel('Vertical Position')
            ax.set_aspect('equal')
            ax.get_legend().remove()
            plt.show()

    def new_setup(self):
        pitcher_df = pd.read_csv(f"data/clean/{self.id}.csv")
        pitcher_unclean = pd.read_csv(f"data/unclean/{self.id}.csv")
        
        pitcher_df_X = pitcher_df[features_dict["plotting_data"]]
        pitcher_df_X = pitcher_df_X.dropna(how="any")
        
        pitcher_df_Y = pitcher_df[["zone"]]
        pitcher_df_Y = pitcher_df_Y.dropna(how="any")
        

        print(pitcher_df_X.shape)
        print(pitcher_df_Y.shape)
        print(self.correlation_matrix(pitcher_df_X))

        print(self.pitcher_plotting(pitcher_unclean))
        
        le = LabelEncoder()
        pitcher_df_Y = le.fit_transform(pitcher_df_Y)

        print(len(pitcher_df_X.columns))
        #pitcher_df_X = pd.get_dummies(pitcher_df_X, columns=["pitch_type", "stand", "p_throws","type","pitch_name"])
        #X_train, X_val, y_train, y_val = train_test_split(pitcher_df_X, pitcher_df_Y, test_size=0.3)

        
        X_train, X_val, y_train, y_val = train_test_split(pitcher_df_X, pitcher_df_Y, test_size=0.3, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_val, y_val, test_size=0.5, random_state=42)
        
            
            # - X_train: training data
            # - y_train: training labels
            # - X_val: validation data
            # - y_val: validation labels
            # - X_test: testing data
            # - y_test: testing labels

        test = keras.Input(shape = (pitcher_df_X.shape[1],))
        """
        Relu (rectified linear unit) activation function
    
        -   an activation function is a layer in a neural network that introduces non-linearity to the model
        -   It takes the output of the previous layer, applies a non-linear transformation, and returns the transformed output
        """
        dense = layers.Dense(64, activation="relu")
        x = dense(test)

        StrikeZone = layers.Dense(13)(x)

        model = keras.Model(inputs=test, outputs=StrikeZone, name="mnist_model")

        model.compile(
            loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            optimizer=keras.optimizers.RMSprop(),
            metrics=["accuracy"],
        )

        early_stopping = EarlyStopping(
            patience=30,        #number of epochs to wait before stopping
            min_delta = 0.001,  #min value to consider an improvement
            restore_best_weights=True
        )

        history = model.fit(
            X_train, 
            y_train,
            epochs=115,
            batch_size=32,
            validation_data=(X_val, y_val),
            callbacks=[early_stopping]
        )

        test_loss, test_acc = model.evaluate(X_test, y_test)
        print(f"Test accuracy: {test_acc:.4f}")


        # Plot training and validation accuracy values
        plt.plot(history.history["accuracy"])
        plt.plot(history.history["val_accuracy"])
        plt.title("Model accuracy")
        plt.ylabel("Accuracy")
        plt.xlabel("Epoch")
        plt.legend(["Train", "Val"], loc="upper left")
        plt.show()

        # Plot training and validation loss values
        plt.plot(history.history["loss"])
        plt.plot(history.history["val_loss"])
        plt.title("Model loss")
        plt.ylabel("Loss")
        plt.xlabel("Epoch")
        plt.legend(["Train", "Val"], loc="upper left")
        plt.show()

         
        '''# Get the predicted values
        predicted_values = model.predict(pitcher_df_X)
        
        # Print out the actual values and predicted values
        for i in range(len(pitcher_df_Y)):
            print(f"Actual value: {pitcher_df_Y[i]}")
            print(f"Predicted value: {predicted_values[i]}")
            print()
        '''
        

        

    def deprecated_setup_pitcher_df(self):
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





p1 = KerasPitcherModel(656302)
p1.new_setup()