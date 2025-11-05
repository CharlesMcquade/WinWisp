"""
WinWisp - Speech to Text using OpenAI Whisper
Main application entry point

This application uses OpenAI's Whisper model for automatic speech recognition.
Whisper: https://github.com/openai/whisper
Paper: "Robust Speech Recognition via Large-Scale Weak Supervision"
       https://arxiv.org/abs/2212.04356

Copyright (c) 2025 WinWisp
Licensed under the MIT License

This is a third-party application and is not affiliated with OpenAI.
"""
import sys
import os
import threading
import time
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
log_dir = Path.home() / "AppData" / "Local" / "WinWisp" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f"winwisp_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout) if sys.stdout else logging.NullHandler()
    ]
)

logger = logging.getLogger(__name__)

from config import config
from audio_recorder import AudioRecorder
from whisper_handler import WhisperHandler
from hotkey_manager import HotkeyManager
from text_paster import paste_text_at_cursor, copy_to_clipboard
from gui import WhisperGUI
from tray_icon import TrayIcon
from recording_indicator import RecordingIndicator, ProcessingIndicator


class WinWispApp:
    def __init__(self):
        logger.info("Starting WinWisp...")
        
        # Ensure config directory exists
        config_dir = Path.home() / "AppData" / "Local" / "WinWisp"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # Create recordings directory
        recordings_dir = config_dir / "recordings"
        recordings_dir.mkdir(parents=True, exist_ok=True)
        
        # Change working directory to config directory
        os.chdir(config_dir)
        logger.info(f"Working directory: {os.getcwd()}")
        
        # Components
        self.config = config
        self.audio_recorder = AudioRecorder()
        
        # Initialize WhisperHandler
        model_name = self.config.get('model', 'small')
        self.whisper_handler = WhisperHandler(
            model_name=model_name,
            language=self.config.get('language', 'en')
        )
        
        # Check if this is first run (no model downloaded)
        self.is_first_run = not self._model_exists(model_name)
        
        # Only load model in background if not first run
        if not self.is_first_run:
            logger.info("Loading Whisper model in background...")
            model_thread = threading.Thread(target=self.whisper_handler.load_model)
            model_thread.daemon = True
            model_thread.start()
        else:
            logger.info("First run detected - model will be downloaded when user saves settings")
        
        self.hotkey_manager = HotkeyManager()
        
        # State
        self.is_recording = False
        self.last_transcription = ""
        self.last_audio_file = None
        
        # GUI and Tray
        self.gui = None
        self.tray_icon = None
        
        # Recording indicator
        self.recording_indicator = RecordingIndicator()
        self.processing_indicator = ProcessingIndicator()
    
    def _model_exists(self, model_name):
        """Check if a Whisper model has been downloaded"""
        cache_dir = Path.home() / ".cache" / "whisper"
        model_files = {
            'tiny': 'tiny.pt',
            'base': 'base.pt',
            'small': 'small.pt',
            'medium': 'medium.pt',
            'large': 'large.pt'
        }
        model_file = model_files.get(model_name, 'small.pt')
        model_path = cache_dir / model_file
        return model_path.exists()
    
    def initialize(self):
        """Initialize the application"""
        try:
            # Create GUI
            logger.info("Creating GUI...")
            self.gui = WhisperGUI(self)
            self.gui.create_window()
            
            # On first run, show the window so user can configure settings
            if self.is_first_run:
                logger.info("First run - showing settings window")
                self.gui.show_window()
                # Show settings dialog immediately
                self.gui.window.after(500, self.gui.show_settings)
            
            # Create system tray icon
            logger.info("Creating system tray icon...")
            self.tray_icon = TrayIcon(self)
            self.tray_icon.start()
            
            # Register hotkey
            hotkey = self.config.get('hotkey', 'ctrl+shift+space')
            logger.info(f"Registering hotkey: {hotkey}")
            if not self.hotkey_manager.register(hotkey, self.on_hotkey_pressed):
                logger.error("Failed to register hotkey!")
                return False
            
            logger.info(f"WinWisp is ready!")
            logger.info(f"Press {hotkey} to start/stop recording")
            
            # Show notification only if not first run
            if not self.is_first_run and self.tray_icon:
                self.tray_icon.notify(
                    f"Press {hotkey.upper()} to start recording",
                    "WinWisp Ready"
                )
            
            return True
        except Exception as e:
            logger.error(f"Failed to initialize: {e}", exc_info=True)
            return False
    
    def on_hotkey_pressed(self):
        """Handle hotkey press - toggle recording"""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Start audio recording"""
        if self.is_recording:
            return
        
        logger.info("Starting recording...")
        self.is_recording = True
        
        # Show recording indicator with audio feedback
        self.recording_indicator.show()
        
        # Update UI
        if self.gui:
            self.gui.update_recording_status(True)
            self.gui.update_status("Recording...")
        
        if self.tray_icon:
            self.tray_icon.update_icon(recording=True)
        
        # Start recording
        if not self.audio_recorder.start_recording():
            logger.error("Failed to start recording!")
            self.is_recording = False
            self.recording_indicator.hide()
            if self.gui:
                self.gui.update_recording_status(False)
                self.gui.update_status("Failed to start recording")
            return
    
    def stop_recording(self):
        """Stop recording and transcribe"""
        if not self.is_recording:
            return
        
        logger.info("Stopping recording...")
        self.is_recording = False
        
        # Hide recording indicator with audio feedback
        self.recording_indicator.hide()
        
        # Show processing indicator
        self.processing_indicator.show("Processing audio...")
        
        # Update UI
        if self.gui:
            self.gui.update_recording_status(False)
            self.gui.update_status("Processing...")
        
        if self.tray_icon:
            self.tray_icon.update_icon(recording=False)
        
        # Stop recording and get file
        audio_file = self.audio_recorder.stop_recording()
        
        if not audio_file:
            logger.warning("No audio recorded")
            self.processing_indicator.hide()
            if self.gui:
                self.gui.update_status("No audio recorded")
            return
        
        self.last_audio_file = audio_file
        
        # Transcribe in background
        logger.info(f"Transcribing audio file: {audio_file}")
        self.whisper_handler.transcribe_async(audio_file, self.on_transcription_complete)
    
    def on_transcription_complete(self, text, error):
        """Handle transcription completion"""
        # Hide processing indicator
        self.processing_indicator.hide()
        
        if error:
            logger.error(f"Transcription error: {error}")
            if self.gui:
                self.gui.update_status(f"Error: {error}")
            if self.tray_icon:
                self.tray_icon.notify("Transcription failed", "WinWisp")
            return
        
        if not text:
            logger.warning("No text transcribed")
            if self.gui:
                self.gui.update_status("No speech detected")
            if self.tray_icon:
                self.tray_icon.notify("No speech detected", "WinWisp")
            return
        
        logger.info(f"Transcription complete: {text}")
        self.last_transcription = text
        
        # Update GUI
        if self.gui:
            self.gui.update_transcription(text)
            self.gui.update_status("Ready")
        
        # Paste text if auto-paste is enabled
        if self.config.get('auto_paste', True):
            logger.info("Pasting text at cursor...")
            if paste_text_at_cursor(text):
                if self.tray_icon:
                    self.tray_icon.notify("Text pasted!", "WinWisp")
            else:
                logger.warning("Failed to paste text")
                if self.tray_icon:
                    self.tray_icon.notify("Failed to paste text", "WinWisp")
                # Copy to clipboard as fallback
                copy_to_clipboard(text)
        else:
            # Just copy to clipboard
            copy_to_clipboard(text)
            if self.tray_icon:
                self.tray_icon.notify("Text copied to clipboard", "WinWisp")
        
        # Clean up audio file if not saving recordings
        if not self.config.get('save_recordings', False):
            try:
                os.remove(self.last_audio_file)
            except:
                pass
    
    def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up...")
        
        self.hotkey_manager.cleanup()
        self.audio_recorder.cleanup()
        
        if self.tray_icon:
            self.tray_icon.stop()
    
    def run(self):
        """Run the application"""
        if not self.initialize():
            logger.error("Failed to initialize application")
            return 1
        
        try:
            # Run GUI main loop
            if self.gui:
                self.gui.run()
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        except Exception as e:
            logger.error(f"Application error: {e}", exc_info=True)
        finally:
            self.cleanup()
        
        return 0


def main():
    """Main entry point"""
    try:
        app = WinWispApp()
        return app.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
