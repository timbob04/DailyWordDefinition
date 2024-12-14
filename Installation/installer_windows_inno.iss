; Define the installer settings
[Setup]
AppName=YourApp
AppVersion=1.0
DefaultDirName={pf}\YourApp
DefaultGroupName=YourApp
OutputBaseFilename=YourAppInstaller
Compression=lzma
SolidCompression=yes

; Define the files to install
[Files]
Source: "..\dist\UserInput.exe"; DestDir: "{app}\program"; Flags: ignoreversion
Source: "..\dist\Background.exe"; DestDir: "{app}\program"; Flags: ignoreversion
Source: "..\accessoryFiles\*"; DestDir: "{app}\accessoryFiles"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\README_afterInstallation.txt"; DestDir: "{app}"; Flags: ignoreversion

; Define shortcuts (only for UserControl)
[Icons]
Name: "{userdesktop}\YourApp Control"; Filename: "{app}\program\UserControl.exe"; IconFilename: "{app}\UserControl.ico"; Tasks: desktopicon

; Define additional tasks
[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon for YourApp Control"; GroupDescription: "Additional icons:"; Flags: unchecked
