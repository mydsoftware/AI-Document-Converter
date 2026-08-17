; نصب‌کننده ویندوز مبدل هوشمند همه‌کاره
; نیازمند Inno Setup 6

#define AppName "مبدل هوشمند همه‌کاره"
#define AppVersion "0.1.0"
#define AppPublisher "AI Document Converter"
#define AppExeName "AI-Document-Converter-GUI.exe"

[Setup]
AppId={{B5B4B3E5-4B1C-4C76-8E1A-ADC000000001}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\AI-Document-Converter
DefaultGroupName={#AppName}
OutputDir=output
OutputBaseFilename=AI-Document-Converter-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible

[Files]
Source: "..\dist\AI-Document-Converter-GUI\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"

[Run]
Filename: "{app}\{#AppExeName}"; Description: "اجرای {#AppName}"; Flags: nowait postinstall skipifsilent
