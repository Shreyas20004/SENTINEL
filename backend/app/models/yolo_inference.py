"""
YOLOv8 Inference Engine - Phase 1 Implementation

Features:
- Load pre-trained YOLOv8n model
- Inference on frames (<50ms target)
- Bounding box + confidence extraction
- GPU acceleration (CUDA)
"""

import logging
from typing import Dict, List, Tuple, Optional
import numpy as np
import time

logger = logging.getLogger(__name__)


class YOLOv8Inference:
    """YOLOv8 object detection"""
    
    def __init__(self, model_path: str, device: str = 'cuda'):
        """
        Initialize YOLO model
        
        Args:
            model_path: Path to YOLOv8 weights
            device: 'cuda' or 'cpu'
        """
        self.model_path = model_path
        self.device = device
        self.model = None
        self.confidence_threshold = 0.5
        logger.info(f"YOLOv8Inference initialized for {device}")
    
    def load_model(self):
        """Load model from disk"""
        try:
            from ultralytics import YOLO
            logger.info(f"Loading YOLOv8 model from {self.model_path}")
            self.model = YOLO(self.model_path)
            self.model.to(self.device)
            logger.info(f"Model loaded successfully on {self.device}")
        except ImportError:
            logger.error("ultralytics not installed. Install with: pip install ultralytics")
            raise
        except FileNotFoundError:
            logger.error(f"Model file not found: {self.model_path}")
            raise
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def predict(self, frame: np.ndarray) -> Dict:
        """
        Run inference on frame
        
        Args:
            frame: Input image frame (H×W×3)
        
        Returns:
            {
                'detections': [
                    {
                        'class_id': int,
                        'class_name': str,
                        'confidence': float,
                        'bbox': [x1, y1, x2, y2]
                    }
                ],
                'inference_time_ms': float
            }
        """
        if self.model is None:
            logger.warning("Model not loaded, loading now...")
            self.load_model()
        
        try:
            # Start timer
            start_time = time.time()
            
            # Run inference
            results = self.model(frame, conf=self.confidence_threshold, verbose=False)
            
            # Extract detections
            detections = []
            if len(results) > 0:
                result = results[0]
                if result.boxes is not None:
                    for box in result.boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                        detections.append({
                            'class_id': int(box.cls[0].cpu().numpy()),
                            'class_name': result.names[int(box.cls[0].cpu().numpy())],
                            'confidence': float(box.conf[0].cpu().numpy()),
                            'bbox': [int(x1), int(y1), int(x2), int(y2)]
                        })
            
            # Calculate inference time
            inference_time_ms = (time.time() - start_time) * 1000
            
            return {
                'detections': detections,
                'inference_time_ms': inference_time_ms
            }
        except Exception as e:
            logger.error(f"Inference error: {e}")
            return {
                'detections': [],
                'inference_time_ms': 0.0
            }
    
    def warm_up(self, image_size: Tuple[int, int] = (640, 640)):
        """Warmup GPU with dummy inference"""
        try:
            logger.info("Warming up GPU...")
            dummy_frame = np.random.randint(0, 255, (*image_size, 3), dtype=np.uint8)
            for _ in range(3):  # 3 warmup inferences
                _ = self.predict(dummy_frame)
            logger.info("GPU warmup complete")
        except Exception as e:
            logger.warning(f"GPU warmup failed: {e}")


# Singleton instance
yolo_engine: Optional[YOLOv8Inference] = None


def get_yolo_engine() -> YOLOv8Inference:
    """Get or create YOLO inference engine"""
    global yolo_engine
    if yolo_engine is None:
        # Load from config in Phase 2
        yolo_engine = YOLOv8Inference(
            model_path='models/yolov8n.pt',
            device='cuda'
        )
        try:
            yolo_engine.load_model()
            yolo_engine.warm_up()
        except Exception as e:
            logger.error(f"Failed to initialize YOLO engine: {e}")
            # Fall back to CPU if GPU fails
            logger.info("Falling back to CPU...")
            yolo_engine = YOLOv8Inference(
                model_path='models/yolov8n.pt',
                device='cpu'
            )
            yolo_engine.load_model()
    return yolo_engine
