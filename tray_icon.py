"""
System tray icon management
"""
import pystray
from PIL import Image, ImageDraw
import threading


class TrayIcon:
    def __init__(self, app):
        self.app = app
        self.icon = None
        self.menu = None
    
    def create_icon_image(self, color="white", recording=False):
        """Create a simple microphone icon"""
        # Create an image for the icon
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(image)
        
        # Choose color based on recording state
        mic_color = 'red' if recording else color
        
        # Draw a simple microphone shape
        # Microphone body (rectangle with rounded top)
        draw.ellipse([20, 15, 44, 35], fill=mic_color)
        draw.rectangle([20, 25, 44, 45], fill=mic_color)
        
        # Microphone stand
        draw.rectangle([30, 45, 34, 55], fill=mic_color)
        draw.rectangle([22, 55, 42, 58], fill=mic_color)
        
        return image
    
    def create_menu(self):
        """Create the system tray menu"""
        self.menu = pystray.Menu(
            pystray.MenuItem("Show Window", self.show_window, default=True),
            pystray.MenuItem("Copy Last Transcription", self.copy_transcription),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Settings", self.show_settings),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self.exit_app)
        )
    
    def show_window(self, icon=None, item=None):
        """Show the main window"""
        if self.app.gui:
            self.app.gui.show_window()
    
    def copy_transcription(self, icon=None, item=None):
        """Copy last transcription to clipboard"""
        if self.app.last_transcription:
            from text_paster import copy_to_clipboard
            copy_to_clipboard(self.app.last_transcription)
            self.icon.notify("Transcription copied to clipboard!", "WinWisp")
        else:
            self.icon.notify("No transcription available", "WinWisp")
    
    def show_settings(self, icon=None, item=None):
        """Show settings dialog"""
        self.show_window()
        if self.app.gui:
            self.app.gui.show_settings()
    
    def exit_app(self, icon=None, item=None):
        """Exit the application"""
        self.app.cleanup()
        if self.icon:
            self.icon.stop()
    
    def start(self):
        """Start the system tray icon"""
        self.create_menu()
        
        image = self.create_icon_image()
        self.icon = pystray.Icon(
            "WinWisp",
            image,
            "WinWisp - Speech to Text",
            self.menu
        )
        
        # Run in a separate thread
        icon_thread = threading.Thread(target=self.icon.run)
        icon_thread.daemon = True
        icon_thread.start()
    
    def update_icon(self, recording=False):
        """Update icon appearance based on recording state"""
        if self.icon:
            image = self.create_icon_image(recording=recording)
            self.icon.icon = image
    
    def notify(self, message, title="WinWisp"):
        """Show a notification"""
        if self.icon:
            self.icon.notify(message, title)
    
    def stop(self):
        """Stop the tray icon"""
        if self.icon:
            self.icon.stop()
