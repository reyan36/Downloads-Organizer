; Script generated for Downloads Organizer

#define MyAppName "Downloads Organizer"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Reyan Arshad"
#define MyAppExeName "Downloads Organizer.exe"
; Expects files in the same folder as this .iss script
#define SourceDir "."

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={{8A47AD95-9721-4198-9086-453258837111}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Interface styling
WizardStyle=modern
; The name of the installer file created
OutputBaseFilename=Downloads Organizer Setup v1.0.0
; Compression settings
Compression=lzma
SolidCompression=yes
; IMPORTANT: You must have an .ico file for the installer icon
SetupIconFile={#SourceDir}\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startup"; Description: "Automatically start when Windows starts"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; The Main Executable (From your dist folder)
Source: "{#SourceDir}\Downloads Organizer.exe"; DestDir: "{app}"; Flags: ignoreversion
; The ICO file (Used for shortcuts)
Source: "{#SourceDir}\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
; The PNG file
Source: "{#SourceDir}\icon.png"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

[Icons]
; Start Menu Shortcut
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon.ico"
; Desktop Shortcut
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\icon.ico"

[Run]
; Option to run immediately after install
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

[Registry]
; Logic to handle "Start on Startup" checkbox during installation
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: startup

[UninstallDelete]
; Clean up the config file if it was created after installation
Type: files; Name: "{app}\organizer_config.json"

[Code]
// This function runs when the installer initializes
function InitializeSetup(): Boolean;
begin
  // Show the warning message about Windows Defender
  MsgBox('IMPORTANT NOTICE:' + #13#10 + #13#10 +
         'Since this is a custom tool, Windows Defender might falsely flag it as unknown.' + #13#10 + #13#10 +
         '1. If the installation is blocked, click "More Info" -> "Run Anyway".' + #13#10 +
         '2. It is recommended to add the installation folder to your Defender Exclusions to prevent interference.' + #13#10 + #13#10 +
         'Click OK to continue installation.', mbInformation, MB_OK);
  
  Result := True;
end;