[Setup]
AppName=Daily word definition
AppVersion=1.0
DefaultDirName={userdocs}\Daily word definition
DefaultGroupName=Daily word definition
OutputBaseFilename=installer_dailyWord
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\bin\Daily_Word_Definition.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\bin\StartStopEditProgram.exe"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "..\bin\TimingLoop.exe"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "..\bin\WordDefAPI.exe"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "..\accessoryFiles\*"; DestDir: "{app}\accessoryFiles"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\README_postInstallation.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{userdesktop}\Daily Word Definition"; Filename: "{app}\Daily_Word_Definition.exe"; IconFilename: "{app}\accessoryFiles\icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon for this application"; GroupDescription: "Additional icons:"; Flags: unchecked
