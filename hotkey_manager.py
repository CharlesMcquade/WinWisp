"""
Global hotkey management
"""
import keyboard
import threading


class HotkeyManager:
    def __init__(self):
        self.current_hotkey = None
        self.callback = None
        self.is_active = False
    
    def register(self, hotkey, callback):
        """Register a global hotkey"""
        # Unregister previous hotkey if exists
        self.unregister()
        
        try:
            self.current_hotkey = hotkey
            self.callback = callback
            
            # Register the hotkey
            keyboard.add_hotkey(hotkey, self._on_hotkey_pressed)
            self.is_active = True
            
            print(f"Hotkey registered: {hotkey}")
            return True
        except Exception as e:
            print(f"Error registering hotkey: {e}")
            return False
    
    def _on_hotkey_pressed(self):
        """Internal hotkey handler"""
        if self.callback:
            # Run callback in a separate thread to avoid blocking
            thread = threading.Thread(target=self.callback)
            thread.start()
    
    def unregister(self):
        """Unregister the current hotkey"""
        if self.current_hotkey and self.is_active:
            try:
                keyboard.remove_hotkey(self.current_hotkey)
                self.is_active = False
                print(f"Hotkey unregistered: {self.current_hotkey}")
            except Exception as e:
                print(f"Error unregistering hotkey: {e}")
    
    def change_hotkey(self, new_hotkey):
        """Change the hotkey"""
        if self.callback:
            return self.register(new_hotkey, self.callback)
        return False
    
    def cleanup(self):
        """Clean up hotkey resources"""
        self.unregister()
