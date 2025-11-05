# WinWisp v1.0.0 - Initial Release

**Release Date**: November 4, 2025

## 🎉 Welcome to WinWisp!

WinWisp is a Windows application that uses OpenAI's Whisper model to convert speech to text, activated by a global hotkey. This is the first public release!

## ✨ Features

- **🎤 Global Hotkey Activation**: Press `Ctrl+Shift+Space` to start/stop recording
- **🎯 Auto-Paste**: Transcribed text is automatically pasted at your cursor location
- **📋 Clipboard Support**: Copy the last transcription to clipboard from the tray menu
- **🖥️ System Tray**: Runs minimized in the system tray
- **⚙️ Configurable**: Settings window to customize hotkey and Whisper model
- **🔊 Real-time Feedback**: Visual and audio feedback during recording

## 📦 Installation (Current Release)

### Requirements
1. Python 3.8 or higher
2. FFmpeg (required by Whisper)
3. Windows 10/11

### Quick Start

1. **Clone or download the repository**:
   ```bash
   git clone https://github.com/CharlesMcquade/WinWisp.git
   cd WinWisp
   ```

2. **Install FFmpeg**:
   - Download from: https://ffmpeg.org/download.html
   - Add to system PATH

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run WinWisp**:
   ```bash
   python main.py
   ```

The first run will download the Whisper model (this may take a few minutes depending on the model size).

## 🎮 Usage

1. **Launch the app**: Run `python main.py`
2. **The app minimizes to system tray** with a microphone icon
3. **Press `Ctrl+Shift+Space`** to start recording (icon turns red)
4. **Speak your message**
5. **Press `Ctrl+Shift+Space` again** to stop and transcribe
6. **Text is automatically pasted** at your cursor location!

### System Tray Menu
- **Show Window**: Open the main window to view last transcription
- **Copy Last Transcription**: Copy the last transcription to clipboard
- **Settings**: Configure hotkey and Whisper model
- **Exit**: Close the application

## 🔧 Configuration

### Whisper Models
Available models (in order of size and accuracy):
- `tiny` - Fastest, ~75MB
- `base` - Fast, ~150MB
- `small` - Balanced, ~500MB **[Default]**
- `medium` - More accurate, ~1.5GB
- `large` - Most accurate, ~3GB

### Settings Location
All configuration is stored in: `%LOCALAPPDATA%\WinWisp\config.json`

## 🏗️ Future Releases

The next release (v1.1.0) will include:
- **Standalone Windows executable** (no Python required)
- **Windows installer** (.exe) for easy installation
- **Auto-start on Windows boot** option
- Improved error handling and logging

## 🐛 Known Issues

- First run requires internet connection to download Whisper model
- Large model sizes may take time to download
- Requires FFmpeg to be installed separately

## 🙏 Attribution

WinWisp uses OpenAI's Whisper model for speech recognition. See [ATTRIBUTION.md](ATTRIBUTION.md) for full details.

**Whisper**: https://github.com/openai/whisper

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

- **Issues**: https://github.com/CharlesMcquade/WinWisp/issues
- **Discussions**: https://github.com/CharlesMcquade/WinWisp/discussions

---

**Note**: This is a source-code release. Binary releases with installers are planned for future versions.
