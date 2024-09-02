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

## Funktionsbeschreibung
### 1. check_and_install_packages()
Diese Funktion überprüft, ob die benötigten Pakete (selenium und webdriver-manager) installiert sind.
Falls sie nicht vorhanden sind, werden sie automatisch installiert und in der setup.ini vermerkt.
### 2. install_package(package_name)
Installiert ein angegebenes Python-Paket mit pip.
Wird verwendet, um selenium und webdriver-manager bei Bedarf automatisch zu installieren.
### 3. read_config(key)
Liest den Wert eines bestimmten Schlüssels aus der setup.ini Konfigurationsdatei.
Wird verwendet, um Einstellungen wie username, password, und ChromeDriverPath zu lesen.
### 4. write_config(key, value)
Schreibt einen neuen Wert in die setup.ini Konfigurationsdatei oder aktualisiert ihn, wenn der Schlüssel bereits existiert.
### 5. clear_and_write_credentials(username, password)
Löscht die vorhandenen Anmeldeinformationen (username und password) aus der setup.ini und speichert die neuen Informationen.
Wird aufgerufen, wenn die Anmeldedaten vom Benutzer gespeichert werden sollen.
### 6. login(username, password)
Führt den automatisierten Login im CC Portal durch.
Ruft das Python-Skript login.py auf, um die Web-Automatisierung zu starten.
### 7. logout(username, password)
Führt den automatisierten Logout im CC Portal durch.
Ruft das Python-Skript logout.py auf, um die Web-Automatisierung zu starten.
### 8. automate_web()
Führt die Hauptaufgabe der Web-Automatisierung durch.
Verwendet Selenium, um den Webbrowser zu steuern und den Login- und Logout-Prozess auszuführen.
### 9. schedule_task(time, task)
Plant eine Aufgabe (task) zu einer bestimmten Uhrzeit (time).
Wartet, bis die festgelegte Uhrzeit erreicht ist, bevor die Aufgabe ausgeführt wird.
### 10. parseTime(timeStr)
Überprüft und parst eine Uhrzeit im Format HH:MM.
Stellt sicher, dass die eingegebene Zeit korrekt ist und innerhalb der gültigen Stunden- und Minutenbereiche liegt.
### 11. is_weekday()
Überprüft, ob der aktuelle Tag ein Werktag (Montag bis Freitag) ist.
Verwendet, um sicherzustellen, dass Login- und Logout-Aktionen nur an Werktagen durchgeführt werden.
### 12. main()
Die Hauptfunktion, die den gesamten Ablauf des Programms steuert.
Führt die Paketüberprüfung, Installation und die Web-Automatisierung durch.

## Einschränkungen
Nicht auf Standort-PCs verwendbar
Dieses Programm kann nicht auf den PCs am Standort verwendet werden, da:

Administratorrechte erforderlich sind, um Python zu installieren: Auf den PCs am Standort ist die Installation von Python ohne Administratorrechte nicht möglich.
Antivirus-Software die .exe-Dateien löscht: Die Antivirus-Software auf den Standort-PCs identifiziert die .exe-Dateien möglicherweise fälschlicherweise als Bedrohung und löscht sie.
Es wird empfohlen, das Programm auf einem privaten oder entsprechend konfigurierten Computer auszuführen, auf dem du die erforderlichen Rechte zur Installation und Nutzung der benötigten Software hast.


```bash
git clone https://github.com/dein-repository/comcave_login_logout_bot.git
cd comcave_login_logout_bot
