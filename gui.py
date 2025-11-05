"""
GUI for WinWisp using tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading


class WhisperGUI:
    def __init__(self, app):
        self.app = app
        self.window = None
        self.is_visible = False
        
        # Status variables
        self.status_var = None
        self.recording_var = None
        self.last_transcription_var = None
    
    def create_window(self):
        """Create the main GUI window"""
        self.window = tk.Tk()
        self.window.title("WinWisp")
        self.window.geometry("600x500")
        
        # Prevent window from closing, minimize to tray instead
        self.window.protocol("WM_DELETE_WINDOW", self.hide_window)
        
        # Set window icon (if available)
        # self.window.iconbitmap("icon.ico")
        
        # Create UI components
        self._create_widgets()
        
        # Start hidden
        self.window.withdraw()
        
        return self.window
    
    def _create_widgets(self):
        """Create GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="WinWisp",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Status Frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        self.status_var = tk.StringVar(value="Ready")
        self.recording_var = tk.StringVar(value="Not Recording")
        
        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(status_frame, textvariable=self.status_var).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(status_frame, text="Recording:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(status_frame, textvariable=self.recording_var).grid(row=1, column=1, sticky=tk.W)
        
        # Last Transcription Frame
        trans_frame = ttk.LabelFrame(main_frame, text="Last Transcription", padding="10")
        trans_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        trans_frame.columnconfigure(0, weight=1)
        trans_frame.rowconfigure(0, weight=1)
        
        self.transcription_text = scrolledtext.ScrolledText(
            trans_frame,
            wrap=tk.WORD,
            width=60,
            height=10,
            font=("Arial", 10)
        )
        self.transcription_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Copy button
        copy_btn = ttk.Button(
            trans_frame,
            text="Copy to Clipboard",
            command=self.copy_last_transcription
        )
        copy_btn.grid(row=1, column=0, pady=(5, 0))
        
        # Info Frame
        info_frame = ttk.LabelFrame(main_frame, text="Information", padding="10")
        info_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        info_text = f"Hotkey: {self.app.config.get('hotkey', 'ctrl+shift+space').upper()}\n"
        info_text += f"Model: {self.app.config.get('model', 'small')}\n"
        info_text += "\nPress the hotkey to start recording.\nPress again to stop and transcribe."
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.grid(row=0, column=0, sticky=tk.W)
        
        # Buttons Frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
        settings_btn = ttk.Button(
            buttons_frame,
            text="Settings",
            command=self.show_settings
        )
        settings_btn.grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))
        
        minimize_btn = ttk.Button(
            buttons_frame,
            text="Minimize to Tray",
            command=self.hide_window
        )
        minimize_btn.grid(row=0, column=1, padx=(5, 0), sticky=(tk.W, tk.E))
    
    def show_window(self):
        """Show the main window"""
        if self.window:
            self.window.deiconify()
            self.window.lift()
            self.window.focus_force()
            self.is_visible = True
    
    def hide_window(self):
        """Hide the main window"""
        if self.window:
            self.window.withdraw()
            self.is_visible = False
    
    def update_status(self, status):
        """Update status label"""
        if self.status_var:
            self.status_var.set(status)
    
    def update_recording_status(self, is_recording):
        """Update recording status"""
        if self.recording_var:
            status = "Recording..." if is_recording else "Not Recording"
            self.recording_var.set(status)
    
    def update_transcription(self, text):
        """Update last transcription display"""
        if self.transcription_text:
            self.transcription_text.delete(1.0, tk.END)
            self.transcription_text.insert(1.0, text if text else "No transcription yet")
    
    def copy_last_transcription(self):
        """Copy last transcription to clipboard"""
        if self.app.last_transcription:
            from text_paster import copy_to_clipboard
            if copy_to_clipboard(self.app.last_transcription):
                messagebox.showinfo("Success", "Transcription copied to clipboard!")
            else:
                messagebox.showerror("Error", "Failed to copy to clipboard")
        else:
            messagebox.showwarning("No Transcription", "No transcription available to copy")
    
    def show_settings(self):
        """Show settings dialog"""
        SettingsDialog(self.window, self.app)
    
    def run(self):
        """Run the GUI main loop"""
        if self.window:
            self.window.mainloop()


