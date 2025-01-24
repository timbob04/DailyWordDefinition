[Setup]
AppName=Daily word definition
AppVersion=1.0
DefaultDirName={userdocs}\Daily word definition
DefaultGroupName=Daily word definition
OutputBaseFilename=installer_dailyWord
Compression=lzma
SolidCompression=yes
UninstallFilesDir={app}\Uninstall
; Disalble option to choose installed location
DisableDirPage=no
; Disalble option to choose installed file name (if yes, DefaultDirName used)
DisableProgramGroupPage=yes

[Files]
Source: "..\bin\Daily_Word_Definition\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\bin\LoadingProgramConsole\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\bin\StartStopEditProgram\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\bin\StartingProgramConsole\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\bin\TimingLoop\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\bin\WordDefAPI\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\accessoryFiles\*"; DestDir: "{app}\accessoryFiles"; Excludes: "readme.txt"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\accessoryFiles\readme.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Shortcut to Daily_Word_Definition.exe on the desktop
Name: "{userdesktop}\Daily Word Definition"; Filename: "{app}\bin\Daily_Word_Definition.exe"; WorkingDir: "{app}\bin"; IconFilename: "{app}\accessoryFiles\icon_DailyWord.ico"; Tasks: desktopicon
; Shortcut to Daily_Word_Definition.exe in the main folder
Name: "{app}\Daily Word Definition"; Filename: "{app}\bin\Daily_Word_Definition.exe"; WorkingDir: "{app}\bin"; IconFilename: "{app}\accessoryFiles\icon_DailyWord.ico"

[Tasks]
; Option to create a desktop icon
Name: "desktopicon"; Description: "Create a desktop icon for this application"; GroupDescription: "Additional icons:"; Flags: unchecked
