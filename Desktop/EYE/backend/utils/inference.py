"""
Model inference utilities for eye infection detection
"""
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from typing import Dict, Tuple
import os


class EyeDiseaseModel:
    """Wrapper class for loading and running the eye disease detection model."""
    
    def __init__(self, model_path: str = None):
        """
        Initialize the model wrapper.
        
        Args:
            model_path: Path to the saved .h5 or .keras model file
        """
        self.model = None
        self.class_names = [
            'Normal',
            'Conjunctivitis',
            'Cataract',
            'Glaucoma'
        ]
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def load_model(self, model_path: str) -> None:
        """
        Load the trained model from disk.
        
        Args:
            model_path: Path to the saved model file
        """
        try:
            # Load model with custom objects if needed
            self.model = load_model(model_path)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")
    
    def predict(self, preprocessed_image: np.ndarray) -> Dict[str, float]:
        """
        Run prediction on a preprocessed image.
        
        Args:
            preprocessed_image: Preprocessed numpy array (1, 224, 224, 3)
        
        Returns:
            Dictionary with 'predicted_class' and 'confidence_score'
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Make prediction
        predictions = self.model.predict(preprocessed_image, verbose=0)
        
        # Get the class with highest probability
        predicted_index = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_index])
        
        return {
            'predicted_class': self.class_names[predicted_index],
            'confidence_score': confidence
        }
    
    def predict_batch(self, images: np.ndarray) -> list:
        """
        Run prediction on a batch of images.
        
        Args:
            images: Batch of preprocessed images (batch_size, 224, 224, 3)
        
        Returns:
            List of prediction dictionaries
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        predictions = self.model.predict(images, verbose=0)
        
        results = []
        for pred in predictions:
            predicted_index = np.argmax(pred)
            confidence = float(pred[predicted_index])
            results.append({
                'predicted_class': self.class_names[predicted_index],
                'confidence_score': confidence
            })
        
        return results
    
    def get_model_summary(self) -> str:
        """
        Get a summary of the loaded model architecture.
        
        Returns:
            String containing model summary
        """
        if self.model is None:
            return "Model not loaded"
        
        import io
        stream = io.StringIO()
        self.model.summary(print_fn=lambda x: stream.write(x + '\n'))
        return stream.getvalue()


def create_model_placeholder():
    """
    Create a simple placeholder model for testing API endpoints.
    This returns random predictions and is only for development.
    
    Returns:
        Simple Keras model (untrained)
    """
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
    from tensorflow.keras.models import Model
    
    # Load pre-trained MobileNetV2 without top layers
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )
    
    # Add custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(4, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    return model
