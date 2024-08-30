import subprocess
import sys
import configparser
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Funktion zum Lesen der Konfiguration aus der setup.ini
def read_config(key):
    config = configparser.ConfigParser()
    config.read('setup.ini')
    return config['DEFAULT'].get(key, '')

# Funktion zum Schreiben in die setup.ini
def write_config(key, value):
    config = configparser.ConfigParser()
    config.read('setup.ini')
    if 'DEFAULT' not in config:
        config['DEFAULT'] = {}
    config['DEFAULT'][key] = value
    with open('setup.ini', 'w') as configfile:
        config.write(configfile)

# Funktion zur Installation von Python-Paketen
def install_package(package_name):
    try:
        print(f"Installiere {package_name}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
        print(f"{package_name} wurde erfolgreich installiert.")
        return True
    except Exception as e:
        print(f"Fehler bei der Installation von {package_name}: {e}")
        return False

# Funktion zum Prüfen und Installieren von benötigten Paketen
def check_and_install_packages():
    # Überprüfen, ob selenium installiert ist
    selenium_installed = False
    webdriver_manager_installed = False

    try:
        import selenium
        selenium_installed = True
    except ImportError:
        print("selenium ist nicht installiert.")

    try:
        from webdriver_manager.chrome import ChromeDriverManager
        webdriver_manager_installed = True
    except ImportError:
        print("webdriver-manager ist nicht installiert.")

    # Installiere fehlende Pakete und aktualisiere die setup.ini
    if not selenium_installed:
        if install_package('selenium'):
            write_config('selenium_installed', 'true')
        else:
            print("Installation von selenium fehlgeschlagen.")
    
    if not webdriver_manager_installed:
        if install_package('webdriver-manager'):
            write_config('webdriver_manager_installed', 'true')
        else:
            print("Installation von webdriver-manager fehlgeschlagen.")

# Funktion zur Ausführung der Web-Automatisierung
def automate_web():
    # Chrome Optionen und ChromeDriver über den WebDriverManager installieren
    chrome_service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless mode (falls kein UI benötigt)
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--incognito")  # Inkognito-Modus

    # WebDriver initialisieren
    try:
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    except Exception as e:
        print(f"Fehler beim Starten des WebDrivers: {e}")
        return

    # Login-Daten aus der setup.ini lesen
    username = read_config("username")
    password = read_config("password")

    try:
        # Login-Seite öffnen
        driver.get("https://portal.cc-student.com/index.php?cmd=login")

        # Warte, bis das Element sichtbar ist
        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "login_username"))
        )

        # Login-Daten eingeben
        password_input = driver.find_element(By.NAME, "login_passwort")
        username_input.send_keys(username)
        password_input.send_keys(password)

        # Login-Button klicken
        login_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        login_button.click()

        # Warte, bis die Hauptseite geladen ist und klicke auf "Zeiterfassung"
        zeiterfassung_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cmd=kug')]"))
        )
        zeiterfassung_button.click()

        # Warte, bis der "Zeiterfassung öffnen"-Button sichtbar ist
        zeiterfassung_oeffnen_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@name, 'showDialogButton')]"))
        )
        zeiterfassung_oeffnen_button.click()

        # Warte, bis das Dialogfeld erscheint und der "Gehen"-Button klickbar ist
        gehen_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='buttonGehen']"))
        )
        
        # Klick auf den "Gehen"-Button via JavaScript
        driver.execute_script("arguments[0].click();", gehen_button)
        print("Gehen Button erfolgreich geklickt!")

    except Exception as e:
        print(f"Fehler aufgetreten: {str(e)}")
        print(driver.page_source)  # Druckt den gesamten Seitenquellcode zur Diagnose
    finally:
        # Schließe den Browser
        driver.quit()

# Hauptfunktion
def main():
    # Überprüfen und Installieren der benötigten Pakete
    check_and_install_packages()

    # Fortfahren mit der Web-Automatisierung
    automate_web()

if __name__ == "__main__":
    main()
