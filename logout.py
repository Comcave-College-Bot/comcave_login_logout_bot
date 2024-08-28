from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

def automate_web(username, password):
    # Pfad zum ChromeDriver
    chrome_service = Service(r'C:\Users\CC-Student\projects\comcave_login_bot\chromedriver.exe')

    # Chrome Optionen
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless mode (falls kein UI benötigt)
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--incognito")  # Inkognito-Modus

    # WebDriver initialisieren
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

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

if __name__ == "__main__":
    # Username und Passwort werden als Argumente übergeben
    username = sys.argv[1]
    password = sys.argv[2]
    automate_web(username, password)
