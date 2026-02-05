import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
from transformers import ViTModel, ViTConfig
from typing import Dict, Any, Optional, Tuple
import numpy as np
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class EyeDiseaseClassifier(nn.Module):
    """
    Hybrid CNN-ViT model for eye disease classification
    Combines EfficientNet for local features with Vision Transformer for global context
    """
    
    def __init__(self, num_classes: int = 8, dropout_rate: float = 0.3):
        super(EyeDiseaseClassifier, self).__init__()
        
        # CNN Backbone (EfficientNet-B4)
        self.cnn_backbone = models.efficientnet_b4(pretrained=True)
        
        # Remove the final classification layer
        self.cnn_features = nn.Sequential(*list(self.cnn_backbone.children())[:-1])
        
        # Get CNN feature dimension
        with torch.no_grad():
            dummy_input = torch.randn(1, 3, 384, 384)
            cnn_output = self.cnn_features(dummy_input)
            self.cnn_feature_dim = cnn_output.flatten(1).size(1)
        
        # Vision Transformer for global context
        self.vit_config = ViTConfig(
            image_size=384,
            patch_size=16,
            num_channels=3,
            hidden_size=768,
            num_hidden_layers=12,
            num_attention_heads=12,
            intermediate_size=3072,
            hidden_dropout_prob=dropout_rate,
            attention_probs_dropout_prob=dropout_rate,
        )
        self.vit = ViTModel(self.vit_config)
        
        # Feature fusion
        self.fusion_layer = nn.Sequential(
            nn.Linear(self.cnn_feature_dim + self.vit_config.hidden_size, 1024),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
        )
        
        # Classification heads
        self.disease_classifier = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(256, num_classes)
        )
        
        self.severity_classifier = nn.Sequential(
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(128, 4)  # mild, moderate, severe, normal
        )
        
        # Visual feature detectors
        self.redness_detector = nn.Sequential(
            nn.Linear(512, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
        
        self.swelling_detector = nn.Sequential(
            nn.Linear(512, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
        
        self.discharge_detector = nn.Sequential(
            nn.Linear(512, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
        
        self.cloudiness_detector = nn.Sequential(
            nn.Linear(512, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
    
    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        # CNN features
        cnn_features = self.cnn_features(x)
        cnn_features = cnn_features.flatten(1)
        
        # ViT features
        vit_outputs = self.vit(x)
        vit_features = vit_outputs.last_hidden_state[:, 0, :]  # [CLS] token
        
        # Feature fusion
        combined_features = torch.cat([cnn_features, vit_features], dim=1)
        fused_features = self.fusion_layer(combined_features)
        
        # Classification outputs
        disease_logits = self.disease_classifier(fused_features)
        severity_logits = self.severity_classifier(fused_features)
        
        # Visual features
        redness = self.redness_detector(fused_features)
        swelling = self.swelling_detector(fused_features)
        discharge = self.discharge_detector(fused_features)
        cloudiness = self.cloudiness_detector(fused_features)
        
        return {
            'disease_logits': disease_logits,
            'severity_logits': severity_logits,
            'visual_features': {
                'redness': redness,
                'swelling': swelling,
                'discharge': discharge,
                'cloudiness': cloudiness
            },
            'features': fused_features
        }


class EyeDiseasePredictor:
    """
    Prediction wrapper for eye disease classification
    """
    
    # Class labels
    DISEASE_LABELS = [
        'normal',
        'conjunctivitis',
        'stye',
        'cataract',
        'blepharitis',
        'corneal_ulcer',
        'dry_eye',
        'glaucoma'
    ]
    
    SEVERITY_LABELS = ['normal', 'mild', 'moderate', 'severe']
    
    def __init__(
        self,
        model_path: str,
        device: Optional[str] = None,
        confidence_threshold: float = 0.7
    ):
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.transform = None
        self._load_model(model_path)
        self._setup_transforms()
    
    def _load_model(self, model_path: str):
        """Load the trained model"""
        try:
            self.model = EyeDiseaseClassifier(num_classes=len(self.DISEASE_LABELS))
            checkpoint = torch.load(model_path, map_location=self.device)
            
            # Handle different checkpoint formats
            if 'model_state_dict' in checkpoint:
                self.model.load_state_dict(checkpoint['model_state_dict'])
            elif 'state_dict' in checkpoint:
                self.model.load_state_dict(checkpoint['state_dict'])
            else:
                self.model.load_state_dict(checkpoint)
            
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"Model loaded successfully from {model_path}")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def _setup_transforms(self):
        """Setup image preprocessing transforms"""
        self.transform = transforms.Compose([
            transforms.Resize((384, 384)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """Preprocess input image"""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return self.transform(image).unsqueeze(0)
    
    def predict(self, image: Image.Image) -> Dict[str, Any]:
        """
        Make prediction on input image
        
        Args:
            image: PIL Image of the eye
            
        Returns:
            Dictionary containing predictions and explanations
        """
        if self.model is None:
            raise ValueError("Model not loaded")
        
        try:
            # Preprocess
            input_tensor = self.preprocess_image(image).to(self.device)
            
            # Inference
            with torch.no_grad():
                outputs = self.model(input_tensor)
            
            # Process predictions
            disease_probs = torch.softmax(outputs['disease_logits'], dim=1)
            disease_confidence, disease_idx = torch.max(disease_probs, dim=1)
            
            severity_probs = torch.softmax(outputs['severity_logits'], dim=1)
            _, severity_idx = torch.max(severity_probs, dim=1)
            
            # Extract visual features
            visual_features_raw = outputs['visual_features']
            visual_features = {
                'redness': self._get_intensity_level(visual_features_raw['redness'].item()),
                'swelling': self._get_intensity_level(visual_features_raw['swelling'].item()),
                'discharge': self._get_intensity_level(visual_features_raw['discharge'].item()),
                'cloudiness': self._get_intensity_level(visual_features_raw['cloudiness'].item())
            }
            
            # Generate probabilities for all classes
            all_probabilities = {}
            for i, label in enumerate(self.DISEASE_LABELS):
                all_probabilities[label] = float(disease_probs[0][i].item())
            
            # Determine if infected or normal
            predicted_disease = self.DISEASE_LABELS[disease_idx.item()]
            is_normal = predicted_disease == 'normal'
            status = 'normal' if is_normal else 'infected'
            
            # Generate explanation
            explanation = self._generate_explanation(
                predicted_disease,
                visual_features,
                float(disease_confidence.item())
            )
            
            return {
                'status': status,
                'condition': predicted_disease if not is_normal else None,
                'confidence': float(disease_confidence.item()),
                'severity': self.SEVERITY_LABELS[severity_idx.item()],
                'all_probabilities': all_probabilities,
                'visual_features': visual_features,
                'explanation': explanation
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise
    
    def _get_intensity_level(self, value: float) -> str:
        """Convert continuous value to intensity level"""
        if value < 0.3:
            return 'absent'
        elif value < 0.6:
            return 'mild'
        elif value < 0.8:
            return 'moderate'
        else:
            return 'severe'
    
    def _generate_explanation(
        self,
        disease: str,
        visual_features: Dict[str, str],
        confidence: float
    ) -> str:
        """Generate human-readable explanation"""
        if disease == 'normal':
            return f"The eye appears normal with {confidence:.1%} confidence. No significant abnormalities detected."
        
        # Build explanation based on detected features and disease
        explanations = []
        
        feature_descriptions = {
            'conjunctivitis': {
                'redness': 'redness indicating inflammation',
                'discharge': 'discharge presence',
                'swelling': 'eyelid swelling'
            },
            'stye': {
                'swelling': 'localized swelling',
                'redness': 'redness around the affected area'
            },
            'cataract': {
                'cloudiness': 'cloudiness in the lens area'
            },
            'blepharitis': {
                'redness': 'eyelid margin redness',
                'swelling': 'eyelid inflammation'
            },
            'corneal_ulcer': {
                'cloudiness': 'corneal opacity',
                'redness': 'surrounding redness'
            },
            'dry_eye': {
                'redness': 'surface redness'
            },
            'glaucoma': {
                'cloudiness': 'potential corneal changes'
            }
        }
        
        disease_features = feature_descriptions.get(disease, {})
        detected_features = []
        
        for feature, description in disease_features.items():
            if visual_features.get(feature) in ['mild', 'moderate', 'severe']:
                detected_features.append(description)
        
        if detected_features:
            feature_text = ', '.join(detected_features[:-1])
            if len(detected_features) > 1:
                feature_text += f', and {detected_features[-1]}'
            else:
                feature_text = detected_features[0]
            
            return f"Model detected {feature_text} consistent with {disease} with {confidence:.1%} confidence."
        else:
            return f"Model prediction suggests {disease} with {confidence:.1%} confidence based on learned patterns."
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None