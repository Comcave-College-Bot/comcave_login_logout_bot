# Comcave Login/Logout Bot

Dieses Programm automatisiert den Login und Logout für das CC Portal zur Zeiterfassung. Das Programm verwendet Selenium und WebDriver Manager, um den Prozess zu automatisieren. Bei jedem Start des Programms wird geprüft, ob Selenium und der WebDriver Manager installiert sind und ob die passende Version des ChromeDrivers vorhanden ist. Falls nicht, werden diese automatisch heruntergeladen und aktualisiert.

## Voraussetzungen

1. **Python 3.8 oder höher**: Stelle sicher, dass Python auf deinem System installiert ist.
   - Download: [Python Downloads](https://www.python.org/downloads/)
2. **Google Chrome Browser**: Das Programm verwendet Google Chrome zur Automatisierung. Stelle sicher, dass Chrome installiert ist und auf dem neuesten Stand ist.
   - Download: [Google Chrome](https://www.google.com/chrome/)

## Installationsanleitung

### Projekt herunterladen:

Lade das Projekt herunter oder klone das Repository:

- **Download des Programms**: [Hier herunterladen](https://www.dropbox.com/scl/fo/5kqktdn4x09v4bd921xdr/ANw4Sa3HWh80SLlJtmUWLPo?rlkey=3k6ejahxuceorti52ky4idouz&st=ws8ms32r&dl=0)

Einschränkungen
Nicht auf Standort-PCs verwendbar
Dieses Programm kann nicht auf den PCs am Standort verwendet werden, da:

Administratorrechte erforderlich sind, um Python zu installieren: Auf den PCs am Standort ist die Installation von Python ohne Administratorrechte nicht möglich.
Antivirus-Software die .exe-Dateien löscht: Die Antivirus-Software auf den Standort-PCs identifiziert die .exe-Dateien möglicherweise fälschlicherweise als Bedrohung und löscht sie.
Es wird empfohlen, das Programm auf einem privaten oder entsprechend konfigurierten Computer auszuführen, auf dem du die erforderlichen Rechte zur Installation und Nutzung der benötigten Software hast.


```bash
git clone https://github.com/dein-repository/comcave_login_logout_bot.git
cd comcave_login_logout_bot
