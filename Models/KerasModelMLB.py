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
from sklearn.metrics import confusion_matrix,ConfusionMatrixDisplay
from sklearn.linear_model import LogisticRegression
from hyperpar_tuning import PitchingTuner
features_dict = {
    "reduced":["vx0","vy0","vz0","ax","ay","az"],
    "full":["pitch_type","release_speed","release_pos_x","release_pos_z","spin_dir",
            "spin_rate_deprecated","break_angle_deprecated","break_length_deprecated",
            "zone","stand","p_throws","type","balls","strikes","pfx_x","pfx_z","plate_x","plate_z",
            "on_3b","on_2b","on_1b","outs_when_up","inning","vx0","vy0","vz0","ax","ay","az","sz_top",
            "sz_bot","release_spin_rate","release_extension","release_pos_y","at_bat_number",
            "pitch_number","pitch_name","spin_axis"],
    "numerical_only":["vx0","vy0","vz0","ax","ay","az","plate_x","plate_z"],
    "plotting_data":["vx0","vy0","vz0","ax","ay","az","pfx_x","pfx_z","plate_x","plate_z","sz_top","sz_bot"]
}
class KerasPitcherModel:
    def __init__(self,id) -> None:
        self.id = id

    def correlation_matrix(self,data:pd.DataFrame):
        #Create Correlation Matrix to show linear relationships between variables
        corr_matrix = data.corr()
        
        plt.figure(figsize=(10,8))
        
        sns.heatmap(corr_matrix, annot=True,cmap='coolwarm',square=True)
        
        plt.title("Correlation Matrix")
        
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
        sns.scatterplot(x='plate_x', y='plate_z', hue='type', data=data, alpha=0.5, ax=ax,palette=['green','red','dodgerblue'])

        # Plot the strike zone rectangle
        strike_zone_rect = plt.Rectangle((-0.7083, data_filter['sz_bot'].median()), 1.4166, data['sz_top'].median() - data['sz_bot'].median(), alpha=0.5, edgecolor='black', facecolor='none', linewidth=2)
        ax.add_patch(strike_zone_rect)
        
        
        # Set the title and labels
        ax.set_title('Called Balls and Strikes')
        ax.set_xlabel('Horizontal Position')
        ax.set_ylabel('Vertical Position')


        # Set the aspect ratio
        ax.set_aspect('equal')

        # Set the font family
        plt.rcParams['font.family'] = 'serif'
        plt.show()


        # Facet by type
        for type in data_filter['type'].unique():
            fig, ax = plt.subplots(figsize=(8, 8))
            
            ax.add_patch(plt.Rectangle((-0.7083, data_filter['sz_bot'].median()), 1.4166, data_filter['sz_top'].median() - data_filter['sz_bot'].median(), alpha=0.5, edgecolor='gray', facecolor='none', linewidth=2))
            if type == 'S':
                sns.scatterplot(x='plate_x', y='plate_z', hue='type', data=data_filter[data_filter['type'] == type], alpha=0.5, ax=ax,palette=['tomato'],legend="full")
               
                ax.set_title('Called Strikes')
                
            elif type == 'B':
                sns.scatterplot(x='plate_x', y='plate_z', hue='type', data=data_filter[data_filter['type'] == type], alpha=0.5, ax=ax,palette=['dodgerblue'],legend="full")
            
                ax.set_title('Called Balls')
                
            ax.set_xlabel('Horizontal Position')
            ax.set_ylabel('Vertical Position')
            ax.set_aspect('equal')
            ax.get_legend().remove()
            plt.show()

    def setup_logistic_regression(self,pitcher_df):
        # Define the features (X) and target (y)
        X = pitcher_df[features_dict["plotting_data"]]
        X = X.dropna(how="any")
        y = pitcher_df["zone"]
        y = y.dropna(how="any")

        # Encode the target variable
        le = LabelEncoder()
        y = le.fit_transform(y)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create a logistic regression model
        logreg = LogisticRegression(max_iter=5000)

        # Train the model
        logreg.fit(X_train, y_train)

        # Return the trained model and the testing data
        return logreg, X_test, y_test
    
    def confusion_matrix(self,data_Y,predicted_Y):
        #Create a confusion matrix, actual zone vs predicted zone
        cm = confusion_matrix(data_Y, predicted_Y)
        
        cm_display = ConfusionMatrixDisplay(cm).plot()
        
        cm_display.ax_.set(title='Confusion Matrix', xlabel='Predicted Zone', ylabel='True Zone')

        plt.show()

    def accuracy_plotting(self,history):
        # Plot training and validation accuracy values
        plt.plot(history.history["accuracy"])
        plt.plot(history.history["val_accuracy"])
        plt.title("Model accuracy")
        plt.ylabel("Accuracy")
        plt.xlabel("Epoch")
        plt.legend(["Train", "Val"], loc="upper left")
        plt.show()
    
    def loss_plotting(self,history):
        # Plot training and validation loss values
        plt.plot(history.history["loss"])
        plt.plot(history.history["val_loss"])
        plt.title("Model loss")
        plt.ylabel("Loss")
        plt.xlabel("Epoch")
        plt.legend(["Train", "Val"], loc="upper left")
        plt.show()
    
    
    
    def new_setup(self):
        pitcher_df = pd.read_csv(f"data/clean/{self.id}.csv")
        pitcher_unclean = pd.read_csv(f"data/unclean/{self.id}.csv")
        
        pitcher_df_X = pitcher_df[features_dict["plotting_data"]]
        pitcher_df_X = pitcher_df_X.dropna(how="any")
        
        pitcher_df_Y = pitcher_df[["zone"]]
        pitcher_df_Y = pitcher_df_Y.dropna(how="any")
        
        self.correlation_matrix(pitcher_df_X)

        self.pitcher_plotting(pitcher_unclean)
        
        le = LabelEncoder()
        pitcher_df_Y = le.fit_transform(pitcher_df_Y)

        print('Number of features: ', len(pitcher_df_X.columns))

        
        X_train, X_val, y_train, y_val = train_test_split(pitcher_df_X, pitcher_df_Y, test_size=0.3, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_val, y_val, test_size=0.5, random_state=42)
        
         # Initialize the tuner with input and output shapes
        tuner = PitchingTuner(
            input_shape=(pitcher_df_X.shape[1],),
            output_shape=13
        )
    
        # Perform hyperparameter tuning
        best_hps, best_model = tuner.tune_model(
            X_train=X_train,
            y_train=y_train,
            X_val=X_val,
            y_val=y_val,
            project_name=f'pitcher_{self.id}_tuning'
        )
       
        early_stopping = EarlyStopping(
            patience=30,        #number of epochs to wait before stopping
            min_delta = 0.001,  #min value to consider an improvement
            restore_best_weights=True
        )

        history = best_model.fit(
            X_train, 
            y_train,
            epochs=500,
            batch_size=32,
            validation_data=(X_val, y_val),
            callbacks=[early_stopping]
        )

        test_loss, test_acc = best_model.evaluate(X_test, y_test)
        print(f"Test accuracy: {test_acc:.4f}") 

        # Plot the training history
        self.accuracy_plotting(history)

        self.loss_plotting(history)
         
        # Get the predicted values
        predicted_values = best_model.predict(pitcher_df_X)
        predicted_zone = np.argmax(predicted_values, axis=1)
        predicted_df = pd.DataFrame(predicted_values, columns=[f'Zone {i}' for i in range(1, 14)])
        
        predicted_zone = np.argmax(predicted_values, axis=1)
        max_probabilities = np.max(predicted_values, axis=1)

        zone_df = pd.DataFrame({
            'Actual Zone': pitcher_df_Y,
            'Predicted Zone': predicted_zone,
            'Highest Probability': max_probabilities
        })

        print(zone_df)
        zone_df.to_csv(f'data/predictions/{self.id}.csv', index=False)

        # Create a confusion matrix
        self.confusion_matrix(pitcher_df_Y, predicted_zone)

        #Logistic Regression Comparison
        logreg, X_test, y_test = self.setup_logistic_regression(pitcher_df)
        
        # Make predictions on the testing data
        y_pred = logreg.predict(X_test)
        
        # Evaluate the model's performance
        accuracy = logreg.score(X_test, y_test)
        print(f"Accuracy: {accuracy:.4f}")

        


p1 = KerasPitcherModel(656302)
p1.new_setup()