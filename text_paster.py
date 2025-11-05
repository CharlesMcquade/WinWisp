"""
Text pasting functionality for Windows
"""
import pyperclip
import time
import win32clipboard
import win32con
from pynput.keyboard import Key, Controller


class TextPaster:
    def __init__(self):
        self.keyboard = Controller()
    
    def paste_text(self, text):
        """
        Paste text at the current cursor location
        Uses clipboard to paste the text
        """
        if not text:
            return False
        
        try:
            # Save current clipboard content
            old_clipboard = self.get_clipboard()
            
            # Copy new text to clipboard
            pyperclip.copy(text)
            
            # Small delay to ensure clipboard is updated
            time.sleep(0.1)
            
            # Simulate Ctrl+V to paste
            self.keyboard.press(Key.ctrl)
            self.keyboard.press('v')
            self.keyboard.release('v')
            self.keyboard.release(Key.ctrl)
            
            # Wait a bit before restoring clipboard
            time.sleep(0.2)
            
            # Restore old clipboard content
            if old_clipboard is not None:
                pyperclip.copy(old_clipboard)
            
            return True
        except Exception as e:
            print(f"Error pasting text: {e}")
            return False
    
    def get_clipboard(self):
        """Get current clipboard content"""
        try:
            return pyperclip.paste()
        except:
            return None
    
    def set_clipboard(self, text):
        """Set clipboard content"""
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"Error setting clipboard: {e}")
            return False


def paste_text_at_cursor(text):
    """Helper function to paste text"""
    paster = TextPaster()
    return paster.paste_text(text)


def copy_to_clipboard(text):
    """Helper function to copy text to clipboard"""
    paster = TextPaster()
    return paster.set_clipboard(text)
