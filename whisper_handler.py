"""
Whisper model handling for speech-to-text conversion
"""
import whisper
import torch
import threading
from pathlib import Path


class WhisperHandler:
    def __init__(self, model_name="small", language="en"):
        self.model_name = model_name
        self.language = language if language else None
        self.model = None
        self.is_loaded = False
        self.loading_lock = threading.Lock()
    
    def load_model(self):
        """Load the Whisper model (can be slow on first run)"""
        with self.loading_lock:
            if self.is_loaded:
                return True
            
            try:
                print(f"Loading Whisper model: {self.model_name}")
                
                # Use GPU if available
                device = "cuda" if torch.cuda.is_available() else "cpu"
                print(f"Using device: {device}")
                
                self.model = whisper.load_model(self.model_name, device=device)
                self.is_loaded = True
                print("Model loaded successfully")
                return True
            except Exception as e:
                print(f"Error loading model: {e}")
                return False
    
    def transcribe(self, audio_file, callback=None):
        """
        Transcribe audio file to text
        
        Args:
            audio_file: Path to audio file
            callback: Optional callback function to call with result
        """
        if not self.is_loaded:
            if not self.load_model():
                if callback:
                    callback(None, "Model not loaded")
                return None
        
        try:
            print(f"Transcribing: {audio_file}")
            
            # Transcribe options
            options = {
                "fp16": torch.cuda.is_available(),  # Use FP16 on GPU
                "language": self.language,
                "task": "transcribe"
            }
            
            result = self.model.transcribe(audio_file, **options)
            text = result["text"].strip()
            
            print(f"Transcription: {text}")
            
            if callback:
                callback(text, None)
            
            return text
        except Exception as e:
            error_msg = f"Error during transcription: {e}"
            print(error_msg)
            if callback:
                callback(None, error_msg)
            return None
    
    def transcribe_async(self, audio_file, callback):
        """Transcribe in a separate thread"""
        thread = threading.Thread(
            target=self.transcribe,
            args=(audio_file, callback)
        )
        thread.start()
    
    def change_model(self, model_name):
        """Change the Whisper model"""
        if model_name == self.model_name and self.is_loaded:
            return True
        
        self.model_name = model_name
        self.model = None
        self.is_loaded = False
        
        return self.load_model()
    
    def change_language(self, language):
        """Change the target language"""
        self.language = language if language else None
