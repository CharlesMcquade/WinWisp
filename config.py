"""
Configuration management for WindowsWhisper
"""
import json
import os
from pathlib import Path

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "hotkey": "ctrl+shift+space",
    "model": "small",  # tiny, base, small, medium, large
    "language": "en",  # Auto-detect if empty, or specify language code
    "auto_paste": True,
    "save_recordings": False,
    "recordings_dir": "recordings"
}


class Config:
    def __init__(self):
        self.config_path = Path(CONFIG_FILE)
        self.data = self.load()
    
    def load(self):
        """Load configuration from file or create default"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                # Merge with defaults to add any new keys
                return {**DEFAULT_CONFIG, **config}
            except Exception as e:
                print(f"Error loading config: {e}")
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.data.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.data[key] = value
        self.save()
    
    def update(self, updates):
        """Update multiple configuration values"""
        self.data.update(updates)
        self.save()


# Global config instance
config = Config()
