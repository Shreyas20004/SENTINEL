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
        # TODO: Implement in Phase 2
        # import cv2
        # cap = cv2.VideoCapture(self.rtsp_url)
        # ...
        pass
    
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
