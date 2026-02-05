"""
Utility script to test the backend API without the frontend.
"""
import requests
from pathlib import Path

API_URL = "http://localhost:8000/predict"
IMAGE_PATH = "path/to/your/test_image.jpg"  # Change this to your test image


def test_prediction(image_path: str):
    """Test the prediction endpoint."""
    
    if not Path(image_path).exists():
        print(f"Error: Image not found at {image_path}")
        return
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(API_URL, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("Prediction Result:")
            print(f"  Class: {result['predicted_class']}")
            print(f"  Confidence: {result['confidence_score']:.2%}")
        else:
            print(f"Error: {response.status_code}")
            print(response.json())
    
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Is the backend running?")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        IMAGE_PATH = sys.argv[1]
    
    test_prediction(IMAGE_PATH)
