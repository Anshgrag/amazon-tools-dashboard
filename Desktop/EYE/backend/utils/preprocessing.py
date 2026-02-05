"""
Image preprocessing utilities for eye infection detection
"""
import numpy as np
from PIL import Image
from typing import Union


def preprocess_image(
    image_path: str,
    target_size: tuple = (224, 224)
) -> np.ndarray:
    """
    Load and preprocess an eye image for model inference.
    
    Args:
        image_path: Path to the uploaded image file
        target_size: Target dimensions for resizing (default: 224x224)
    
    Returns:
        Preprocessed numpy array ready for model prediction
    """
    try:
        # Load image with PIL
        img = Image.open(image_path)
        
        # Convert RGB if necessary (handles RGBA, grayscale, etc.)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to target dimensions
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array and normalize to [0, 1]
        img_array = np.array(img, dtype=np.float32) / 255.0
        
        # Add batch dimension for model input
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {str(e)}")


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize image using ImageNet statistics for transfer learning.
    
    Args:
        image: Input image array (H, W, C)
    
    Returns:
        Normalized image array
    """
    # ImageNet mean and std
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    
    normalized = image.copy()
    for i in range(3):
        normalized[:, :, i] = (image[:, :, i] - mean[i]) / std[i]
    
    return normalized


def validate_image_format(file_path: str) -> bool:
    """
    Validate that the file is a supported image format.
    
    Args:
        file_path: Path to the image file
    
    Returns:
        True if valid format, False otherwise
    """
    valid_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
    return any(file_path.endswith(ext) for ext in valid_extensions)
