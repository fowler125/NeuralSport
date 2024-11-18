import keras_tuner as kt
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow as tf
import keras

class PitchingTuner:
    def __init__(self, input_shape, output_shape):
        self.input_shape = input_shape
        self.output_shape = output_shape
        
    def build_model(self, hp):
        """
        Model builder function for Keras Tuner.
        """
        inputs = keras.Input(shape=self.input_shape)
        
        # Tune number of layers
        n_layers = hp.Int('n_layers', min_value=1, max_value=4, default=1)
        
        x = inputs
        # Tune units and activation for each layer
        for i in range(n_layers):
            units = hp.Int(f'units_{i}', min_value=16, max_value=256, step=16)
            activation = hp.Choice(f'activation_{i}', values=['relu'])
            x = layers.Dense(units=units, activation=activation)(x)
            
            """# Optional dropout
            dropout_rate = hp.Float(f'dropout_{i}', min_value=0.0, max_value=0.5, step=0.1)
            if dropout_rate > 0:
                x = layers.Dropout(dropout_rate)(x)"""
        
        outputs = layers.Dense(self.output_shape)(x)
        
        model = keras.Model(inputs=inputs, outputs=outputs)
        
        # Tune learning rate
        learning_rate = hp.Float('learning_rate', min_value=1e-4, max_value=1e-2, sampling='log')
        
        # Tune optimizer
        optimizer_choice = hp.Choice('optimizer', values=['adam', 'rmsprop'])
        if optimizer_choice == 'adam':
            optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
        else:
            optimizer = keras.optimizers.RMSprop(learning_rate=learning_rate)
        
        model.compile(
            optimizer=optimizer,
            loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )
        
        return model
    
    def tune_model(self, X_train, y_train, X_val, y_val, project_name='pitch_classification'):
        """
        Perform hyperparameter tuning using Keras Tuner.
        
        Parameters:
        -----------
        X_train : array-like
            Training features
        y_train : array-like
            Training labels
        X_val : array-like
            Validation features
        y_val : array-like
            Validation labels
        project_name : str
            Name for the tuning project directory
            
        Returns:
        --------
        tuple
            (best_hyperparameters, best_model)
        """
        tuner = kt.Hyperband(
            self.build_model,
            objective='accuracy',
            max_epochs=100,
            factor=3,
            directory='keras_tuner',
            project_name=project_name
        )
        
        # Define early stopping callback for tuner
        stop_early = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            min_delta=0.001,
            restore_best_weights=True
        )
        
        # Search for best hyperparameters
        tuner.search(
            X_train,
            y_train,
            epochs=50,
            validation_data=(X_val, y_val),
            callbacks=[stop_early],
            verbose=1
        )
        
        # Get best hyperparameters
        best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
        print("\nBest Hyperparameters:")
        for param in best_hps.values:
            print(f"{param}: {best_hps.values[param]}")
        
        # Build model with best hyperparameters
        best_model = tuner.hypermodel.build(best_hps)
        
        return best_hps, best_model