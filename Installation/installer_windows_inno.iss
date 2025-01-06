[Setup]
AppName=Daily word definition
AppVersion=1.0
DefaultDirName={userdocs}\Daily word definition
DefaultGroupName=Daily word definition
OutputBaseFilename=installer_dailyWord
Compression=lzma
SolidCompression=yes
UninstallFilesDir={app}\Uninstall

[Files]
; Place Daily_Word_Definition and its dependencies in bin
Source: "..\bin\Daily_Word_Definition\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs

; Place StartStopEditProgram and its dependencies in bin
Source: "..\bin\StartStopEditProgram\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs

; Place TimingLoop and its dependencies in bin
Source: "..\bin\TimingLoop\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs

; Place WordDefAPI and its dependencies in bin
Source: "..\bin\WordDefAPI\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs

; Accessory files and README
Source: "..\accessoryFiles\*"; DestDir: "{app}\accessoryFiles"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\README_postInstallation.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Shortcut to the main entry executable on the desktop
Name: "{userdesktop}\Daily Word Definition"; Filename: "{app}\bin\Daily_Word_Definition\Daily_Word_Definition.exe"; IconFilename: "{app}\accessoryFiles\icon.ico"; Tasks: desktopicon

; Shortcut to the main entry executable in the main folder
Name: "{app}\Daily Word Definition"; Filename: "{app}\bin\Daily_Word_Definition\Daily_Word_Definition.exe"; IconFilename: "{app}\accessoryFiles\icon.ico"

[Tasks]
; Option to create a desktop icon
Name: "desktopicon"; Description: "Create a desktop icon for this application"; GroupDescription: "Additional icons:"; Flags: unchecked
