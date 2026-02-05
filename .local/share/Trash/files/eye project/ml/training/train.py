import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
import pandas as pd
from PIL import Image
import os
import json
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import logging
from typing import Dict, List, Tuple, Optional
import albumentations as A
from albumentations.pytorch import ToTensorV2

from .cnn_vit_hybrid import EyeDiseaseClassifier

logger = logging.getLogger(__name__)


class EyeDataset(Dataset):
    """Custom dataset for eye disease classification"""
    
    def __init__(
        self,
        image_paths: List[str],
        labels: List[int],
        transforms: Optional[A.Compose] = None,
        multi_label: bool = False,
        multi_hot_labels: Optional[List[np.ndarray]] = None
    ):
        self.image_paths = image_paths
        self.labels = labels
        self.transforms = transforms
        self.multi_label = multi_label
        self.multi_hot_labels = multi_hot_labels
    
    def __len__(self) -> int:
        return len(self.image_paths)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        # Load image
        image = Image.open(self.image_paths[idx]).convert('RGB')
        image = np.array(image)
        
        # Apply transforms
        if self.transforms:
            augmented = self.transforms(image=image)
            image = augmented['image']
        
        # Get labels
        if self.multi_label and self.multi_hot_labels:
            label = torch.FloatTensor(self.multi_hot_labels[idx])
        else:
            label = torch.LongTensor([self.labels[idx]])
        
        return image, label


