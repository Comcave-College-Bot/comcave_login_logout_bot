import subprocess
import sys
import configparser
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Funktion zum Lesen der Konfiguration aus setup.ini
def read_config(key, section='DEFAULT'):
    config = configparser.ConfigParser()
    config.read('setup.ini')
    return config[section].get(key, '')

# Funktion zum Schreiben in die setup.ini
def write_config(key, value, section='DEFAULT'):
    config = configparser.ConfigParser()
    config.read('setup.ini')
    if section not in config:
        config[section] = {}
    config[section][key] = value
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

# Funktion zum Überprüfen und Installieren der benötigten Pakete
def check_and_install_packages():
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

# Funktion zum Überprüfen, ob ein Datum ein Urlaubstag oder gesetzlicher Feiertag ist
def is_holiday_or_vacation(date_to_check):
    holiday_str = read_config('urlaub_dates', section='Urlaub')
    legal_holiday_str = read_config('feiertag_dates', section='Gesetzliche Feiertage')
    holiday_ranges = parse_date_ranges(holiday_str)
    legal_holiday_ranges = parse_date_ranges(legal_holiday_str)

    print(f"Überprüfe Datum: {date_to_check} gegen Urlaubsdaten: {holiday_ranges} und Feiertagsdaten: {legal_holiday_ranges}")

    for start, end in holiday_ranges + legal_holiday_ranges:
        if start <= date_to_check <= end:
            print(f"Datum {date_to_check} ist ein Urlaubstag oder Feiertag.")
            return True
    print(f"Datum {date_to_check} ist kein Urlaubstag oder Feiertag.")
    return False

# Funktion zum Finden des nächsten gültigen Tages (kein Wochenende, Urlaub oder Feiertag)
def find_next_valid_day(current_date):
    next_date = current_date + timedelta(days=1)
    while next_date.weekday() >= 5 or is_holiday_or_vacation(next_date):
        print(f"{next_date} ist ein ungültiger Tag (Wochenende, Urlaub oder Feiertag), suche weiter...")
        next_date += timedelta(days=1)
    print(f"Nächster gültiger Tag gefunden: {next_date}")
    return next_date

# Funktion zum Parsen von Datumsbereichen aus der setup.ini
def parse_date_ranges(date_str):
    date_ranges = []
    if not date_str:
        return date_ranges

    for part in date_str.split(','):
        try:
            dates = part.split('-')
            start_date = datetime.strptime(dates[0].strip(), '%d.%m.%Y').date()
            end_date = start_date if len(dates) == 1 else datetime.strptime(dates[1].strip(), '%d.%m.%Y').date()
            date_ranges.append((start_date, end_date))
        except ValueError:
            print(f"Ungültiges Datumsformat: {part}. Erwartet: DD.MM.YYYY oder DD.MM.YYYY-DD.MM.YYYY.")
    return date_ranges

# Funktion zur Anzeige der nächsten geplanten Aktion
def print_next_action_time(next_action_date, planned_time):
    next_action_time = datetime.combine(next_action_date, planned_time)
    print(f"Nächste geplante Aktion am: {next_action_time.strftime('%d.%m.%Y %H:%M')}")

# Funktion zur Ausführung der Web-Automatisierung
def automate_web():
    today = datetime.now().date()
    if is_holiday_or_vacation(today):
        print("Heute ist ein Urlaubstag oder gesetzlicher Feiertag. Keine Aktionen werden durchgeführt.")
        return

    chrome_service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--incognito")

    try:
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    except Exception as e:
        print(f"Fehler beim Starten des WebDrivers: {e}")
        return

    username = read_config("username", section="Benutzerdaten")
    password = read_config("password", section="Benutzerdaten")

    try:
        driver.get("https://portal.cc-student.com/index.php?cmd=login")

        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "login_username"))
        )
        password_input = driver.find_element(By.NAME, "login_passwort")
        username_input.send_keys(username)
        password_input.send_keys(password)

        login_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        login_button.click()

        zeiterfassung_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cmd=kug')]"))
        )
        zeiterfassung_button.click()

        zeiterfassung_oeffnen_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@name, 'showDialogButton')]"))
        )
        zeiterfassung_oeffnen_button.click()

        gehen_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='buttonGehen']"))
        )
        driver.execute_script("arguments[0].click();", gehen_button)
        print("Gehen Button erfolgreich geklickt!")

    except Exception as e:
        print(f"Fehler aufgetreten: {str(e)}")
        print(driver.page_source)
    finally:
        driver.quit()

    # Ermittlung der nächsten gültigen Aktion
    next_action_date = find_next_valid_day(today)
    planned_time = datetime.now().time()  # Behalte die aktuelle Uhrzeit für die nächste geplante Aktion
    print_next_action_time(next_action_date, planned_time)

# Hauptfunktion
def main():
    check_and_install_packages()
    automate_web()

if __name__ == "__main__":
    main()
