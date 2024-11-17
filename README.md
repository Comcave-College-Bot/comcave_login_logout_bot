# Comcave Login/Logout Bot

Dieses Programm automatisiert den Login und Logout für das CC Portal zur Zeiterfassung. Das Programm ist in drei Versionen verfügbar: für Google Chrome, Mozilla Firefox und Microsoft Edge. Die Automatisierung erfolgt über Selenium und den jeweiligen WebDriver Manager.

## Voraussetzungen

1. **Python 3.8 oder höher**
   - Download: [Python Downloads](https://www.python.org/downloads/)

2. **Einer der unterstützten Browser:**
   - [Google Chrome](https://www.google.com/chrome/)
   - [Mozilla Firefox](https://www.mozilla.org/firefox/)
   - [Microsoft Edge](https://www.microsoft.com/edge)

## Installation

1. Laden Sie die Version für Ihren bevorzugten Browser herunter
2. Entpacken Sie den Ordner an einen beliebigen Ort
3. Starten Sie die .exe Datei im entsprechenden Browser-Ordner:
   - Chrome: `comcave_bot_chrome.exe`
   - Firefox: `comcave_bot_firefox.exe`
   - Edge: `comcave_bot_edge.exe`

## Erste Nutzung

1. Beim ersten Start werden automatisch alle benötigten Python-Pakete installiert
2. Geben Sie Ihre Anmeldedaten ein
3. Wählen Sie, ob die Anmeldedaten gespeichert werden sollen
4. Legen Sie die gewünschten Zeiten für Login und Logout fest (Format: HH:MM, z.B. 13:30)

## Funktionsweise

- Das Programm läuft im Hintergrund und führt die Login/Logout-Aktionen automatisch zur eingestellten Zeit aus
- An Wochenenden und Feiertagen werden keine Aktionen ausgeführt
- Der Browser wird im Headless-Modus ausgeführt (unsichtbar)
- Die Anmeldedaten werden optional in einer setup.ini gespeichert

## Einschränkungen

**Nicht auf Standort-PCs verwendbar**, da:
- Administratorrechte für Python-Installation erforderlich sind
- Antivirus-Software die .exe-Dateien möglicherweise blockiert
- Eingeschränkte Benutzerrechte die Installation verhindern können

Es wird empfohlen, das Programm auf einem privaten Computer zu verwenden.

## Dateien im Programmordner

Jede Browser-Version enthält:
1. Die ausführbare Datei (.exe)
2. Python-Skripte für die Automatisierung
3. Eine requirements.txt für die Python-Abhängigkeiten

Die setup.ini wird automatisch erstellt, wenn Sie Ihre Anmeldedaten speichern.

## Sicherheitshinweise

- Gespeicherte Anmeldedaten werden lokal in der setup.ini gespeichert
- Das Programm kommuniziert nur mit dem CC Portal
- Alle Aktionen werden in der Konsole protokolliert

## Support

Bei Problemen oder Fragen:
1. Stellen Sie sicher, dass alle Voraussetzungen erfüllt sind
2. Prüfen Sie die Konsolenausgabe auf Fehlermeldungen
3. Stellen Sie sicher, dass der gewählte Browser installiert und aktuell ist