class SettingsDialog:
    def __init__(self, parent, app):
        self.app = app
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create settings widgets"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Hotkey setting
        ttk.Label(main_frame, text="Hotkey:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        self.hotkey_var = tk.StringVar(value=self.app.config.get('hotkey'))
        hotkey_entry = ttk.Entry(main_frame, textvariable=self.hotkey_var, width=30)
        hotkey_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(
            main_frame,
            text="Examples: ctrl+shift+space, alt+r, ctrl+alt+w",
            font=("Arial", 8)
        ).grid(row=2, column=0, sticky=tk.W, pady=(0, 15))
        
        # Model setting
        ttk.Label(main_frame, text="Whisper Model:", font=("Arial", 10, "bold")).grid(
            row=3, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        self.model_var = tk.StringVar(value=self.app.config.get('model'))
        models = ["tiny", "base", "small", "medium", "large"]
        model_combo = ttk.Combobox(
            main_frame,
            textvariable=self.model_var,
            values=models,
            state="readonly",
            width=27
        )
        model_combo.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        model_info = {
            "tiny": "Fastest, ~75MB",
            "base": "Fast, ~150MB",
            "small": "Balanced, ~500MB (Recommended)",
            "medium": "Accurate, ~1.5GB",
            "large": "Most accurate, ~3GB"
        }
        
        self.model_info_var = tk.StringVar(value=model_info.get(self.model_var.get(), ""))
        model_info_label = ttk.Label(
            main_frame,
            textvariable=self.model_info_var,
            font=("Arial", 8)
        )
        model_info_label.grid(row=5, column=0, sticky=tk.W, pady=(0, 15))
        
        # Update info when model changes
        def update_model_info(*args):
            self.model_info_var.set(model_info.get(self.model_var.get(), ""))
        
        self.model_var.trace('w', update_model_info)
        
        # Language setting
        ttk.Label(main_frame, text="Language:", font=("Arial", 10, "bold")).grid(
            row=6, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        self.language_var = tk.StringVar(value=self.app.config.get('language', 'en'))
        language_entry = ttk.Entry(main_frame, textvariable=self.language_var, width=30)
        language_entry.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(
            main_frame,
            text="Leave as 'en' for English, or use ISO language codes",
            font=("Arial", 8)
        ).grid(row=8, column=0, sticky=tk.W, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        save_btn = ttk.Button(button_frame, text="Save", command=self.save_settings)
        save_btn.grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy)
        cancel_btn.grid(row=0, column=1, padx=(5, 0), sticky=(tk.W, tk.E))
        
        # Configure grid weights
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
    
    def save_settings(self):
        """Save settings and apply changes"""
        new_hotkey = self.hotkey_var.get().strip()
        new_model = self.model_var.get()
        new_language = self.language_var.get().strip()
        
        # Validate hotkey
        if not new_hotkey:
            messagebox.showerror("Error", "Hotkey cannot be empty")
            return
        
        # Update configuration
        old_hotkey = self.app.config.get('hotkey')
        old_model = self.app.config.get('model')
        
        self.app.config.update({
            'hotkey': new_hotkey,
            'model': new_model,
            'language': new_language
        })
        
        # Apply changes
        changes_made = False
        
        # Update hotkey if changed
        if new_hotkey != old_hotkey:
            if self.app.hotkey_manager.change_hotkey(new_hotkey):
                messagebox.showinfo("Success", f"Hotkey changed to: {new_hotkey}")
                changes_made = True
            else:
                messagebox.showerror("Error", "Failed to register new hotkey")
                self.app.config.set('hotkey', old_hotkey)
                return
        
        # Update model if changed
        if new_model != old_model:
            messagebox.showinfo(
                "Model Change",
                f"Model will be changed to '{new_model}'.\nThis may take a few moments on next use."
            )
            self.app.whisper_handler.change_model(new_model)
            changes_made = True
        
        # Update language
        self.app.whisper_handler.change_language(new_language)
        
        if not changes_made:
            messagebox.showinfo("Info", "Settings saved")
        
        self.dialog.destroy()
