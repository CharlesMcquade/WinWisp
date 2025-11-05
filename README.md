# WindowsWhisper

A Windows application that uses OpenAI's Whisper model to convert speech to text, activated by a global hotkey.

## Features

- 🎤 **Global Hotkey Activation**: Press `Ctrl+Shift+Space` to start/stop recording
- 🎯 **Auto-Paste**: Transcribed text is automatically pasted at the active cursor location
- 📋 **Clipboard Support**: Copy the last transcription to clipboard from the tray menu
- 🖥️ **System Tray**: Runs minimized in the system tray
- ⚙️ **Configurable**: Settings window to customize hotkey and Whisper model
- 🔊 **Real-time Feedback**: Visual and audio feedback during recording

## Installation

1. **Prerequisites**:
   - Python 3.8 or higher
   - FFmpeg (required by Whisper)
   - Windows 10/11

2. **Install FFmpeg**:
   - Download from: https://ffmpeg.org/download.html
   - Add to system PATH

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **First Run**:
   ```bash
   python main.py
   ```
   The first run will download the Whisper model (this may take a few minutes).

## Usage

1. **Start the application**: Run `python main.py`
2. **The app minimizes to system tray** with a microphone icon
3. **Press `Ctrl+Shift+Space`** to start recording
4. **Press `Ctrl+Shift+Space` again** to stop and transcribe
5. **Text is automatically pasted** at your cursor location

### Tray Menu Options:
- **Show Window**: Open the main window
- **Copy Last Transcription**: Copy the last transcription to clipboard
- **Settings**: Configure hotkey and Whisper model
- **Exit**: Close the application

## Configuration

### Whisper Models
Available models (in order of size and accuracy):
- `tiny` - Fastest, least accurate (~75MB)
- `base` - Fast, good for real-time (~150MB)
- `small` - Balanced (~500MB) **[Default]**
- `medium` - More accurate (~1.5GB)
- `large` - Most accurate (~3GB)

### Hotkey
Default: `Ctrl+Shift+Space`
Can be customized in Settings window.

## Troubleshooting

### Audio Issues
- Ensure your microphone is set as the default recording device
- Check microphone permissions in Windows Settings

### Whisper Model Download
- First run downloads the selected model
- Requires internet connection
- Models are cached locally

### Hotkey Not Working
- Ensure the application is running (check system tray)
- Check for hotkey conflicts with other applications
- Try running as Administrator

## License

MIT License
