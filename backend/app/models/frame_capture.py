"""
OpenCV RTSP Frame Capture - Phase 1 Placeholder

Full implementation in Phase 2

Features:
- Capture RTSP/ONVIF streams
- Frame buffering (ring buffer)
- FPS control
- Connection health checks
- Thread-safe frame access
"""

import logging
import threading
from collections import deque
from datetime import datetime
from typing import Optional, Dict
import numpy as np

logger = logging.getLogger(__name__)


class RTSPCapture:
    """RTSP stream capture"""
    
    def __init__(
        self,
        camera_id: str,
        rtsp_url: str,
        fps: int = 25,
        buffer_size: int = 128
    ):
        """
        Initialize RTSP capture
        
        Args:
            camera_id: Camera identifier
            rtsp_url: RTSP stream URL
            fps: Target FPS (default 25)
            buffer_size: Frame buffer size
        """
        self.camera_id = camera_id
        self.rtsp_url = rtsp_url
        self.fps = fps
        self.buffer_size = buffer_size
        self.frame_buffer = deque(maxlen=buffer_size)
        
        self.is_running = False
        self.capture_thread: Optional[threading.Thread] = None
        self.last_frame_time = None
        self.frame_count = 0
        
        logger.info(f"RTSPCapture initialized for {camera_id}: {rtsp_url}")
    
    def start(self):
        """Start capture thread"""
        if self.is_running:
            logger.warning(f"Capture already running for {self.camera_id}")
            return
        
        self.is_running = True
        self.capture_thread = threading.Thread(
            target=self._capture_loop,
            daemon=True
        )
        self.capture_thread.start()
        logger.info(f"Started capture thread for {self.camera_id}")
    
    def _capture_loop(self):
        """Capture frames from RTSP stream"""
        import cv2
        import time
        
        cap = None
        retry_count = 0
        max_retries = 5
        
        try:
            while self.is_running:
                # Try to open stream if not open
                if cap is None:
                    logger.info(f"Attempting to open {self.camera_id}: {self.rtsp_url}")
                    cap = cv2.VideoCapture(self.rtsp_url)
                    
                    # Set camera properties for better performance
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer lag
                    cap.set(cv2.CAP_PROP_FPS, self.fps)
                    
                    if not cap.isOpened():
                        logger.error(f"Failed to open {self.camera_id}")
                        retry_count += 1
                        if retry_count > max_retries:
                            logger.error(f"Max retries exceeded for {self.camera_id}")
                            break
                        time.sleep(5)  # Wait before retry
                        continue
                    
                    logger.info(f"Successfully opened {self.camera_id}")
                    retry_count = 0
                
                # Capture frame
                ret, frame = cap.read()
                
                if not ret:
                    logger.warning(f"Failed to read frame from {self.camera_id}")
                    cap.release()
                    cap = None
                    continue
                
                # Store frame with metadata
                self.frame_buffer.append({
                    'frame': frame,
                    'timestamp': datetime.now().isoformat(),
                    'camera_id': self.camera_id,
                    'shape': frame.shape
                })
                
                self.frame_count += 1
                self.last_frame_time = datetime.now()
                
                # Control FPS
                frame_interval = 1.0 / self.fps
                time.sleep(frame_interval)
        
        except Exception as e:
            logger.error(f"Error in capture loop for {self.camera_id}: {e}")
        finally:
            if cap is not None:
                cap.release()
                logger.info(f"Released camera {self.camera_id}")
    
    def get_latest_frame(self) -> Optional[Dict]:
        """
        Get latest frame from buffer
        
        Returns:
            {
                'frame': np.ndarray (H×W×3),
                'timestamp': datetime,
                'camera_id': str
            }
        """
        if self.frame_buffer:
            return self.frame_buffer[-1]
        return None
    
    def get_all_frames(self) -> list:
        """Get all buffered frames"""
        return list(self.frame_buffer)
    
    def get_stats(self) -> Dict:
        """Get capture statistics"""
        return {
            'camera_id': self.camera_id,
            'is_running': self.is_running,
            'buffer_size': len(self.frame_buffer),
            'total_frames': self.frame_count,
            'fps': self.fps,
            'last_frame_time': self.last_frame_time
        }
    
    def stop(self):
        """Stop capture thread"""
        self.is_running = False
        if self.capture_thread:
            self.capture_thread.join(timeout=5)
        logger.info(f"Stopped capture thread for {self.camera_id}")


class StreamManager:
    """Manage multiple RTSP streams"""
    
    def __init__(self):
        """Initialize stream manager"""
        self.streams: Dict[str, RTSPCapture] = {}
        logger.info("StreamManager initialized")
    
    def add_stream(self, camera_id: str, rtsp_url: str) -> RTSPCapture:
        """Register new stream"""
        if camera_id in self.streams:
            logger.warning(f"Stream {camera_id} already exists")
            return self.streams[camera_id]
        
        capture = RTSPCapture(camera_id, rtsp_url)
        capture.start()
        self.streams[camera_id] = capture
        logger.info(f"Added stream {camera_id}")
        return capture
    
    def remove_stream(self, camera_id: str):
        """Stop and remove stream"""
        if camera_id in self.streams:
            self.streams[camera_id].stop()
            del self.streams[camera_id]
            logger.info(f"Removed stream {camera_id}")
    
    def get_frame(self, camera_id: str) -> Optional[Dict]:
        """Get latest frame from stream"""
        if camera_id in self.streams:
            return self.streams[camera_id].get_latest_frame()
        return None
    
    def get_stats(self) -> Dict:
        """Get stats for all streams"""
        return {
            camera_id: stream.get_stats()
            for camera_id, stream in self.streams.items()
        }


# Singleton instance
stream_manager: Optional[StreamManager] = None


def get_stream_manager() -> StreamManager:
    """Get or create stream manager"""
    global stream_manager
    if stream_manager is None:
        stream_manager = StreamManager()
    return stream_manager
