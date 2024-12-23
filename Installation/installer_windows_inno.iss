[Setup]
AppName=Daily word definition
AppVersion=1.0
DefaultDirName={localappdata}\Daily word definition
DefaultGroupName=Daily word definition
OutputBaseFilename=installer_dailyWord
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\bin\DailyWordDefinition.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\bin\TimingLoop.exe"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "..\bin\WordDefAPI.exe"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "..\accessoryFiles\*"; DestDir: "{app}\accessoryFiles"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\README_postInstallation.txt"; DestDir: "{app}"; Flags: ignoreversion

; Define shortcuts (only for UserInput)
[Icons]
Name: "{userdesktop}\Daily word definition"; Filename: "{app}\program\UserInput.exe"; IconFilename: "{app}\accessoryFiles\icon.ico"; Tasks: desktopicon

; Define additional tasks
[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon for this application"; GroupDescription: "Additional icons:"; Flags: unchecked

