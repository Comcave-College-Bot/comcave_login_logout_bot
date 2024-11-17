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



            time.sleep(2)  # Längere Wartezeit für das Laden der Seite



            # Login-Daten eingeben

            print("Gebe Anmeldedaten ein...")

            sys.stdout.flush()

            username_input = WebDriverWait(self.driver, 10).until(

                EC.presence_of_element_located((By.NAME, "login_username"))

            )

            password_input = self.driver.find_element(By.NAME, "login_passwort")

            username_input.send_keys(username)

            password_input.send_keys(password)



            time.sleep(1)  # Wartezeit nach Eingabe



            # Login-Button klicken

            print("Führe Login durch...")

            sys.stdout.flush()

            login_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")

            self.driver.execute_script("arguments[0].click();", login_button)



            time.sleep(2)  # Längere Wartezeit nach Login



            # Zeiterfassung öffnen

            print("Öffne Zeiterfassung...")

            sys.stdout.flush()

            

            # Warte explizit auf das Laden der Seite

            WebDriverWait(self.driver, 10).until(

                lambda driver: driver.execute_script('return document.readyState') == 'complete'

            )



            zeiterfassung_button = WebDriverWait(self.driver, 10).until(

                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cmd=kug')]"))

            )

            zeiterfassung_button.click()  # Normaler Klick statt JavaScript



            time.sleep(1)



            zeiterfassung_oeffnen_button = WebDriverWait(self.driver, 10).until(

                EC.element_to_be_clickable((By.XPATH, "//button[contains(@name, 'showDialogButton')]"))

            )

            zeiterfassung_oeffnen_button.click()  # Normaler Klick statt JavaScript



            time.sleep(1)



            # Kommen-Button klicken

            print("Klicke Kommen-Button...")

            sys.stdout.flush()

            kommen_button = WebDriverWait(self.driver, 10).until(

                EC.element_to_be_clickable((By.XPATH, "//input[@class='buttonKommen']"))

            )

            kommen_button.click()  # Normaler Klick statt JavaScript

            

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



            # Direkt zum Zeiterfassungs-Dialog

            self.driver.get("https://portal.cc-student.com/index.php?cmd=kug")

            time.sleep(2)



            # Zeiterfassung öffnen

            print("Öffne Zeiterfassung...")

            sys.stdout.flush()

            

            zeiterfassung_oeffnen_button = WebDriverWait(self.driver, 10).until(

                EC.element_to_be_clickable((By.XPATH, "//button[contains(@name, 'showDialogButton')]"))

            )

            zeiterfassung_oeffnen_button.click()



            time.sleep(1)



            # Gehen-Button klicken

            print("Klicke Gehen-Button...")

            sys.stdout.flush()

            gehen_button = WebDriverWait(self.driver, 10).until(

                EC.element_to_be_clickable((By.XPATH, "//input[@class='buttonGehen']"))

            )

            gehen_button.click()

            

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
