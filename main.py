"""
WindowsWhisper - Speech to Text using OpenAI Whisper
Main application entry point
"""
import sys
import os
import threading
import time
from pathlib import Path

from config import config
from audio_recorder import AudioRecorder
from whisper_handler import WhisperHandler
from hotkey_manager import HotkeyManager
from text_paster import paste_text_at_cursor, copy_to_clipboard
from gui import WhisperGUI
from tray_icon import TrayIcon


class WindowsWhisperApp:
    def __init__(self):
        print("Starting WindowsWhisper...")
        
        # Components
        self.config = config
        self.audio_recorder = AudioRecorder()
        self.whisper_handler = WhisperHandler(
            model_name=self.config.get('model', 'small'),
            language=self.config.get('language', 'en')
        )
        self.hotkey_manager = HotkeyManager()
        
        # State
        self.is_recording = False
        self.last_transcription = ""
        self.last_audio_file = None
        
        # GUI and Tray
        self.gui = None
        self.tray_icon = None
        
        # Load model in background
        print("Loading Whisper model in background...")
        model_thread = threading.Thread(target=self.whisper_handler.load_model)
        model_thread.daemon = True
        model_thread.start()
    
    def initialize(self):
        """Initialize the application"""
        # Create GUI
        print("Creating GUI...")
        self.gui = WhisperGUI(self)
        self.gui.create_window()
        
        # Create system tray icon
        print("Creating system tray icon...")
        self.tray_icon = TrayIcon(self)
        self.tray_icon.start()
        
        # Register hotkey
        hotkey = self.config.get('hotkey', 'ctrl+shift+space')
        print(f"Registering hotkey: {hotkey}")
        if not self.hotkey_manager.register(hotkey, self.on_hotkey_pressed):
            print("Failed to register hotkey!")
            return False
        
        print(f"WindowsWhisper is ready!")
        print(f"Press {hotkey} to start/stop recording")
        
        # Show notification
        if self.tray_icon:
            self.tray_icon.notify(
                f"Press {hotkey.upper()} to start recording",
                "WindowsWhisper Ready"
            )
        
        return True
    
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
        
        print("Starting recording...")
        self.is_recording = True
        
        # Update UI
        if self.gui:
            self.gui.update_recording_status(True)
            self.gui.update_status("Recording...")
        
        if self.tray_icon:
            self.tray_icon.update_icon(recording=True)
            self.tray_icon.notify("Recording started", "WindowsWhisper")
        
        # Start recording
        if not self.audio_recorder.start_recording():
            print("Failed to start recording!")
            self.is_recording = False
            if self.gui:
                self.gui.update_recording_status(False)
                self.gui.update_status("Failed to start recording")
            return
    
    def stop_recording(self):
        """Stop recording and transcribe"""
        if not self.is_recording:
            return
        
        print("Stopping recording...")
        self.is_recording = False
        
        # Update UI
        if self.gui:
            self.gui.update_recording_status(False)
            self.gui.update_status("Processing...")
        
        if self.tray_icon:
            self.tray_icon.update_icon(recording=False)
            self.tray_icon.notify("Processing audio...", "WindowsWhisper")
        
        # Stop recording and get file
        audio_file = self.audio_recorder.stop_recording()
        
        if not audio_file:
            print("No audio recorded")
            if self.gui:
                self.gui.update_status("No audio recorded")
            return
        
        self.last_audio_file = audio_file
        
        # Transcribe in background
        print(f"Transcribing audio file: {audio_file}")
        self.whisper_handler.transcribe_async(audio_file, self.on_transcription_complete)
    
    def on_transcription_complete(self, text, error):
        """Handle transcription completion"""
        if error:
            print(f"Transcription error: {error}")
            if self.gui:
                self.gui.update_status(f"Error: {error}")
            if self.tray_icon:
                self.tray_icon.notify("Transcription failed", "WindowsWhisper")
            return
        
        if not text:
            print("No text transcribed")
            if self.gui:
                self.gui.update_status("No speech detected")
            if self.tray_icon:
                self.tray_icon.notify("No speech detected", "WindowsWhisper")
            return
        
        print(f"Transcription complete: {text}")
        self.last_transcription = text
        
        # Update GUI
        if self.gui:
            self.gui.update_transcription(text)
            self.gui.update_status("Ready")
        
        # Paste text if auto-paste is enabled
        if self.config.get('auto_paste', True):
            print("Pasting text at cursor...")
            if paste_text_at_cursor(text):
                if self.tray_icon:
                    self.tray_icon.notify("Text pasted!", "WindowsWhisper")
            else:
                print("Failed to paste text")
                if self.tray_icon:
                    self.tray_icon.notify("Failed to paste text", "WindowsWhisper")
                # Copy to clipboard as fallback
                copy_to_clipboard(text)
        else:
            # Just copy to clipboard
            copy_to_clipboard(text)
            if self.tray_icon:
                self.tray_icon.notify("Text copied to clipboard", "WindowsWhisper")
        
        # Clean up audio file if not saving recordings
        if not self.config.get('save_recordings', False):
            try:
                os.remove(self.last_audio_file)
            except:
                pass
    
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up...")
        
        self.hotkey_manager.cleanup()
        self.audio_recorder.cleanup()
        
        if self.tray_icon:
            self.tray_icon.stop()
    
    def run(self):
        """Run the application"""
        if not self.initialize():
            print("Failed to initialize application")
            return 1
        
        try:
            # Run GUI main loop
            if self.gui:
                self.gui.run()
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.cleanup()
        
        return 0


def main():
    """Main entry point"""
    app = WindowsWhisperApp()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
