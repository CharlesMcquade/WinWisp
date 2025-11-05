# WinWisp

A Windows application that uses OpenAI's Whisper model to convert speech to text, activated by a global hotkey.

## Features

- 🎤 **Global Hotkey Activation**: Press `Ctrl+Shift+Space` to start/stop recording
- 🎯 **Auto-Paste**: Transcribed text is automatically pasted at the active cursor location
- 📋 **Clipboard Support**: Copy the last transcription to clipboard from the tray menu
- 🖥️ **System Tray**: Runs minimized in the system tray
- ⚙️ **Configurable**: Settings window to customize hotkey and Whisper model
- 🔊 **Real-time Feedback**: Visual and audio feedback during recording
- 💻 **Standalone Executable**: No Python installation required for end users
- 🚀 **Windows Installer**: Easy installation with Start Menu integration

## Installation

### For End Users (Recommended)

1. **Download the installer**: `WinWisp-Setup.exe` from the [Releases](https://github.com/CharlesMcquade/WinWisp/releases) page
2. **Run the installer** and follow the prompts
3. **Install FFmpeg** (if not already installed):
   - Download from: https://ffmpeg.org/download.html
   - Add to system PATH
4. **Launch WinWisp** from the Start Menu or desktop shortcut

The first run will download the Whisper model (this may take a few minutes).

### For Developers

1. **Prerequisites**:
   - Python 3.8 or higher
   - FFmpeg (required by Whisper)
   - Windows 10/11

2. **Clone the repository**:
   ```bash
   git clone https://github.com/CharlesMcquade/WinWisp.git
   cd WinWisp
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run from source**:
   ```bash
   python main.py
   ```

See [BUILD_GUIDE.md](BUILD_GUIDE.md) for instructions on building the executable and installer.

## Usage

1. **Launch WinWisp**: The app starts minimized in the system tray with a microphone icon
2. **Press the hotkey**: `Ctrl+Shift+Space` to start recording (icon turns red)
3. **Speak your message**: The app records your audio
4. **Press the hotkey again**: Stops recording and begins transcription
5. **Text is pasted**: Transcribed text is automatically pasted at your cursor location

### Tray Menu Options:
- **Show Window**: Open the main window
- **Copy Last Transcription**: Copy the last transcription to clipboard
- **Settings**: Configure hotkey and Whisper model
- **Exit**: Close the application

## Configuration

### User Data Location
All user data is stored in: `%LOCALAPPDATA%\WinWisp\`
- Configuration: `config.json`
- Logs: `logs/`
- Recordings: `recordings/` (if enabled)

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

## Building from Source

See [BUILD_GUIDE.md](BUILD_GUIDE.md) for detailed instructions on:
- Building the standalone executable
- Creating the Windows installer
- Distribution and deployment

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Attribution

This project uses [OpenAI Whisper](https://github.com/openai/whisper), a general-purpose speech recognition model by OpenAI.

**Whisper Citation:**
```
@misc{radford2022whisper,
  title={Robust Speech Recognition via Large-Scale Weak Supervision},
  author={Radford, Alec and Kim, Jong Wook and Xu, Tao and Brockman, Greg and McLeavey, Christine and Sutskever, Ilya},
  year={2022},
  eprint={2212.04356},
  archivePrefix={arXiv},
  primaryClass={eess.AS}
}
```

Whisper is licensed under the MIT License - Copyright (c) 2022 OpenAI.

## License

WinWisp is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This project is a third-party application and is not affiliated with, officially maintained, or endorsed by OpenAI.
