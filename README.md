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

**Coming Soon**: A Windows installer will be available in the Releases section.

For now, follow the developer installation instructions below.

### For Developers

1. **Prerequisites**:
   - Python 3.8 or higher
   - FFmpeg (required by Whisper)
   - Windows 10/11
   - **Optional**: NVIDIA GPU with CUDA support for faster transcription

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

### GPU vs CPU
WinWisp automatically detects and uses your GPU if available:
- **GPU (NVIDIA CUDA)**: Much faster transcription (2-10x speed)
- **CPU Only**: Works perfectly, just slower transcription times

No configuration needed - the app automatically uses the best available option.

**Transcription Speed Examples** (approximate):
- 10 seconds of audio on GPU: ~1-2 seconds
- 10 seconds of audio on CPU: ~5-15 seconds (depends on CPU)

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
