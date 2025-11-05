; Inno Setup Script for WinWisp
; Creates a Windows installer for WinWisp

#define MyAppName "WinWisp"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "WinWisp"
#define MyAppURL "https://github.com/CharlesMcquade/WinWisp"
#define MyAppExeName "WinWisp.exe"

[Setup]
; Application information
AppId={{A1B2C3D4-E5F6-4A5B-8C9D-0E1F2A3B4C5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output
OutputDir=..\installer_output
OutputBaseFilename=WinWisp-Setup-{#MyAppVersion}
SetupIconFile=app_icon.ico
Compression=lzma
SolidCompression=yes

; Windows version requirements
MinVersion=10.0
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; UI
WizardStyle=modern
DisableWelcomePage=no
LicenseFile=..\LICENSE

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startup"; Description: "Run WinWisp on Windows startup"; GroupDescription: "Startup Options:"; Flags: unchecked

[Files]
Source: "..\dist\WinWisp.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\ATTRIBUTION.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startup

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  // Check if FFmpeg is installed
  if not FileExists(ExpandConstant('{sys}\ffmpeg.exe')) and 
     not RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\FFmpeg') then
  begin
    if MsgBox('FFmpeg is required but not detected. Do you want to continue anyway?' + #13#10 + 
              'You can install FFmpeg later from https://ffmpeg.org/', 
              mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create config directory
    CreateDir(ExpandConstant('{userappdata}\WinWisp'));
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  ConfigPath: String;
begin
  if CurUninstallStep = usUninstall then
  begin
    if MsgBox('Do you want to remove user settings and recordings?', 
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      ConfigPath := ExpandConstant('{userappdata}\WinWisp');
      if DirExists(ConfigPath) then
        DelTree(ConfigPath, True, True, True);
    end;
  end;
end;
