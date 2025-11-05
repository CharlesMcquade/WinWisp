"""
Audio recording functionality
"""
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import threading
from datetime import datetime
from pathlib import Path


class AudioRecorder:
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        
        self.frames = []
        self.is_recording = False
        self.recording_thread = None
    
    def start_recording(self):
        """Start recording audio"""
        if self.is_recording:
            return False
        
        self.frames = []
        self.is_recording = True
        
        try:
            # Start recording in a separate thread
            self.recording_thread = threading.Thread(target=self._record)
            self.recording_thread.start()
            return True
        except Exception as e:
            print(f"Error starting recording: {e}")
            self.is_recording = False
            return False
    
    def _record(self):
        """Internal recording loop"""
        try:
            # Record audio using sounddevice
            # We'll record in chunks and append to frames
            def callback(indata, frames, time, status):
                if status:
                    print(f"Recording status: {status}")
                if self.is_recording:
                    self.frames.append(indata.copy())
            
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=callback,
                dtype=np.float32
            ):
                while self.is_recording:
                    sd.sleep(100)  # Sleep for 100ms
        except Exception as e:
            print(f"Error during recording: {e}")
            self.is_recording = False
    
    def stop_recording(self):
        """Stop recording and return the audio file path"""
        if not self.is_recording:
            return None
        
        self.is_recording = False
        
        if self.recording_thread:
            self.recording_thread.join()
        
        if not self.frames:
            return None
        
        # Concatenate all recorded frames
        recording = np.concatenate(self.frames, axis=0)
        
        # Save to temporary file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_dir = Path("recordings")
        temp_dir.mkdir(exist_ok=True)
        
        output_file = temp_dir / f"recording_{timestamp}.wav"
        
        try:
            # Convert to int16 for WAV file
            recording_int16 = (recording * 32767).astype(np.int16)
            
            # Save as WAV file
            write(str(output_file), self.sample_rate, recording_int16)
            
            return str(output_file)
        except Exception as e:
            print(f"Error saving recording: {e}")
            return None
    
    def get_recording_duration(self):
        """Get current recording duration in seconds"""
        if not self.frames:
            return 0
        
        total_samples = sum(len(frame) for frame in self.frames)
        duration = total_samples / self.sample_rate
        return duration
    
    def cleanup(self):
        """Clean up audio resources"""
        if self.is_recording:
            self.stop_recording()
    
    def __del__(self):
        self.cleanup()
