"""
Always-on-top recording indicator with audio feedback
"""
import tkinter as tk
from tkinter import Canvas
import threading
import time
import math
import winsound


class RecordingIndicator:
    """
    Always-on-top visual indicator shown during recording.
    Similar to VoiceInk's recording indicator on macOS.
    """
    
    def __init__(self):
        self.window = None
        self.canvas = None
        self.is_visible = False
        self.animation_running = False
        self.pulse_angle = 0
        
    def play_start_tone(self):
        """Play ascending tone to indicate recording started"""
        def play():
            try:
                # Low to high beep (ascending)
                winsound.Beep(400, 100)  # 400Hz for 100ms
                time.sleep(0.05)
                winsound.Beep(600, 100)  # 600Hz for 100ms
            except Exception as e:
                print(f"Error playing start tone: {e}")
        
        threading.Thread(target=play, daemon=True).start()
    
    def play_stop_tone(self):
        """Play descending tone to indicate recording stopped"""
        def play():
            try:
                # High to low beep (descending)
                winsound.Beep(600, 100)  # 600Hz for 100ms
                time.sleep(0.05)
                winsound.Beep(400, 100)  # 400Hz for 100ms
            except Exception as e:
                print(f"Error playing stop tone: {e}")
        
        threading.Thread(target=play, daemon=True).start()
    
    def create_window(self):
        """Create the always-on-top indicator window"""
        self.window = tk.Toplevel()
        self.window.title("")
        
        # Make window frameless
        self.window.overrideredirect(True)
        
        # Set window size (compact indicator)
        width = 200
        height = 60
        
        # Position at top center of screen
        screen_width = self.window.winfo_screenwidth()
        x = (screen_width - width) // 2
        y = 20  # 20px from top
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Always on top
        self.window.attributes('-topmost', True)
        
        # Transparent background support
        self.window.attributes('-alpha', 0.95)
        
        # Create main frame with rounded appearance
        frame = tk.Frame(self.window, bg='#E53935', padx=2, pady=2)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas for pulsing animation
        self.canvas = Canvas(
            frame,
            width=width-4,
            height=height-4,
            bg='#E53935',
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Create recording indicator elements
        # Microphone icon (circle with line)
        center_x = 40
        center_y = 30
        
        # Pulsing circle (will be animated)
        self.pulse_circle = self.canvas.create_oval(
            center_x - 15, center_y - 15,
            center_x + 15, center_y + 15,
            fill='white', outline=''
        )
        
        # Microphone icon
        self.canvas.create_oval(
            center_x - 8, center_y - 8,
            center_x + 8, center_y + 8,
            fill='#E53935', outline='white', width=2
        )
        
        # Text label
        self.canvas.create_text(
            120, 30,
            text='Recording...',
            fill='white',
            font=('Segoe UI', 12, 'bold'),
            anchor='w'
        )
        
        # Blinking dot
        self.blink_dot = self.canvas.create_oval(
            180, 27, 188, 35,
            fill='white', outline=''
        )
        
        self.is_visible = True
        
        # Start animations
        self.animation_running = True
        self.animate_pulse()
        self.animate_blink()
    
    def animate_pulse(self):
        """Animate the pulsing circle effect"""
        if not self.animation_running or not self.window:
            return
        
        try:
            # Calculate pulse size
            self.pulse_angle = (self.pulse_angle + 10) % 360
            scale = 1 + 0.3 * math.sin(math.radians(self.pulse_angle))
            
            # Update pulse circle
            center_x = 40
            center_y = 30
            radius = 15 * scale
            
            self.canvas.coords(
                self.pulse_circle,
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius
            )
            
            # Adjust opacity based on scale
            alpha = int(255 * (1.3 - scale))
            color = f'#{alpha:02x}{alpha:02x}{alpha:02x}'
            self.canvas.itemconfig(self.pulse_circle, fill=color)
            
            # Schedule next frame
            self.window.after(50, self.animate_pulse)
        except:
            pass
    
    def animate_blink(self):
        """Animate the blinking dot"""
        if not self.animation_running or not self.window:
            return
        
        try:
            # Toggle dot visibility
            current_color = self.canvas.itemcget(self.blink_dot, 'fill')
            new_color = 'white' if current_color == '#E53935' else '#E53935'
            self.canvas.itemconfig(self.blink_dot, fill=new_color)
            
            # Schedule next blink
            self.window.after(500, self.animate_blink)
        except:
            pass
    
    def show(self):
        """Show the recording indicator"""
        if not self.is_visible:
            try:
                self.create_window()
                self.play_start_tone()
            except Exception as e:
                print(f"Error showing recording indicator: {e}")
    
    def hide(self):
        """Hide the recording indicator"""
        if self.is_visible and self.window:
            try:
                self.animation_running = False
                self.play_stop_tone()
                
                # Delay destruction slightly to allow tone to play
                def destroy():
                    time.sleep(0.2)
                    if self.window:
                        try:
                            self.window.destroy()
                        except:
                            pass
                    self.window = None
                    self.canvas = None
                    self.is_visible = False
                
                threading.Thread(target=destroy, daemon=True).start()
            except Exception as e:
                print(f"Error hiding recording indicator: {e}")
    
    def update_status(self, text):
        """Update the status text on the indicator"""
        if self.is_visible and self.canvas:
            try:
                # Find and update the text item
                self.canvas.itemconfig(2, text=text)
            except:
                pass


class ProcessingIndicator:
    """
    Simple indicator shown while processing/transcribing
    """
    
    def __init__(self):
        self.window = None
        self.is_visible = False
    
    def show(self, message="Processing..."):
        """Show processing indicator"""
        if self.is_visible:
            return
        
        try:
            self.window = tk.Toplevel()
            self.window.title("")
            self.window.overrideredirect(True)
            
            width = 200
            height = 50
            
            screen_width = self.window.winfo_screenwidth()
            x = (screen_width - width) // 2
            y = 20
            
            self.window.geometry(f"{width}x{height}+{x}+{y}")
            self.window.attributes('-topmost', True)
            self.window.attributes('-alpha', 0.95)
            
            frame = tk.Frame(self.window, bg='#2196F3', padx=15, pady=10)
            frame.pack(fill=tk.BOTH, expand=True)
            
            label = tk.Label(
                frame,
                text=message,
                bg='#2196F3',
                fg='white',
                font=('Segoe UI', 11)
            )
            label.pack()
            
            self.is_visible = True
        except Exception as e:
            print(f"Error showing processing indicator: {e}")
    
    def hide(self):
        """Hide processing indicator"""
        if self.is_visible and self.window:
            try:
                self.window.destroy()
                self.window = None
                self.is_visible = False
            except:
                pass
