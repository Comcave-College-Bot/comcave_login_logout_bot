# Installations- und Verteilungsanleitung

## Für Entwickler (Kompilierung)

1. Benötigte Tools:
   - Visual Studio mit C++ Compiler
   - Python 3.8 oder höher
   - Git (optional)

2. Kompilierung:
   - Öffnen Sie den jeweiligen Browser-Ordner
   - Führen Sie compile.bat aus oder nutzen Sie VS Code mit Strg+Shift+B
   - Die .exe wird im jeweiligen Browser-Ordner erstellt

## Für die Verteilung

1. Erstellen Sie für jeden Browser einen separaten Ordner:
   - Windows_Google_Chrome
   - Windows_Mozilla_Firefox
   - Windows_Microsoft_Edge

2. Kopieren Sie in jeden Ordner nur die notwendigen Dateien:
   ```
   Browser-Ordner/
   ├── comcave_bot_[browser].exe    # Kompilierte Anwendung
   ├── web_automation.py            # Browser-spezifisch
   ├── main.py                      # Identisch für alle
   ├── config_manager.py            # Identisch für alle
   └── requirements.txt             # Browser-spezifisch
   ```

3. Entfernen Sie alle Entwicklungsdateien:
   - *.cpp Quelldateien
   - *.rc und *.res Ressourcendateien
   - *.ico Dateien
   - compile.bat
   - Temporäre Build-Dateien (.obj, .ilk, .pdb)

## Für Endbenutzer

1. Voraussetzungen:
   - Python 3.8 oder höher
   - Der gewählte Browser muss installiert sein

2. Installation:
   - Entpacken Sie den Browser-Ordner an einen beliebigen Ort
   - Starten Sie die .exe
   - Beim ersten Start werden automatisch alle Python-Pakete installiert

3. Erste Einrichtung:
   - Geben Sie Ihre Anmeldedaten ein
   - Wählen Sie, ob diese gespeichert werden sollen
   - Legen Sie die Login- und Logout-Zeiten fest

## Hinweise

- Die setup.ini wird automatisch erstellt
- Jeder Browser benötigt seinen eigenen Ordner
- Python muss im System-PATH sein
- Administratorrechte für die Python-Paketinstallation erforderlich