class EyeDiseaseTrainer:
    """Trainer class for eye disease classification model"""
    
    def __init__(
        self,
        num_classes: int = 8,
        device: Optional[str] = None,
        save_dir: str = "ml/models/checkpoints"
    ):
        self.num_classes = num_classes
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.save_dir = save_dir
        self.model = None
        self.train_loader = None
        self.val_loader = None
        self.test_loader = None
        
        # Create save directory
        os.makedirs(save_dir, exist_ok=True)
        
        # Setup logging
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(self.save_dir, 'training.log')),
                logging.StreamHandler()
            ]
        )
    
    def setup_data(
        self,
        data_dir: str,
        batch_size: int = 32,
        test_size: float = 0.2,
        val_size: float = 0.1,
        random_state: int = 42
    ):
        """Setup data loaders"""
        
        # Training transforms with augmentation
        train_transforms = A.Compose([
            A.Resize(384, 384),
            A.HorizontalFlip(p=0.5),
            A.RandomRotate90(p=0.5),
            A.RandomBrightnessContrast(
                brightness_limit=0.2,
                contrast_limit=0.2,
                p=0.5
            ),
            A.ShiftScaleRotate(
                shift_limit=0.1,
                scale_limit=0.1,
                rotate_limit=15,
                p=0.5
            ),
            A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
            A.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
            ToTensorV2()
        ])
        
        # Validation/test transforms (no augmentation)
        val_transforms = A.Compose([
            A.Resize(384, 384),
            A.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
            ToTensorV2()
        ])
        
        # Load data (assuming CSV file with image paths and labels)
        csv_path = os.path.join(data_dir, 'labels.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            image_paths = [os.path.join(data_dir, path) for path in df['image_path']]
            labels = df['label'].tolist()
        else:
            # Fallback to directory structure
            image_paths, labels = self._load_from_directories(data_dir)
        
        # Split data
        train_paths, test_paths, train_labels, test_labels = train_test_split(
            image_paths, labels, test_size=test_size, random_state=random_state, stratify=labels
        )
        
        train_paths, val_paths, train_labels, val_labels = train_test_split(
            train_paths, train_labels, test_size=val_size, random_state=random_state, stratify=train_labels
        )
        
        # Create datasets
        train_dataset = EyeDataset(train_paths, train_labels, train_transforms)
        val_dataset = EyeDataset(val_paths, val_labels, val_transforms)
        test_dataset = EyeDataset(test_paths, test_labels, val_transforms)
        
        # Create data loaders
        self.train_loader = DataLoader(
            train_dataset, batch_size=batch_size, shuffle=True, num_workers=4
        )
        self.val_loader = DataLoader(
            val_dataset, batch_size=batch_size, shuffle=False, num_workers=4
        )
        self.test_loader = DataLoader(
            test_dataset, batch_size=batch_size, shuffle=False, num_workers=4
        )
        
        logger.info(f"Data loaded: {len(train_dataset)} train, {len(val_dataset)} val, {len(test_dataset)} test")
    
    def _load_from_directories(self, data_dir: str) -> Tuple[List[str], List[int]]:
        """Load data from directory structure"""
        image_paths = []
        labels = []
        class_names = sorted([d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))])
        
        for class_idx, class_name in enumerate(class_names):
            class_dir = os.path.join(data_dir, class_name)
            for image_name in os.listdir(class_dir):
                if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_paths.append(os.path.join(class_dir, image_name))
                    labels.append(class_idx)
        
        return image_paths, labels
    
    def setup_model(self, learning_rate: float = 1e-4):
        """Setup model and optimizer"""
        self.model = EyeDiseaseClassifier(num_classes=self.num_classes)
        self.model.to(self.device)
        
        # Loss function
        self.criterion = nn.CrossEntropyLoss()
        
        # Optimizer
        self.optimizer = optim.AdamW(
            self.model.parameters(),
            lr=learning_rate,
            weight_decay=1e-4
        )
        
        # Learning rate scheduler
        self.scheduler = optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, T_max=50, eta_min=1e-6
        )
        
        logger.info(f"Model setup complete. Parameters: {sum(p.numel() for p in self.model.parameters()):,}")
    
    def train_epoch(self) -> Dict[str, float]:
        """Train for one epoch"""
        self.model.train()
        total_loss = 0
        correct = 0
        total = 0
        
        for batch_idx, (images, labels) in enumerate(self.train_loader):
            images, labels = images.to(self.device), labels.to(self.device).squeeze()
            
            # Zero gradients
            self.optimizer.zero_grad()
            
            # Forward pass
            outputs = self.model(images)
            loss = self.criterion(outputs['disease_logits'], labels)
            
            # Backward pass
            loss.backward()
            self.optimizer.step()
            
            # Statistics
            total_loss += loss.item()
            _, predicted = outputs['disease_logits'].max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            # Log progress
            if batch_idx % 100 == 0:
                logger.info(f'Batch {batch_idx}/{len(self.train_loader)}, Loss: {loss.item():.4f}')
        
        avg_loss = total_loss / len(self.train_loader)
        accuracy = 100. * correct / total
        
        return {'loss': avg_loss, 'accuracy': accuracy}
    
    def validate_epoch(self) -> Dict[str, float]:
        """Validate for one epoch"""
        self.model.eval()
        total_loss = 0
        correct = 0
        total = 0
        all_predictions = []
        all_labels = []
        
        with torch.no_grad():
            for images, labels in self.val_loader:
                images, labels = images.to(self.device), labels.to(self.device).squeeze()
                
                outputs = self.model(images)
                loss = self.criterion(outputs['disease_logits'], labels)
                
                total_loss += loss.item()
                _, predicted = outputs['disease_logits'].max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
                
                all_predictions.extend(predicted.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        avg_loss = total_loss / len(self.val_loader)
        accuracy = 100. * correct / total
        
        # Calculate additional metrics
        report = classification_report(
            all_labels, all_predictions,
            output_dict=True, zero_division=0
        )
        
        return {
            'loss': avg_loss,
            'accuracy': accuracy,
            'precision': report['macro avg']['precision'],
            'recall': report['macro avg']['recall'],
            'f1': report['macro avg']['f1-score']
        }
    
    def train(
        self,
        num_epochs: int = 100,
        early_stopping_patience: int = 15,
        save_best: bool = True
    ):
        """Train the model"""
        best_val_f1 = 0
        patience_counter = 0
        history = {
            'train_loss': [], 'train_acc': [],
            'val_loss': [], 'val_acc': [],
            'val_f1': []
        }
        
        for epoch in range(num_epochs):
            logger.info(f'Epoch {epoch + 1}/{num_epochs}')
            
            # Train
            train_metrics = self.train_epoch()
            
            # Validate
            val_metrics = self.validate_epoch()
            
            # Learning rate step
            self.scheduler.step()
            
            # Log metrics
            history['train_loss'].append(train_metrics['loss'])
            history['train_acc'].append(train_metrics['accuracy'])
            history['val_loss'].append(val_metrics['loss'])
            history['val_acc'].append(val_metrics['accuracy'])
            history['val_f1'].append(val_metrics['f1'])
            
            logger.info(f"Train Loss: {train_metrics['loss']:.4f}, Train Acc: {train_metrics['accuracy']:.2f}%")
            logger.info(f"Val Loss: {val_metrics['loss']:.4f}, Val Acc: {val_metrics['accuracy']:.2f}%, Val F1: {val_metrics['f1']:.4f}")
            
            # Save best model
            if save_best and val_metrics['f1'] > best_val_f1:
                best_val_f1 = val_metrics['f1']
                self.save_checkpoint(f'best_model_epoch_{epoch + 1}.pth', val_metrics)
                patience_counter = 0
            else:
                patience_counter += 1
            
            # Early stopping
            if patience_counter >= early_stopping_patience:
                logger.info(f"Early stopping triggered after {epoch + 1} epochs")
                break
        
        # Save training history
        with open(os.path.join(self.save_dir, 'training_history.json'), 'w') as f:
            json.dump(history, f, indent=2)
        
        # Plot training curves
        self.plot_training_curves(history)
        
        return history
    
    def save_checkpoint(self, filename: str, metrics: Dict[str, float]):
        """Save model checkpoint"""
        checkpoint = {
            'epoch': len(history.get('train_loss', [])),
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'metrics': metrics,
            'num_classes': self.num_classes
        }
        
        filepath = os.path.join(self.save_dir, filename)
        torch.save(checkpoint, filepath)
        logger.info(f"Checkpoint saved: {filepath}")
    
    def plot_training_curves(self, history: Dict[str, List[float]]):
        """Plot training curves"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Loss
        axes[0, 0].plot(history['train_loss'], label='Train Loss')
        axes[0, 0].plot(history['val_loss'], label='Val Loss')
        axes[0, 0].set_title('Loss')
        axes[0, 0].legend()
        
        # Accuracy
        axes[0, 1].plot(history['train_acc'], label='Train Acc')
        axes[0, 1].plot(history['val_acc'], label='Val Acc')
        axes[0, 1].set_title('Accuracy')
        axes[0, 1].legend()
        
        # F1 Score
        axes[1, 0].plot(history['val_f1'], label='Val F1')
        axes[1, 0].set_title('F1 Score')
        axes[1, 0].legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.save_dir, 'training_curves.png'))
        plt.close()
    
    def evaluate_model(self):
        """Evaluate model on test set"""
        self.model.eval()
        all_predictions = []
        all_labels = []
        
        with torch.no_grad():
            for images, labels in self.test_loader:
                images, labels = images.to(self.device), labels.to(self.device).squeeze()
                outputs = self.model(images)
                _, predicted = outputs['disease_logits'].max(1)
                
                all_predictions.extend(predicted.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        # Generate classification report
        report = classification_report(all_labels, all_predictions, output_dict=True)
        cm = confusion_matrix(all_labels, all_predictions)
        
        # Plot confusion matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig(os.path.join(self.save_dir, 'confusion_matrix.png'))
        plt.close()
        
        # Save results
        results = {
            'classification_report': report,
            'confusion_matrix': cm.tolist()
        }
        
        with open(os.path.join(self.save_dir, 'evaluation_results.json'), 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info("Evaluation complete. Results saved.")
        return results


def main():
    """Main training function"""
    # Configuration
    config = {
        'data_dir': 'ml/data/processed',
        'num_classes': 8,
        'batch_size': 32,
        'num_epochs': 100,
        'learning_rate': 1e-4,
        'early_stopping_patience': 15
    }
    
    # Initialize trainer
    trainer = EyeDiseaseTrainer(
        num_classes=config['num_classes'],
        save_dir='ml/models/checkpoints'
    )
    
    # Setup data
    trainer.setup_data(
        data_dir=config['data_dir'],
        batch_size=config['batch_size']
    )
    
    # Setup model
    trainer.setup_model(learning_rate=config['learning_rate'])
    
    # Train
    history = trainer.train(
        num_epochs=config['num_epochs'],
        early_stopping_patience=config['early_stopping_patience']
    )
    
    # Evaluate
    results = trainer.evaluate_model()
    
    logger.info("Training completed successfully!")


if __name__ == "__main__":
    main()