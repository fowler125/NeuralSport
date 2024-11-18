from tensorflow import keras
from tensorflow.keras import layers

class OptimizedPitchingModel:
    """
    Neural network model for pitch classification using optimized hyperparameters
    found through tuning.
    """
    
    def __init__(self, input_shape, output_shape=13):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.model = self._build_model()
        
    def _build_model(self):
        """
        Builds the model with the optimized architecture found through hyperparameter tuning.
        """
        inputs = keras.Input(shape=self.input_shape)
        
        # Layer 1
        x = layers.Dense(
            units=192,
            activation='relu',
            name='dense_1'
        )(inputs)
        
        # Layer 2
        x = layers.Dense(
            units=240,
            activation='relu',
            name='dense_2'
        )(x)
        
        # Output layer
        outputs = layers.Dense(
            self.output_shape,
            name='predictions'
        )(x)
        
        model = keras.Model(inputs=inputs, outputs=outputs)
        
        # Use the optimized learning rate found during tuning
        optimizer = keras.optimizers.Adam(learning_rate=0.001070)
        
        model.compile(
            optimizer=optimizer,
            loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )
        
        return model
    
    def fit(self, X_train, y_train, X_val=None, y_val=None, **kwargs):
        """
        Train the model with early stopping and optional validation data.
        
        Parameters:
        -----------
        X_train : array-like
            Training features
        y_train : array-like
            Training labels
        X_val : array-like, optional
            Validation features
        y_val : array-like, optional
            Validation labels
        **kwargs : 
            Additional arguments passed to model.fit()
        
        Returns:
        --------
        History object
        """
        callbacks = [
            keras.callbacks.EarlyStopping(
                patience=30,
                min_delta=0.001,
                restore_best_weights=True,
                monitor='val_loss' if X_val is not None else 'loss'
            )
        ]
        
        validation_data = (X_val, y_val) if X_val is not None and y_val is not None else None
        
        return self.model.fit(
            X_train,
            y_train,
            validation_data=validation_data,
            callbacks=callbacks,
            **kwargs
        )
    
    def predict(self, X):
        """
        Make predictions using the model.
        """
        return self.model.predict(X)
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate the model on test data.
        """
        return self.model.evaluate(X_test, y_test)
    
    def save(self, filepath):
        """
        Save the model to a file.
        """
        self.model.save(filepath)
    
    @classmethod
    def load(cls, filepath):
        """
        Load a saved model.
        """
        model = keras.models.load_model(filepath)
        instance = cls(model.input_shape[1:])
        instance.model = model
        return instance