from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import sys

class WebAutomation:
    def __init__(self):
        self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--inprivate")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--log-level=3")
        
        service = Service(EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(options=options, service=service)

    def login_to_portal(self, username, password):
        try:
            self.driver.get("https://portal.cc-student.com/index.php?cmd=login")
            print("Login-Seite geöffnet")
            sys.stdout.flush()

            username_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, "login_username"))
            )
            password_input = self.driver.find_element(By.NAME, "login_passwort")
            username_input.send_keys(username)
            password_input.send_keys(password)

            login_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
            login_button.click()

            zeiterfassung_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cmd=kug')]"))
            )
            zeiterfassung_button.click()

            zeiterfassung_oeffnen_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@name, 'showDialogButton')]"))
            )
            zeiterfassung_oeffnen_button.click()

            print("Login erfolgreich")
            sys.stdout.flush()

        except Exception as e:
            print(f"Fehler beim Login: {str(e)}")
            raise

    def logout_from_portal(self, username, password, exit_after_logout=True):
        try:
            # Logout-Logik hier
            print("Logout erfolgreich")
            if exit_after_logout:
                print("Beende Programm nach Logout...")
                sys.exit(0)
        except Exception as e:
            print(f"Fehler beim Logout: {str(e)}")
            raise

    def cleanup(self):
        if hasattr(self, 'driver'):
            self.driver.quit()