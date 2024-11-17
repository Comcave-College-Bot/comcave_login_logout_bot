from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys

class WebAutomation:
    def __init__(self):
        self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--incognito")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=options, service=service)

    def login_to_portal(self, username, password):
        try:
            # Login-Seite öffnen
            self.driver.get("https://portal.cc-student.com/index.php?cmd=login")
            print("Login-Seite geöffnet")
            sys.stdout.flush()

            time.sleep(1)  # Kurz warten, bis die Seite vollständig geladen ist

            # Login-Daten eingeben
            print("Gebe Anmeldedaten ein...")
            sys.stdout.flush()
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "login_username"))
            )
            password_input = self.driver.find_element(By.NAME, "login_passwort")
            username_input.send_keys(username)
            password_input.send_keys(password)

            time.sleep(0.5)  # Kurz warten nach Eingabe

            # Login-Button klicken
            print("Führe Login durch...")
            sys.stdout.flush()
            login_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
            self.driver.execute_script("arguments[0].click();", login_button)

            time.sleep(1)  # Warten nach Login

            # Zeiterfassung öffnen
            print("Öffne Zeiterfassung...")
            sys.stdout.flush()
            zeiterfassung_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cmd=kug')]"))
            )
            self.driver.execute_script("arguments[0].click();", zeiterfassung_button)

            time.sleep(0.5)  # Warten nach Klick

            zeiterfassung_oeffnen_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@name, 'showDialogButton')]"))
            )
            self.driver.execute_script("arguments[0].click();", zeiterfassung_oeffnen_button)

            time.sleep(0.5)  # Warten nach Dialog-Öffnung

            # Kommen-Button klicken
            print("Klicke Kommen-Button...")
            sys.stdout.flush()
            kommen_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@class='buttonKommen']"))
            )
            self.driver.execute_script("arguments[0].click();", kommen_button)
            print("Login erfolgreich")
            sys.stdout.flush()
            return True

        except Exception as e:
            print(f"Login nicht möglich: {str(e)}")
            sys.stdout.flush()
            return False

    def logout_from_portal(self, username, password):
        try:
            print("Starte Logout-Prozess...")
            sys.stdout.flush()

            # Komplett neue Session für Logout
            self.driver.quit()
            self.setup_driver()

            # Login-Seite öffnen
            print("Öffne Login-Seite für Logout...")
            sys.stdout.flush()
            self.driver.get("https://portal.cc-student.com/index.php?cmd=login")

            time.sleep(1)  # Kurz warten, bis die Seite vollständig geladen ist

            # Login-Daten eingeben
            print("Gebe Anmeldedaten ein...")
            sys.stdout.flush()
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "login_username"))
            )
            password_input = self.driver.find_element(By.NAME, "login_passwort")
            username_input.send_keys(username)
            password_input.send_keys(password)

            time.sleep(0.5)  # Kurz warten nach Eingabe

            # Login-Button klicken
            print("Führe Login für Logout durch...")
            sys.stdout.flush()
            login_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
            self.driver.execute_script("arguments[0].click();", login_button)

            time.sleep(1)  # Warten nach Login

            # Zeiterfassung öffnen
            print("Öffne Zeiterfassung...")
            sys.stdout.flush()
            zeiterfassung_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cmd=kug')]"))
            )
            self.driver.execute_script("arguments[0].click();", zeiterfassung_button)

            time.sleep(0.5)  # Warten nach Klick

            zeiterfassung_oeffnen_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@name, 'showDialogButton')]"))
            )
            self.driver.execute_script("arguments[0].click();", zeiterfassung_oeffnen_button)

            time.sleep(0.5)  # Warten nach Dialog-Öffnung

            # Gehen-Button klicken
            print("Klicke Gehen-Button...")
            sys.stdout.flush()
            gehen_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@class='buttonGehen']"))
            )
            self.driver.execute_script("arguments[0].click();", gehen_button)
            print("Logout erfolgreich")
            sys.stdout.flush()
            return True

        except Exception as e:
            print(f"Logout nicht möglich: {str(e)}")
            sys.stdout.flush()
            return False

    def cleanup(self):
        if hasattr(self, 'driver'):
            self.driver.quit()