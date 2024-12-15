; Define the installer settings
[Setup]
; Name of program - appears in add/remove program, etc 
AppName=Daily word definition
AppVersion=1.0
; default path for install.  {pf} a placeholder for 'Program files'
DefaultDirName={pf}\Daily word definition
DefaultGroupName=Daily word definition
OutputBaseFilename=installer_dailyWord
Compression=lzma
SolidCompression=yes

; Define the files to install
[Files]
Source: "..\dist\UserInput.exe"; DestDir: "{app}\program"; Flags: ignoreversion
Source: "..\dist\Background.exe"; DestDir: "{app}\program"; Flags: ignoreversion
Source: "..\accessoryFiles\*"; DestDir: "{app}\accessoryFiles"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\README_postInstallation.txt"; DestDir: "{app}"; Flags: ignoreversion

; Define shortcuts (only for UserInput)
[Icons]
Name: "{userdesktop}\Daily word definition"; Filename: "{app}\program\UserInput.exe"; IconFilename: "{app}\accessoryFiles\icon.ico"; Tasks: desktopicon

; Define additional tasks
[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon for this application"; GroupDescription: "Additional icons:"; Flags: unchecked
